import re
from pathlib import Path
from .cleaner import is_instruction_line
from .normalizer import (
    normalize_operand,
    normalize_control_operand,
)

BYTE_PATTERN = re.compile(r"^[0-9a-fA-F]{2}$")
MNEMONIC_PATTERN = re.compile(r"^[a-zA-Z][a-zA-Z0-9]*$")


def parse_instruction(line: str, keep_register: bool = False):
    line = line.split("#", 1)[0]

    if ":" not in line:
        return None

    _, rest = line.split(":", 1)
    tokens = rest.strip().split()

    if not tokens:
        return None

    i = 0
    while i < len(tokens) and BYTE_PATTERN.match(tokens[i]):
        i += 1

    if i >= len(tokens):
        return None

    mnemonic = tokens[i].lower()
    if not MNEMONIC_PATTERN.match(mnemonic):
        return None

    operand_str = " ".join(tokens[i + 1 :]).strip()

    result = [mnemonic]

    if mnemonic == "call":
        result.append("FUNC")
        return result

    if mnemonic.startswith("j"):
        result.append("JMP")
        return result

    if operand_str:
        operands = [op.strip() for op in operand_str.split(",")]
        for op in operands:
            result.append(
                normalize_operand(op, keep_register=keep_register)
            )

    return result

def parse_file(path: str, keep_register: bool = False) -> list[str]:
    path = Path(path)
    corpus = []

    with path.open() as f:
        for line in f:
            if not is_instruction_line(line):
                continue

            tokens = parse_instruction(
                line,
                keep_register=keep_register,
            )
            if tokens:
                corpus.append(" ".join(tokens))

    return corpus

def parse_folder(
    asm_dir: str,
    keep_register: bool = False,
) -> dict[str, list[str]]:
    """
    Parse all .asm files in a folder and keep results per file.

    Returns
    -------
    dict[str, list[str]]
        {
            "file.asm": ["mov REG REG", "call FUNC", ...],
            ...
        }
    """
    asm_dir = Path(asm_dir)

    if not asm_dir.exists():
        raise FileNotFoundError(asm_dir)

    asm_files = sorted(asm_dir.glob("*.asm"))

    if not asm_files:
        raise ValueError(f"No .asm files found in {asm_dir}")

    result: dict[str, list[str]] = {}

    for asm_file in asm_files:
        result[asm_file.name] = parse_file(
            asm_file,
            keep_register=keep_register,
        )

    return result
