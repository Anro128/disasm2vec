import unittest
from unittest.mock import MagicMock, patch
import tempfile
import os
from disasm2vec.vectorizer import tfidf
import pickle

class TestVectorizer(unittest.TestCase):
    def setUp(self):
        self.doc1 = ["mov", "REG", "REG"]
        self.doc2 = ["add", "REG", "IMM"]
        self.documents = [self.doc1, self.doc2]
        
    def test_init(self):
        vectorizer = tfidf.Tfidf(max_features=100)
        self.assertFalse(vectorizer._fitted)
        self.assertEqual(vectorizer.vectorizer.max_features, 100)

    @patch("sklearn.feature_extraction.text.TfidfVectorizer.fit")
    def test_fit(self, mock_fit):
        vectorizer = tfidf.Tfidf()
        vectorizer.fit(self.documents)
        
        mock_fit.assert_called_once_with(self.documents)
        self.assertTrue(vectorizer._fitted)

    @patch("sklearn.feature_extraction.text.TfidfVectorizer.transform")
    def test_transform(self, mock_transform):
        vectorizer = tfidf.Tfidf()
        vectorizer._fitted = True # Manually set fitted
        
        vectorizer.transform(self.documents)
        mock_transform.assert_called_once_with(self.documents)

    def test_transform_not_fitted(self):
        vectorizer = tfidf.Tfidf()
        with self.assertRaises(RuntimeError):
            vectorizer.transform(self.documents)

    def test_validate_docs(self):
        vectorizer = tfidf.Tfidf()
        with self.assertRaises(TypeError):
            vectorizer.fit("invalid docs") # Not iterable
            
        with self.assertRaises(TypeError):
            vectorizer.fit(["invalid doc"]) # Inner not list

    @patch("pickle.dump")
    @patch("builtins.open")
    def test_save(self, mock_open, mock_dump):
        vectorizer = tfidf.Tfidf()
        vectorizer._fitted = True
        
        # Mock open context manager
        mock_file = MagicMock()
        mock_open.return_value.__enter__.return_value = mock_file
        
        vectorizer.save("model.pkl")
        
        mock_open.assert_called_with("model.pkl", "wb")
        mock_dump.assert_called_once()
        self.assertEqual(mock_dump.call_args[0][0], vectorizer.vectorizer)

    @patch("pickle.load")
    @patch("builtins.open")
    def test_load(self, mock_open, mock_load):
        vectorizer = tfidf.Tfidf()
        
        # Mock loaded vectorizer
        mock_loaded_vec = MagicMock()
        mock_load.return_value = mock_loaded_vec
        
        # Mock open context manager
        mock_file = MagicMock()
        mock_open.return_value.__enter__.return_value = mock_file
        
        vectorizer.load("model.pkl")
        
        mock_open.assert_called_with("model.pkl", "rb")
        mock_load.assert_called_once()
        self.assertEqual(vectorizer.vectorizer, mock_loaded_vec)
        self.assertTrue(vectorizer._fitted)

if __name__ == '__main__':
    unittest.main()
