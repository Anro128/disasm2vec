from dataclasses import dataclass
from typing import Optional, Tuple


@dataclass
class PipelineConfig:
    source_file: str

    build_dir: str
    asm_dir: str

    # compiler
    optimize: str = "-O0"
    extra_flags: Optional[list[str]] = None

    # disassembler
    arch: Optional[str] = None
    full_disasm: bool = False

    # preprocess
    entry: str = "main"
    keep_register: bool = False

    # vectorizer
    max_features: Optional[int] = None
    ngram_range: Tuple[int, int] = (1, 2)
    min_df: int = 1

    # switches
    do_compile: bool = True
    do_disassemble: bool = True
