import main
from src.constants import Labels
import unittest

class TestMain(unittest.TestCase):
    def setUp(self):
        pass

    def test_latest(self):
        main.latest()

    def test_latest_update(self):
        main.latest_update()

    def test_train(self):
        main.train()

    def test_suggestions(self):
        main.suggestions()

    def test_sync(self):
        pass

    def test_search_negative(self):
        main.search_keywords("cnn")
        main.annotate("search", [1], Labels.NEGATIVE)

    def test_search_show(self):
        main.search_keywords("federated")
        main.show("search", [0,1,2])

if __name__ == "__main__":
    unittest.main()
