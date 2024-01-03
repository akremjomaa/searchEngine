from .Author import Author
from .decorators import singleton
import re
import pandas as pd
from collections import Counter


class Corpus:
    def __init__(self, nom):
        self.nom = nom
        self.authors = {}
        self.id2aut = {}
        self.id2doc = {}
        self.ndoc = 0
        self.naut = 0
        self.concatenated_text = None
        self.vocabulary = set()
        self.word_frequencies = None

    def add(self, doc):
        if doc.auteur not in self.id2aut:
            self.naut += 1
            self.authors[self.naut] = Author(doc.auteur)
            self.id2aut[doc.auteur] = self.naut

        self.authors[self.id2aut[doc.auteur]].add(doc.texte)
        self.ndoc += 1
        self.id2doc[self.ndoc] = doc
        self.update_vocabulary(doc.texte)

    def show(self, ndocs=-1, tri="titre"):
        docs = list(self.id2doc.values())
        if tri == "titre":
            docs = list(sorted(docs, key=lambda doc: doc.titre))[:ndocs]
        if tri == "date":
            docs = list(sorted(docs, key=lambda doc: doc.date))[:ndocs]
        print(
            f"Title: {doc.titre}\nAuthor: {doc.auteur}\nDate: {doc.date}\nURL: {doc.url}\nText: {doc.texte}\n\n"
            for doc in docs
        )

    def update_concatenated_text(self):
        if self.concatenated_text is None:
            self.concatenated_text = "".join(
                [doc.texte for doc in self.id2doc.values()]
            )

    def search(self, keyword, context_length=30):
        self.update_concatenated_text()

        matches = list(
            re.finditer(
                rf"\b{re.escape(keyword)}\b", self.concatenated_text, re.IGNORECASE
            )
        )
        print(
            f"Number of passages containing the keyword '{keyword}': {len(matches)}\n"
        )
        print("Passages containing the keyword:\n")

        for match in matches:
            start_pos = max(0, match.start() - context_length)
            end_pos = min(len(self.concatenated_text), match.end() + context_length)
            passage = self.concatenated_text[start_pos:end_pos]
            print(f"{passage}\n")

        return

    def concorde(self, motif, taill=(20, 20)):
        if self.concatenated_text is None:
            self.update_concatenated_text()
        matches = re.finditer(motif, self.concatenated_text)
        concordance_data = []

        for match in matches:
            start_index = max(0, match.start() - taill[0])
            end_index = min(len(self.concatenated_text), match.end() + taill[1])
            left_context = self.concatenated_text[start_index : match.start()]
            right_context = self.concatenated_text[match.end() : end_index]
            concordance_data.append((left_context, match.group(), right_context))

        df = pd.DataFrame(
            concordance_data,
            columns=["Context left", "Pattern found", "Right context"],
        )

        return df

    def nettoyer_texte(self, texte):
        texte = texte.lower()
        texte = re.sub(r"\n", " ", texte)
        texte = re.sub(r"[^\w\s]", "", texte)
        return texte

    def stats(self, top_n=10):
        self.update_concatenated_text()
        cleaned_text = self.nettoyer_texte(self.concatenated_text)
        mots = cleaned_text.split()
        nb_mots_differents = len(set(mots))
        print(f"Number of different words in the corpus : {nb_mots_differents}\n")
        mots_frequents = Counter(mots).most_common(top_n)
        print(f"{top_n} most frequent words in the corpus :")
        for mot, occurences in mots_frequents:
            print(f"{mot}: {occurences} occurrences")

    def update_vocabulary(self, text):
        words = re.split(r'\s+|[.,;\'"!?()]', text)
        words = [word for word in words if word != ""]
        words = [word for word in words if word.isalpha()]
        words = [word.lower() for word in words]
        self.vocabulary.update(words)

    def get_vocabulary_stats(self):
        print(f"Number of words in the vocabulary: {len(self.vocabulary)}\n")
        print("Words in the vocabulary:\n")
        print(self.vocabulary)

    def update_word_frequencies(self):
        self.update_concatenated_text()
        cleaned_text = self.nettoyer_texte(self.concatenated_text)
        words = re.split(r'\s+|[.,;\'"!?()]', cleaned_text)
        words = [word for word in words if word != ""]
        words = [word for word in words if word.isalpha()]
        words = [word.lower() for word in words]
        self.word_frequencies = Counter(words)

        doc_word_freq = Counter()
        for doc in self.id2doc.values():
            doc_text = self.nettoyer_texte(doc.texte)
            doc_words = set(re.split(r'\s+|[.,;\'"!?()]', doc_text))
            doc_words = {word.lower() for word in doc_words if word.isalpha()}
            doc_word_freq.update(doc_words)

        for word, freq in self.word_frequencies.items():
            self.word_frequencies[word] = {
                "term_frequency": freq,
                "document_frequency": doc_word_freq[word],
            }

    def get_word_frequencies(self):
        if self.word_frequencies is None:
            self.update_word_frequencies()

        df = pd.DataFrame(
            list(self.word_frequencies.items()), columns=["Word", "Frequencies"]
        )
        df[["Term Frequency", "Document Frequency"]] = pd.DataFrame(
            df["Frequencies"].tolist(), index=df.index
        )
        df.drop(columns=["Frequencies"], inplace=True)
        return df

    def __repr__(self):
        docs = list(self.id2doc.values())
        docs = list(sorted(docs, key=lambda x: x.titre))

        return "\n".join(list(map(str, docs)))
