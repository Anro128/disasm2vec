import re
from pathlib import Path
from .cleaner import is_instruction_line
from .normalizer import normalize_operand


BYTE_PATTERN = re.compile(r"^[0-9a-fA-F]{2}$")
MNEMONIC_PATTERN = re.compile(r"^[a-zA-Z][a-zA-Z0-9]*$")
FUNCTION_HEADER = re.compile(r"<(.+?)>:")


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


def _split_functions(path: Path) -> dict[str, list[str]]:
    functions = {}
    current = None

    with path.open() as f:
        for line in f:
            header = FUNCTION_HEADER.search(line)
            if header:
                current = header.group(1)
                functions[current] = []
                continue

            if current and is_instruction_line(line):
                functions[current].append(line)

    return functions


def _extract_call_target(line: str) -> str | None:
    if "call" not in line:
        return None

    if "<" in line and ">" in line:
        return line.split("<")[1].split(">")[0]

    return None


def _expand_function(
    func_name: str,
    functions: dict[str, list[str]],
    keep_register: bool,
    visited: set,
) -> list[str]:
    """
    Inline user-defined function bodies at call sites.
    """
    if func_name in visited:
        return []

    visited.add(func_name)

    result = []

    for line in functions.get(func_name, []):
        tokens = parse_instruction(
            line,
            keep_register=keep_register,
        )

        if not tokens:
            continue

        if tokens[0] == "call":
            callee = _extract_call_target(line)

            if (
                callee
                and "@plt" not in callee
                and callee in functions
            ):
                result.extend(
                    _expand_function(
                        callee,
                        functions,
                        keep_register,
                        visited,
                    )
                )
                continue

        result.append(" ".join(tokens))

    return result


def parse_file(
    path: str,
    keep_register: bool = False,
    entry: str = "main",
) -> list[str]:
    """
    Parse file and inline user-defined function calls
    inside selected entry function.
    """
    path = Path(path)

    functions = _split_functions(path)

    if entry not in functions:
        raise ValueError(f"Function '{entry}' not found.")

    return _expand_function(
        entry,
        functions,
        keep_register,
        visited=set(),
    )


def parse_folder(
    asm_dir: str,
    keep_register: bool = False,
    entry: str = "main",
) -> dict[str, list[str]]:
    """
    Parse all .asm files in a folder.
    Each file processed independently.
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
            entry=entry,
        )

    return result
