import unittest
from models.Corpus import Corpus
from models.decorators import singleton
from models.Author import Author
from models.Document import Document
from models.document_factory import DocumentFactory
from datetime import datetime

print("[INFO] [TESTING] Running unit tests for Corpus.py...")


class TestCorpusSingleton(unittest.TestCase):
    def setUp(self):
        self.corpus = Corpus("TestCorpus")

    def test_singleton_instance(self):
        other_corpus = Corpus("other_corpus")
        self.assertEqual(self.corpus, other_corpus)
        self.assertEqual(id(self.corpus), id(other_corpus))
        self.corpus.set_name("new_name")
        self.assertEqual(self.corpus.get_name(), "new_name")


class TestCorpusAddition(unittest.TestCase):
    def setUp(self):
        self.corpus = Corpus("TestCorpus")
        self.author = Author("John Doe")
        self.current_date = datetime.now()
        self.doc = DocumentFactory.create_document(
            "Reddit",
            "titre",
            self.author,
            self.current_date,
            "https://reddit.com",
            "testing",
        )

    def test_add_document(self):
        self.corpus.add(self.doc)
        self.assertEqual(self.corpus.ndoc, 1)
        self.assertIn(self.doc, self.corpus.id2doc.values())
        self.assertEqual(self.corpus.naut, 1)
        self.assertEqual(self.corpus.ndoc, 1)
        self.assertEqual(self.corpus.id2aut[self.author], 1)

    def test_update_vocabulary(self):
        self.assertIn("testing", self.corpus.vocabulary)
        self.assertEqual(self.corpus.vocab["testing"]["id"], 1)
        self.assertEqual(self.corpus.vocab["testing"]["total_occurences"], 1)
        self.assertEqual(self.corpus.vocab["testing"]["documents_occurences"], 1)

    def test_search(self):
        results = self.corpus.search("testing")
        self.assertIn("testing", results)
        self.assertNotIn("testing.", results)

    def test_concorde(self):
        df = self.corpus.concorde("testing")
        self.assertTrue("testing" in df["Pattern found"].values)
        self.assertFalse("testing." in df["Pattern found"].values)

    def test_update_word_frequencies(self):
        doc2 = DocumentFactory.create_document(
            "Reddit",
            "titre",
            self.author,
            self.current_date,
            "https://reddit.com",
            "testing",
        )
        self.corpus.add(doc2)
        self.corpus.update_word_frequencies()
        self.assertEqual(self.corpus.word_frequencies["testing"]["term_frequency"], 1)
        self.assertEqual(
            self.corpus.word_frequencies["testing"]["document_frequency"], 2
        )


if __name__ == "__main__":
    unittest.main()
