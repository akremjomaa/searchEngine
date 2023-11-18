import praw

reddit = praw.Reddit(
    client_id="UKtZgFhv6izOz1HVZYi4iQ",
    client_secret="DKMUyLlfc-6pjWK2XE4fNSN6O7C5nA",
    user_agent="Test App",
)
# les champs de post de l'api Reddit

# title: Titre de la publication.
# score: Score de la publication.
# author: Auteur de la publication.
# created_utc: Date de création de la publication (en temps universel coordonné).
# num_comments: Nombre de commentaires.
# selftext: Contenu textuel de la publication (pour les textes de type "self").
# url: URL de la publication.

docs = []
textes_Reddit = []
textes_Arxiv = []

# extract Covid-19 data from Reddit API

hot_posts = reddit.subreddit("Coronavirus").hot(limit=100)
for post in hot_posts:
    # get the specific data that i need
    text = post.title
    text = text.replace("\n", " ")
    textes_Reddit.append(text)


import urllib, urllib.request
import xmltodict

# extract Covid-19 data from arxiv API
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

for doc in docs:
    text = doc["title"] + "." + doc["summary"]
    text = text.replace("\n", " ")
    textes_Arxiv.append(text)

import pandas as pd

# create id list
identifiants = list(range(0, len(textes_Reddit) + len(textes_Arxiv)))

# create origin list
origines = ["Reddit"] * len(textes_Reddit) + ["Arxiv"] * len(textes_Arxiv)
corpus = textes_Reddit + textes_Arxiv
# create our dataFrame
corpusDataFrame = pd.DataFrame({"id": identifiants, "text": corpus, "origin": origines})
# transfom our dataFrame to csv file

# corpusDataFrame.to_csv("td3/myData.csv", sep="\t", index=False)

# get the dataFrame from the csv instead of calling APIS each time

# corpusDataFrame = pd.read_csv("td3/myData.csv")
# print(corpusDataFrame)

print("Longueur du corpus : " + str(len(corpus)))
import pickle

with open("out.pkl", "wb") as f:
    pickle.dump(corpusDataFrame, f)
with open("out.pkl", "rb") as f:
    corpusLoaded = pickle.load(f)

corpusPlus100 = [doc for doc in corpusLoaded["text"] if len(doc) > 100]

print("Longueur du corpus filtré : " + str(len(corpusPlus100)))
for doc in corpusPlus100:
    print("Nombre de phrases : " + str(len(doc.split("."))))
    print("Nombre de mots : " + str(len(doc.split(" "))))
uniqueChain = " ".join(corpusPlus100)
print(uniqueChain)
