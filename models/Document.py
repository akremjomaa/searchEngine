import itertools
class Document:
    object_id = itertools.count()

    def __init__(self, titre, auteur, date, url, texte, type=""):
        self.id = next(Document.object_id)
        self.titre = titre
        self.auteur = auteur
        self.date = date
        self.url = url
        self.texte = texte
        self.type = type

    def __repr__(self):
        return f"le titre : {self.titre}\t l'auteur : {self.auteur}\t la date : {self.date}\t l'URL : {self.url}\t le texte : {self.texte}\t"

    def __str__(self):
        return f"le post :{self.titre}, crée par {self.auteur}"

    def getType(self):
        pass


class RedditDocument(Document):
    def __init__(self, titre, auteur, date, url, texte, commentNb=0, voteNb=0, type=""):
        Document.__init__(
            self, titre=titre, auteur=auteur, date=date, url=url, texte=texte, type=type
        )
        self.__commentNb = commentNb
        self.__voteNb = voteNb

    def __str__(self):
        return f"le post :{self.titre}, crée par {self.auteur} , a un score = {self.__voteNb} et {self.__commentNb} commentaires"

    def getCommentNb(self):
        return self.__commentNb

    def setCommentNb(self, commentNb):
        self.__commentNb = commentNb

    def getVoteNb(self):
        return self.__voteNb

    def setVoteNb(self, voteNb):
        self.__voteNb = voteNb

    def getType(self):
        return "Reddit"


class ArxivDocument(Document):
    def __init__(self, titre, coAuteur, date, url, texte, type=""):
        Document.__init__(
            self,
            titre=titre,
            auteur=coAuteur,
            date=date,
            url=url,
            texte=texte,
            type=type,
        )

    def __str__(self):
        return f"le post :{self.titre}, crée par plusieurs auteurs qui sont : {self.auteur}"

    def getType(self):
        return "Arxiv"
