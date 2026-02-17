import unittest
from unittest.mock import MagicMock, patch
from disasm2vec.pipeline import runner, config
from disasm2vec.vectorizer import Tfidf

class TestPipeline(unittest.TestCase):
    @patch("disasm2vec.pipeline.runner.compile_c")
    @patch("disasm2vec.pipeline.runner.disassemble")
    @patch("disasm2vec.pipeline.runner.tokenize")
    @patch("disasm2vec.vectorizer.Tfidf.load")
    @patch("disasm2vec.vectorizer.Tfidf.transform_one")
    def test_run_pipeline_success(self, mock_transform, mock_load, mock_tokenize, mock_disassemble, mock_compile):
        # Setup config
        cfg = config.PipelineConfig(
            source_file="test.c",
            build_dir="build",
            asm_dir="asm",
            model_path="model.pkl"
        )
        
        # Mocks
        mock_tokenize.return_value = ["mov", "eax", "ebx"]
        mock_transform.return_value = "vector"
        
        with patch("pathlib.Path.exists", return_value=True), \
             patch("pathlib.Path.mkdir"):
            
            X, vectorizer = runner.run_pipeline(cfg)
            
            self.assertEqual(X, "vector")
            self.assertIsInstance(vectorizer, Tfidf)
            
            # Verify calls
            mock_compile.assert_called_once()
            mock_disassemble.assert_called_once()
            mock_tokenize.assert_called_once()
            mock_load.assert_called_once_with("model.pkl")
            mock_transform.assert_called_once_with(["mov", "eax", "ebx"])

    def test_missing_model_path(self):
        cfg = config.PipelineConfig(
            source_file="test.c",
            build_dir="build",
            asm_dir="asm",
            model_path=None # Missing model path
        )
        
        with patch("pathlib.Path.exists", return_value=True), \
             patch("pathlib.Path.mkdir"), \
             patch("disasm2vec.pipeline.runner.compile_c"), \
             patch("disasm2vec.pipeline.runner.disassemble"), \
             patch("disasm2vec.pipeline.runner.tokenize"):
                 
            with self.assertRaisesRegex(ValueError, "model_path is required"):
                runner.run_pipeline(cfg)

if __name__ == '__main__':
    unittest.main()
