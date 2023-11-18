class Document:
    def __init__(self, titre, auteur, date, url, texte):
        self.titre = titre
        self.auteur = auteur
        self.date = date
        self.url = url
        self.texte = texte

    def __repr__(self):
        return f"le titre : {self.titre}\t l'auteur : {self.auteur}\t la date : {self.date}\t l'URL : {self.url}\t le texte : {self.texte}\t"

    def __str__(self):
        return f"le post :{self.titre}, crée par {self.auteur}"
