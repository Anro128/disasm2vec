import re

REGISTER_PATTERN = re.compile(r"%([a-zA-Z0-9]+)")
IMMEDIATE_PATTERN = re.compile(r"\$0x[0-9a-fA-F]+|\$\d+")
MEMORY_PATTERN = re.compile(
    r"%[a-z]{2}:|"
    r"\([^)]+\)|"
    r"0x[0-9a-fA-F]+"
)
SYMBOL_PATTERN = re.compile(r"<.*?>")


def normalize_operand(operand: str, keep_register: bool = False) -> str:
    operand = SYMBOL_PATTERN.sub("", operand)

    if MEMORY_PATTERN.search(operand):
        return "MEM"

    if IMMEDIATE_PATTERN.search(operand):
        return "IMM"

    m = REGISTER_PATTERN.search(operand)
    if m:
        return m.group(1).lower() if keep_register else "REG"

    return operand
