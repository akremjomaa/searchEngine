from .Author import Author
from .decorators import singleton
import re
import pandas as pd
from collections import Counter
from scipy.sparse import csr_matrix
import numpy as np
import dill
import itertools
import random


def create_new_ref_number():
    return str(random.randint(1000000000, 9999999999))


@singleton
class Corpus:
    def __init__(self, nom):
        self.id = create_new_ref_number()
        self.nom = nom
        self.authors = {}
        self.id2aut = {}
        self.id2doc = {}  # key: id, value: doc
        self.ndoc = 0
        self.naut = 0
        self.concatenated_text = None
        self.vocabulary = set()
        self.word_frequencies = (
            None  # key: word, value: {term_frequency, document_frequency}
        )
        self.vocab = (
            dict()
        )  # key: word, value: {id, total_occurences, documents_occurences}

    def get_name(self):
        return self.nom

    def set_name(self, nom):
        self.nom = nom

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
        passages = []

        for match in matches:
            start_pos = max(0, match.start() - context_length)
            end_pos = min(len(self.concatenated_text), match.end() + context_length)
            passage = self.concatenated_text[start_pos:end_pos]
            passages.append(passage)

        return passages

    def concorde(self, motif, taill=(20, 20)):
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

    ###############################################################

    def update_vocabulary(self, text):
        words = self.prepare_text(text)
        self.vocabulary.update(words)
        self.vocabulary = set(sorted(self.vocabulary))

        for word in words:
            if word not in self.vocab:
                self.vocab[word] = {
                    "id": len(self.vocab) + 1,
                    "total_occurences": 0,
                    "documents_occurences": 0,
                }
            self.vocab[word]["total_occurences"] += 1
            self.vocab[word]["documents_occurences"] += 1

    def get_vocab(self):
        for word, data in self.vocab.items():
            print(f"{word}: {data}")
        print(f"Number of words in the vocabulary: {len(self.vocab)}\n")

    def get_vocabulary_stats(self):
        print(f"Number of words in the vocabulary: {len(self.vocabulary)}\n")
        print("Words in the vocabulary:\n")
        print(self.vocabulary)

    def prepare_text(self, text):
        words = re.split(r'\s+|[.,;\'"!?()]', text)
        words = [word for word in words if word != ""]
        words = [word for word in words if word.isalpha()]
        words = [word.lower() for word in words]
        return words

    def build_term_frequency_matrix(self):
        rows = list()
        cols = list()
        values = list()
        for doc_id, doc in self.id2doc.items():
            words = self.prepare_text(doc.texte)
            wf = Counter(words)
            for w, freq in wf.items():
                if w not in self.vocab:
                    print(f"[ERRER] -- The word | {w} | is not in the vocabulary")
                else:
                    cols.append(
                        self.vocab[w]["id"] - 1
                    )  # -1 because of the index start at 0 and not 1
                    rows.append(doc_id - 1)
                    values.append(freq)

        return csr_matrix(
            (values, (rows, cols)), shape=(len(self.id2doc), len(self.vocab))
        )

    def query_to_new_vector(self, query):
        local_vector = np.zeros(len(self.vocab))

        for w in self.prepare_text(query):
            if w not in self.vocab:
                print(
                    f"[ERRER] -- Errer occured while trying to create the vector for the word | {w} |"
                )
            else:
                dx = (
                    self.vocab[w]["id"] - 1
                )  # get the word id by ajdusting the based-0-indextion
                local_vector[
                    dx
                ] += 1  # increment the value of the vector at the index of the word

        return local_vector

    def calculate_cosine_similarity(self, v1, v2):
        norm_v1 = np.linalg.norm(v1)
        norm_v2 = np.linalg.norm(v2)

        if norm_v1 == 0 or norm_v2 == 0:
            return 0
        return np.dot(v1, v2) / (norm_v1 * norm_v2)

    def search_on_scoring(self, q):
        qv = self.query_to_new_vector(q)  # qv: query vector
        term_frq_mat = self.build_term_frequency_matrix()
        scoring = list()
        for id in self.id2doc.keys():
            dv = term_frq_mat[
                id - 1
            ].toarray()  # converting the sparse mat into a dense mat
            score = self.calculate_cosine_similarity(qv, dv.flatten())
            scoring.append((id, score))
        return scoring

    def rank_after_scoring(self, scores):
        scores = sorted(scores, key=lambda x: x[1], reverse=True)
        scores = [(id, score) for id, score in scores if score > 0]
        return scores

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

    def load_corpus(self):
        with open(f"corpus.pkl", "rb") as f:
            self.__dict__.update(dill.load(f).__dict__)

    def save(self):
        with open(f"corpus.pkl", "wb") as f:
            dill.dump(self, f)

    def __repr__(self):
        docs = list(self.id2doc.values())
        docs = list(sorted(docs, key=lambda x: x.titre))

        return "\n".join(list(map(str, docs)))
