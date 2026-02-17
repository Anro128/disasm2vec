import unittest
from unittest.mock import patch, MagicMock
from pathlib import Path
import subprocess
from disasm2vec.compiler import gcc, errors

class TestCompiler(unittest.TestCase):
    @patch("subprocess.run")
    def test_compile_c_success(self, mock_run):
        source = "test.c"
        output = "test"
        
        with patch("pathlib.Path.exists", return_value=True):
            gcc.compile_c(source, output)
            
        mock_run.assert_called_once()
        args = mock_run.call_args[0][0]
        self.assertEqual(args[0], "gcc")
        self.assertIn(source, args)
        self.assertIn("-o", args)
        self.assertIn(output, args)

    @patch("subprocess.run")
    def test_compile_cpp_success(self, mock_run):
        source = "test.cpp"
        output = "test"
        
        with patch("pathlib.Path.exists", return_value=True):
            gcc.compile_cpp(source, output)
            
        mock_run.assert_called_once()
        args = mock_run.call_args[0][0]
        self.assertEqual(args[0], "g++")
        self.assertIn(source, args)

    def test_compile_file_not_found(self):
        with patch("pathlib.Path.exists", return_value=False):
            with self.assertRaises(FileNotFoundError):
                gcc.compile_c("nonexistent.c", "output")

    @patch("subprocess.run")
    def test_compile_error(self, mock_run):
        mock_run.side_effect = subprocess.CalledProcessError(1, ["gcc"], stderr="error")
        
        with patch("pathlib.Path.exists", return_value=True):
            with self.assertRaises(errors.CompilationError):
                gcc.compile_c("test.c", "test")

    @patch("subprocess.run")
    @patch("pathlib.Path.rglob")
    @patch("pathlib.Path.mkdir")
    def test_compile_folder(self, mock_mkdir, mock_rglob, mock_run):
        mock_rglob.side_effect = [
            [Path("src/a.c")], 
            [Path("src/b.cpp")] 
        ]
        
        with patch("pathlib.Path.exists", return_value=True):
            gcc.compile_folder("src", "out")
            
        self.assertEqual(mock_run.call_count, 2)
        
        # Verify gcc called for .c
        call1 = mock_run.call_args_list[0][0][0]
        self.assertEqual(call1[0], "gcc")
        
        # Verify g++ called for .cpp
        call2 = mock_run.call_args_list[1][0][0]
        self.assertEqual(call2[0], "g++")

if __name__ == '__main__':
    unittest.main()
