from Author import Author


class Corpus:
    def __init__(self, nom):
        self.nom = nom
        self.authors = {}
        self.id2aut = {}
        self.id2doc = {}
        self.ndoc = 0
        self.naut = 0

    def add(self, doc):
        if doc.auteur not in self.id2aut:
            self.naut += 1
            self.authors[self.naut] = Author(doc.auteur)
            self.id2aut[doc.auteur] = self.naut

        self.authors[self.id2aut[doc.auteur]].add(doc.texte)
        self.ndoc += 1
        self.id2doc[self.ndoc] = doc

    def show(self, ndocs=-1, tri="titre"):
        docs = list(self.id2doc.values())
        if tri == "titre":
            docs = list(sorted(docs, key=lambda doc: doc.titre))[:ndocs]
        if tri == "date":
            docs = list(sorted(docs, key=lambda doc: doc.date))[:ndocs]
        print("\n".join(list(map(repr, docs))))

    def __repr__(self):
        docs = list(self.id2doc.values())
        docs = list(sorted(docs, key=lambda x: x.titre))

        return "\n".join(list(map(str, docs)))
