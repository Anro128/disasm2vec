from pathlib import Path

from disasm2vec.compiler import compile_c, compile_cpp
from disasm2vec.disassembler import disassemble
from disasm2vec.tokenizer import tokenize
from disasm2vec.vectorizer import vectorize

from .config import PipelineConfig


def run_pipeline(config: PipelineConfig):
    """
    Run pipeline for single source file.

    Flow:
        source -> compile -> disassemble -> tokenizer -> vectorize
    """

    source = Path(config.source_file)

    if not source.exists():
        raise FileNotFoundError(source)

    stem = source.stem

    binary_path = Path(config.build_dir) / stem
    asm_path = Path(config.asm_dir) / f"{stem}.asm"

    binary_path.parent.mkdir(parents=True, exist_ok=True)
    asm_path.parent.mkdir(parents=True, exist_ok=True)

    # COMPILE
    if config.do_compile:
        flags = [config.optimize]
        if config.extra_flags:
            flags.extend(config.extra_flags)

        if source.suffix == ".c":
            compile_c(source, binary_path, flags)

        elif source.suffix == ".cpp":
            compile_cpp(source, binary_path, flags)

        else:
            raise ValueError(
                f"Unsupported source type: {source.suffix}"
            )

    # DISASSEMBLE
    if config.do_disassemble:
        disassemble(
            binary=binary_path,
            output=asm_path,
            arch=config.arch,
            full=config.full_disasm,
        )

    # TOKENIZER
    corpus = tokenize(
        path=asm_path,
        entry=config.entry,
        keep_register=config.keep_register,
    )

    # VECTORIZE
    X, _, vectorizer = vectorize([corpus])

    return X, vectorizer
