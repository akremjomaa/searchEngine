import unittest
from models.Document import Document, RedditDocument, ArxivDocument
from models.document_factory import DocumentFactory
from models.decorators import singleton

print(
    "[INFO] [TESTING] Running unit tests for Document.py..."
)


class TestDocument(unittest.TestCase):
    def test_document_creation(self):
        doc = Document("Title", "Author", "Date", "URL", "Text")
        self.assertEqual(doc.titre, "Title")


class TestRedditDocument(unittest.TestCase):
    def test_reddit_document_creation(self):
        reddit_doc = RedditDocument("Title", "Author", "Date", "URL", "Text", 10, 100)
        self.assertEqual(reddit_doc.getCommentNb(), 10)
        self.assertEqual(reddit_doc.getVoteNb(), 100)


class TestArxivDocument(unittest.TestCase):
    def test_arxiv_document_creation(self):
        arxiv_doc = ArxivDocument("Title", "CoAuthor", "Date", "URL", "Text")
        self.assertEqual(arxiv_doc.getType(), "Arxiv")


class TestDocumentFactory(unittest.TestCase):
    def test_create_reddit_document(self):
        doc = DocumentFactory.create_document(
            "Reddit", "Title", "Author", "Date", "URL", "Text", 10, 100
        )
        self.assertIsInstance(doc, RedditDocument)

    def test_create_arxiv_document(self):
        doc = DocumentFactory.create_document(
            "Arxiv", "Title", "Author", "Date", "URL", "Text"
        )
        self.assertIsInstance(doc, ArxivDocument)

    def test_create_invalid_document(self):
        with self.assertRaises(ValueError):
            DocumentFactory.create_document(
                "InvalidType", "Title", "Author", "Date", "URL", "Text"
            )


if __name__ == "__main__":
    unittest.main()
