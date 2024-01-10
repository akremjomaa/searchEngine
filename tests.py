import unittest

if __name__ == "__main__":
    loader = unittest.TestLoader()
    start_dir = "tests"
    suite = loader.discover(start_dir, pattern="test_*.py")
    runner = unittest.TextTestRunner()
    runner.run(suite)
