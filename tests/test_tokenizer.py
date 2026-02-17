import unittest
from disasm2vec.tokenizer import core, cleaner, normalizer

class TestTokenizer(unittest.TestCase):
    def test_is_instruction_line(self):
        self.assertTrue(cleaner.is_instruction_line("    1149:	f3 0f 1e fa          	endbr64 "))
        self.assertFalse(cleaner.is_instruction_line("0000000000001149 <main>:"))
        self.assertFalse(cleaner.is_instruction_line(""))

    def test_normalize_operand(self):
        self.assertEqual(normalizer.normalize_operand("%eax", keep_register=False), "REG")
        self.assertEqual(normalizer.normalize_operand("%eax", keep_register=True), "eax")
        
        self.assertEqual(normalizer.normalize_operand("$10"), "IMM")
        self.assertEqual(normalizer.normalize_operand("$0x10"), "MEM")
        
        self.assertEqual(normalizer.normalize_operand("0x10"), "MEM")
        self.assertEqual(normalizer.normalize_operand("(%rax)"), "MEM")
        self.assertEqual(normalizer.normalize_operand("-0x10(%rbp)"), "MEM")
        
        self.assertEqual(normalizer.normalize_operand("<main>"), "")

    def test_tokenize_instruction(self):
        # Normal instruction
        line = "    1149:	f3 0f 1e fa          	endbr64 "
        tokens = core.tokenize_instruction(line)
        self.assertEqual(tokens, ["endbr64"])
        
        # Instruction with operands
        line = "    114d:	55                   	push   %rbp"
        tokens = core.tokenize_instruction(line)
        self.assertEqual(tokens, ["push", "REG"])
        
        # Instruction with multiple operands
        line = "    1150:	48 89 e5             	mov    %rsp,%rbp"
        tokens = core.tokenize_instruction(line)
        self.assertEqual(tokens, ["mov", "REG", "REG"])
        
        # Func call
        line = "    1160:	e8 eb fe ff ff       	call   1050 <_start>"
        tokens = core.tokenize_instruction(line)
        self.assertEqual(tokens, ["call", "FUNC"])
        
        # Jump
        line = "    1165:	eb fe                	jmp    1165 <main+0x1c>"
        tokens = core.tokenize_instruction(line)
        self.assertEqual(tokens, ["jmp", "JMP"])

    def test_tokenize_invalid_lines(self):
        self.assertIsNone(core.tokenize_instruction("invalid line"))
        self.assertIsNone(core.tokenize_instruction("    1149: ")) 

if __name__ == '__main__':
    unittest.main()
