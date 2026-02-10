import re

INSTRUCTION_PATTERN = re.compile(r"\s*[0-9a-fA-F]+:\s+")


def is_instruction_line(line: str) -> bool:
    """
    Check whether a line is a valid objdump instruction line.
    """
    return bool(INSTRUCTION_PATTERN.match(line))
