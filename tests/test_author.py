import unittest
from models.Author import Author

print("[INFO] [TESTING] Running unit tests for Author.py...")


class TestAuthor(unittest.TestCase):
    def setUp(self):
        self.author = Author("John Doe")

    def test_initialization(self):
        self.assertEqual(self.author.name, "John Doe")
        self.assertEqual(self.author.ndoc, 0)
        self.assertEqual(self.author.production, [])

    def test_add_production(self):
        self.author.add("Production 1")
        self.assertEqual(self.author.ndoc, 1)
        self.assertIn("Production 1", self.author.production)
        self.author.add("Production 2")
        self.assertEqual(self.author.ndoc, 2)
        self.assertIn("Production 2", self.author.production)

    def test_str_representation(self):
        expected_string = "Auteur : John Doe \t nombre de productions publiées : 0"
        self.assertEqual(str(self.author), expected_string)
        self.author.add("Production 1")
        updated_string = "Auteur : John Doe \t nombre de productions publiées : 1"
        self.assertEqual(str(self.author), updated_string)


if __name__ == "__main__":
    unittest.main()
