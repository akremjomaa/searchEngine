import re
import pandas as pd
from .Author import Author
from .decorators import singleton
from collections import Counter
import string


class Corpus:
    def __init__(self, nom):
        self.nom = nom
        self.authors = {}
        self.id2aut = {}
        self.id2doc = {}
        self.ndoc = 0
        self.naut = 0
        self.full_text = ""

    def add(self, doc):
        if doc.auteur not in self.id2aut:
            self.naut += 1
            self.authors[self.naut] = Author(doc.auteur)
            self.id2aut[doc.auteur] = self.naut

        self.authors[self.id2aut[doc.auteur]].add(doc.texte)
        self.ndoc += 1
        self.id2doc[self.ndoc] = doc
        self.full_text += " " + doc.texte

    #################################################TD5#################################################
    def search(self, mot_clef):
        matches = re.finditer(mot_clef, self.full_text)
        passages = []

        for match in matches:
            passages.append(match.group())

        return passages

    def concorde(self, motif, contexte_gauche=20, contexte_droit=20):
        matches = re.finditer(motif, self.full_text)
        concordance_data = []

        for match in matches:
            start_index = max(0, match.start() - contexte_gauche)
            end_index = min(len(self.full_text), match.end() + contexte_droit)
            left_context = self.full_text[start_index : match.start()]
            right_context = self.full_text[match.end() : end_index]
            concordance_data.append((left_context, match.group(), right_context))

        df = pd.DataFrame(
            concordance_data,
            columns=["Contexte gauche", "Motif trouvé", "Contexte droit"],
        )
        return df

    def nettoyer_texte(self, texte):
        texte = texte.lower()
        texte = re.sub(r"\n", " ", texte)
        # texte = re.sub(r'[^a-z]', '', texte) # supprime les caractères non alphabétiques mais aussi les caractères accentués !
        texte = re.sub(
            r"[^\w]", "", texte
        )  # supprime les caractères non alphanumériques et conserve les caractères accentués
        return texte

    def stats(self, n_mots_frequents=10):
        texte_nettoye = self.nettoyer_texte(self.full_text)
        mots = texte_nettoye.split()
        nb_mots_differents = len(set(mots))
        print(f"Nombre de mots différents dans le corpus : {nb_mots_differents}")
        mots_frequents = Counter(mots).most_common(n_mots_frequents)
        print(f"\nLes {n_mots_frequents} mots les plus fréquents :")
        for mot, freq in mots_frequents:
            print(f"{mot.ljust(15)}: {freq} occurrences")

    def construire_vocabulaire(self):
        vocabulaire = set()

        for doc in self.id2doc.values():
            mots = re.split(r"\s+|[" + re.escape(string.punctuation) + "]", doc.texte)
            vocabulaire.update(mots)

        return vocabulaire

    def afficher_vocabulaire(self):
        print("Vocabulaire du corpus:")
        print(v for v in self.construire_vocabulaire())

    def construire_tableau_frequences(self):
        texte_complet = " ".join(doc.texte for doc in self.id2doc.values())
        texte_nettoye = self.nettoyer_texte(texte_complet)
        mots = texte_nettoye.split()
        freq_mots = Counter(mots)
        doc_freq_dict = {mot: 0 for mot in freq_mots.keys()}

        for doc in self.id2doc.values():
            mots_du_doc = set(
                re.split(
                    r"\s+|[" + re.escape(string.punctuation) + "]", doc.texte.lower()
                )
            )
            for mot in mots_du_doc:
                if mot in doc_freq_dict:
                    doc_freq_dict[mot] += 1

        df_freq = pd.DataFrame.from_dict(
            freq_mots, orient="index", columns=["Fréquence"]
        )
        df_freq.index.name = "Mot"  # Nommez l'index du DataFrame
        df_freq["Document-Frequency"] = df_freq.index.map(doc_freq_dict)

        return df_freq

    #################################################TD5#################################################

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
