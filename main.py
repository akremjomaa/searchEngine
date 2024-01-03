from datetime import datetime
import praw
import prawcore
import sys
from models.Author import Author
from models.document_factory import DocumentFactory
import urllib, urllib.request
import xmltodict
import dill
import os
from models.Corpus import Corpus

from dotenv import load_dotenv

########################################################################################
############### Setup the settings ( Load environment variables and set stdout to utf-8 )
########################################################################################

load_dotenv()
sys.stdout = open(sys.stdout.fileno(), mode="w", encoding="utf-8", buffering=1)

########################################################################################
########################### Creating a global variable for the main subject
########################################################################################


listData = []
id2doc = {}
id2aut = {}
authors = {}


########################################################################################
######### Fuctions to fetch data from Reddit and Arxiv and fill the corpus with it
########################################################################################


def fetch_reddit_data(query, limit=10):
    """
    Fetches data from Reddit and fills the listData list with it.
    @param query: the query to search for
    @param limit: the maximum number of posts to fetch (default: 10)
    @return: None
    """
    client_id = os.environ.get("REDDIT_CLIENT_ID")
    client_secret = os.environ.get("REDDIT_SECRET_ID")
    user_agent = os.environ.get("REDDIT_USER_AGENT")

    reddit = praw.Reddit(
        client_id=client_id,
        client_secret=client_secret,
        user_agent=user_agent,
    )

    hot_posts = reddit.subreddit(query).hot(limit=limit)
    try:
        for post in hot_posts:
            if post.selftext != "":
                titre = (
                    post.title.encode("utf-8", errors="ignore")
                    .decode("utf-8")
                    .replace("\n", "")
                )

                auteur = str(post.author)
                date = datetime.fromtimestamp(post.created_utc).strftime("%Y/%m/%d")
                url = post.url
                texte = post.selftext.replace("\n", "")

                doc = DocumentFactory.create_document(
                    "Reddit",
                    titre,
                    auteur,
                    date,
                    url,
                    texte,
                )
            listData.append(("Reddit", doc))
    except (
        prawcore.exceptions.Redirect,
        prawcore.exceptions.Forbidden,
        prawcore.exceptions.NotFound,
        prawcore.exceptions.ServerError,
        prawcore.exceptions.ResponseException,
    ) as e:
        print("[ERRER] -- While fetching data from Reddit, an error occured:")
        if e.response.status_code == 404:
            print(
                """
********************************************************
The subreddit you entered does not exist.
Please make sure you entered the correct subreddit name.
********************************************************
            """
            )
        elif e.response.status_code == 403:
            print(
                """
********************************************************
You are not allowed to access this subreddit.
Please make sure you entered the correct subreddit name.
********************************************************
            """
            )
        elif e.response.status_code == 302:
            print(
                """
********************************************************
The subreddit you entered does not exist.
Please make sure you entered the correct subreddit name.
********************************************************
            """
            )
        elif e.response.status_code == 500:
            print(
                """
********************************************************
An internal server error occured.
Please try again later.
********************************************************
            """
            )
        else:
            print(e.response.status_code)
            print("Exiting...")
            sys.exit(1)


def fetch_arxiv_data(query, limit=10):
    """
    Fetches data from Arxiv and fills the listData list with it.
    @param query: the query to search for
    @param limit: the maximum number of posts to fetch (default: 10)
    @return: None
    """
    url = (
        "http://export.arxiv.org/api/query?search_query=all:"
        + query
        + "&start=0&max_results="
        + str(limit)
    )

    data = urllib.request.urlopen(url).read().decode("utf-8")

    # transform the data from xml to json

    dataToJson = xmltodict.parse(data)

    if (
        "entry" in dataToJson["feed"]
    ):  # check if the key 'entry' exists in the json before trying to access it because it may not exist
        adocs = dataToJson["feed"]["entry"]
        for aPost in adocs:
            titre = aPost["title"].replace("\n", "")
            try:
                authors = ", ".join([a["name"] for a in aPost["author"]])
            except TypeError:
                authors = aPost["author"]["name"]

            summary = aPost["summary"].replace("\n", "")
            date = datetime.strptime(aPost["published"], "%Y-%m-%dT%H:%M:%SZ").strftime(
                "%Y/%m/%d"
            )

            adoc = DocumentFactory.create_document(
                "Arxiv",
                titre,
                authors,
                date,
                aPost["link"][1]["@href"],
                summary,
            )
            listData.append(("Arxiv", adoc))
    else:
        print(
            """
[ERROR] -- While fetching data from Arxiv, an error occured:
********************************************************
No 'entry' key found in the (Arxiv) API response. Unable to retrieve document information.
********************************************************
            """
        )


def fillDocDict():
    counter = 0
    for origin, data in listData:
        id = f"{origin}_{counter}"
        id2doc[id] = data
        counter += 1


def fillAuthorsDict():
    idAuthor = 0
    for doc in id2doc.values():
        if doc.auteur not in id2aut:
            idAuthor += 1
            authors[idAuthor] = Author(doc.auteur)
            id2aut[doc.auteur] = authors[idAuthor]


def fillCorpus(docType=""):
    global nbPosts
    for origin, d in listData:
        if docType == origin:
            corpus.add(d)
            nbPosts += 1
        else:
            corpus.add(d)
            nbPosts += 1


if __name__ == "__main__":
    CorpusNoSingleton = Corpus
    del Corpus
    corpus = CorpusNoSingleton("Mon corpus")
    nbPosts = 0

    print("Welcome to the document retrieval system.\n")
    print("This work was made by GHIZLAN MOQIM and JOMAA AKREM.\n")
    opt = input("1) Fetch new data\n2) Exit\n> ")
    if opt == "1":
        query = input("Enter a query to search for:\n> ")
        limit = input("Enter the maximum number of posts to fetch: Default is 10\n> ")
        if limit == "":
            limit = 10
        else:
            try:
                limit = int(limit)
            except ValueError:
                print("[ERRER] -- Invalid input!")
                sys.exit(1)

        print("-" * 50)
        print("Fetching data from Reddit...")
        fetch_reddit_data(query, limit)

        print("-" * 50)
        print("Fetching data from Arxiv...")
        fetch_arxiv_data(query, limit)

        print("-" * 50)
        print("Filling the document dictionary...")
        fillDocDict()

        print("-" * 50)
        print("Filling the authors dictionary...")
        fillAuthorsDict()

        print("-" * 50)
        print("Filling the corpus...")
        fillCorpus()

        print("-" * 50)
        print("Saving the corpus...")
        with open("corpus.pkl", "wb") as f:
            dill.dump(corpus, f)
        print("Done!")
        print(f"{nbPosts} posts were added to the corpus.")

        print("Here is your corpus: \n")
        print("=" * 50)
        print(corpus)
        print("=" * 50)

    elif opt == "2":
        print("Goodbye!")
    else:
        print("Invalid option!")
