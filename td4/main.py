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
counter = 0
listData = []
for post in hot_posts:
    if post.selftext != "":
        titre = post.title.replace("\n", "")
        auteur = str(post.author)
        date = datetime.datetime.fromtimestamp(post.created_utc).strftime("%Y/%m/%d")
        url = post.url
        texte = post.selftext.replace("\n", "")
        doc = Document(
            titre,
            auteur,
            date,
            url,
            texte,
        )
    listData.append(("Reddit", doc))
# print(listData)


# for i, post in enumerate(hot_posts):
#     if post.selftext != "":
#         titre = post.title.replace("\n", "")
#         auteur = str(post.author)
#         date = datetime.datetime.fromtimestamp(post.created_utc).strftime("%Y/%m/%d")
#         url = post.url
#         texte = post.selftext.replace("\n", "")
#         doc_id = f"reddit_{counter}"
#         counter += 1
#         doc = Document(
#             titre,
#             auteur,
#             date,
#             url,
#             texte,
#         )
#         id2doc[doc_id] = doc

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

    adoc = Document(
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

# print(id2doc)
# for j, aPost in enumerate(docs):
#     doc_id = f"arxiv_{counter}"
#     titre = aPost["title"].replace("\n", "")
#     try:
#         authors = ", ".join(
#             [a["name"] for a in aPost["author"]]
#         )  # On fait une liste d'auteurs, séparés par une virgule
#     except:
#         authors = aPost["author"]["name"]  # Si l'auteur est seul, pas besoin de liste
#     summary = aPost["summary"].replace("\n", "")  # On enlève les retours à la ligne
#     date = datetime.strptime(aPost["published"], "%Y-%m-%dT%H:%M:%SZ").strftime(
#         "%Y/%m/%d"
#     )  # Formatage de la date en année/mois/jour avec librairie datetime

#     doc = Document(
#         titre,
#         authors,
#         date,
#         aPost["link"][1]["@href"],
#         summary,
#     )
#     id2doc[doc_id] = doc

# print(id2doc)


id2aut = {}
authors = {}
idAuthor = 0
for doc in id2doc.values():
    if doc.auteur not in id2aut:
        idAuthor += 1
        authors[idAuthor] = Author(doc.auteur)
        id2aut[doc.auteur] = authors[idAuthor]

from Corpus import Corpus

corpus = Corpus("Mon corpus")

for origin, d in listData:
    corpus.add(d)

# print(corpus)
import pickle

with open("corpus.pkl", "wb") as f:
    pickle.dump(corpus, f)

# Supression de la variable "corpus"
del corpus

# Ouverture du fichier, puis lecture avec pickle
with open("corpus.pkl", "rb") as f:
    corpus = pickle.load(f)

# La variable est réapparue
# print(corpus)
