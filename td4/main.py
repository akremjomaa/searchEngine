import datetime
import praw
from Document import Document
from Author import Author

reddit = praw.Reddit(
    client_id="UKtZgFhv6izOz1HVZYi4iQ",
    client_secret="DKMUyLlfc-6pjWK2XE4fNSN6O7C5nA",
    user_agent="Test App",
)

hot_posts = reddit.subreddit("Coronavirus").hot(limit=100)

id2doc = {}
print(hot_posts)
counter = 0
for i, post in enumerate(hot_posts):
    if post.selftext != "":
        doc_id = f"reddit_{counter}"
        counter += 1
        doc = Document(
            post.title,
            post.author,
            datetime.datetime.utcfromtimestamp(post.created_utc),
            post.url,
            post.selftext,
        )
        id2doc[doc_id] = doc

# print(id2doc)


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
docs = dataToJson["feed"]["entry"]


for j, aPost in enumerate(docs):
    doc_id = f"arxiv_{counter}"
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

    doc = Document(
        titre,
        authors,
        date,
        aPost["link"][1]["@href"],
        summary,
    )
    id2doc[doc_id] = doc

print(id2doc)
