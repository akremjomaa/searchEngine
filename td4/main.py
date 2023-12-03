import datetime
import praw
from Author import Author
import sys
from document_factory import DocumentFactory


sys.stdout = open(sys.stdout.fileno(), mode="w", encoding="utf-8", buffering=1)

reddit = praw.Reddit(
    client_id="UKtZgFhv6izOz1HVZYi4iQ",
    client_secret="DKMUyLlfc-6pjWK2XE4fNSN6O7C5nA",
    user_agent="Test App",
)

hot_posts = reddit.subreddit("Handball").hot(limit=100)
id2doc = {}
counter = 0
listData = []
for post in hot_posts:
    if post.selftext != "":
        titre = (
            post.title.encode("utf-8", errors="ignore")
            .decode("utf-8")
            .replace("\n", "")
        )
        auteur = str(post.author)
        date = datetime.datetime.fromtimestamp(post.created_utc).strftime("%Y/%m/%d")
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


import urllib, urllib.request
import xmltodict
from datetime import datetime

query = "covid"
url = (
    "http://export.arxiv.org/api/query?search_query=all:"
    + query
    + "&start=0&max_results=100"
)
data = urllib.request.urlopen(url).read().decode("utf-8")

# transform the data from xml to json
dataToJson = xmltodict.parse(data)

# get the specific data that i need
adocs = dataToJson["feed"]["entry"]

for aPost in adocs:
    titre = aPost["title"].replace("\n", "")
    try:
        authors = ", ".join(
            [a["name"] for a in aPost["author"]]
        )  # On fait une liste d'auteurs, séparés par une virgule
    except:
        authors = aPost["author"]["name"]  # Si l'auteur est seul, pas besoin de liste

    summary = aPost["summary"].replace("\n", "")  # On enlève les retours à la ligne
    date = datetime.strptime(aPost["published"], "%Y-%m-%dT%H:%M:%SZ").strftime(
        "%Y/%m/%d"
    )  # Formatage de la date en année/mois/jour avec librairie datetime

    adoc = DocumentFactory.create_document(
        "Arxiv",
        titre,
        authors,
        date,
        aPost["link"][1]["@href"],
        summary,
    )
    listData.append(("Arxiv", adoc))


for origin, data in listData:
    id = f"{origin}_{counter}"
    id2doc[id] = data
    counter += 1

id2aut = {}
authors = {}
idAuthor = 0
for doc in id2doc.values():
    if doc.auteur not in id2aut:
        idAuthor += 1
        authors[idAuthor] = Author(doc.auteur)
        id2aut[doc.auteur] = authors[idAuthor]

from Corpus import Corpus

CorpusNoSingleton = Corpus
del Corpus
corpus = CorpusNoSingleton("Mon corpus")


def fillCorpus(docType=""):
    for origin, d in listData:
        if docType == origin:
            corpus.add(d)
        else:
            corpus.add(d)


fillCorpus()
import pickle

with open("corpus.pkl", "wb") as f:
    pickle.dump(corpus, f)


from decorators import singleton


@singleton
class Corpus(CorpusNoSingleton):
    pass


with open("corpus.pkl", "rb") as f:
    corpus = pickle.load(f)

print(corpus)
