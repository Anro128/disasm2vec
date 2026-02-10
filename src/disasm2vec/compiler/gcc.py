import subprocess
from pathlib import Path
from .errors import CompilationError

def compile_c(
    source: str,
    output: str,
    flags: list[str] | None = None
):
    """
    Compile C source file using gcc.
    """
    _compile(
        compiler="gcc",
        source=source,
        output=output,
        flags=flags,
    )


def compile_cpp(
    source: str,
    output: str,
    flags: list[str] | None = None
):
    """
    Compile C++ source file using g++.
    """
    _compile(
        compiler="g++",
        source=source,
        output=output,
        flags=flags,
    )


def _compile(
    compiler: str,
    source: str,
    output: str,
    flags: list[str] | None = None,
):
    source = Path(source)
    output = Path(output)

    if not source.exists():
        raise FileNotFoundError(source)

    cmd = [
        compiler,
        str(source),
        "-o",
        str(output),
    ]

    if flags:
        cmd.extend(flags)

    try:
        subprocess.run(
            cmd,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
    except subprocess.CalledProcessError as e:
        raise CompilationError(
            f"Compilation failed for {source}:\n{e.stderr}"
        ) from e


def compile_folder(
    src_dir: str,
    out_dir: str,
    optimize: str = "-O0",
    extra_flags: list[str] | None = None,
):
    """
    Compile all .c and .cpp files in a folder (recursively).
    """
    src_dir = Path(src_dir)
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    extra_flags = extra_flags or []

    sources = list(src_dir.rglob("*.c")) + list(src_dir.rglob("*.cpp"))

    if not sources:
        raise ValueError(f"No C/C++ files found in {src_dir}")

    for src in sources:
        output = out_dir / src.stem
        flags = [optimize, *extra_flags]

        try:
            if src.suffix == ".c":
                compile_c(src, output, flags)
            else:
                compile_cpp(src, output, flags)

        except CompilationError as e:
            raise CompilationError(
                f"Compilation failed for {src}:\n{e}"
            ) from e
