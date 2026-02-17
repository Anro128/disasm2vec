import unittest
from unittest.mock import patch, MagicMock
from pathlib import Path
import subprocess
from disasm2vec.disassembler import objdump, errors

class TestDisassembler(unittest.TestCase):
    @patch("subprocess.run")
    def test_disassemble_success(self, mock_run):
        binary = "test.bin"
        output = "test.asm"
        
        mock_run.return_value.stdout = "start:\n\tmov %eax, %ebx\n"
        
        with patch("pathlib.Path.exists", return_value=True), \
             patch("pathlib.Path.mkdir"), \
             patch("pathlib.Path.write_text") as mock_write:
            
            objdump.disassemble(binary, output)
            
            mock_run.assert_called_once()
            args = mock_run.call_args[0][0]
            self.assertEqual(args[0], "objdump")
            self.assertIn("-d", args)
            self.assertIn(binary, args)
            mock_write.assert_called_once()

    def test_filter_builtin_functions(self):
        asm_input = """
0000000000001149 <main>:
    1149:	f3 0f 1e fa          	endbr64 
    114d:	55                   	push   %rbp

0000000000001030 <printf@plt>:
    1030:	f3 0f 1e fa          	endbr64 
    1034:	f2 ff 25 9d 2f 00 00 	bnd jmp *0x2f9d(%rip)        # 3fd8 <printf@GLIBC_2.2.5>

0000000000001000 <_start>:
    1000:	f3 0f 1e fa          	endbr64
"""
        expected = """
0000000000001149 <main>:
    1149:	f3 0f 1e fa          	endbr64 
    114d:	55                   	push   %rbp

"""
        filtered = objdump._filter_builtin_functions(asm_input).strip()
        self.assertIn("<main>:", filtered)
        self.assertNotIn("<printf@plt>:", filtered)
        self.assertNotIn("<_start>:", filtered)

    @patch("subprocess.run")
    def test_disassembly_error(self, mock_run):
        mock_run.side_effect = subprocess.CalledProcessError(1, ["objdump"], stderr="error")
        
        with patch("pathlib.Path.exists", return_value=True), \
             patch("pathlib.Path.mkdir"):
            with self.assertRaises(errors.DisassemblyError):
                objdump.disassemble("test.bin", "test.asm")

    @patch("disasm2vec.disassembler.objdump.disassemble")
    @patch("pathlib.Path.iterdir")
    @patch("pathlib.Path.mkdir")
    def test_disassemble_folder(self, mock_mkdir, mock_iterdir, mock_disassemble):
        mock_iterdir.return_value = [Path("bin/a"), Path("bin/b")]
        
        with patch("pathlib.Path.exists", return_value=True), \
             patch("pathlib.Path.is_file", return_value=True):
                 
            objdump.disassemble_folder("bin", "asm")
            
        self.assertEqual(mock_disassemble.call_count, 2)

if __name__ == '__main__':
    unittest.main()
