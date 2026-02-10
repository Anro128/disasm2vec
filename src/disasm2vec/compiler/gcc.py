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

    Parameters
    ----------
    source : str
        Path to .c file
    output : str
        Output binary path
    flags : list[str], optional
        Compiler flags (e.g. ["-O0", "-g"])
    """
    _compile(
        compiler="gcc",
        source=source,
        output=output,
        flags=flags
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
        flags=flags
    )


def _compile(
    compiler: str,
    source: str,
    output: str,
    flags: list[str] | None
):
    source = Path(source)
    output = Path(output)

    if not source.exists():
        raise FileNotFoundError(source)

    cmd = [
        compiler,
        str(source),
        "-o",
        str(output)
    ]

    if flags:
        cmd.extend(flags)

    try:
        subprocess.run(
            cmd,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
    except subprocess.CalledProcessError as e:
        raise CompilationError(
            f"Compilation failed:\n{e.stderr}"
        )

def compile_folder(
    src_dir: str,
    out_dir: str,
    optimize: str = "-O0",
    extra_flags: list[str] | None = None
):
    """
    Compile all .c and .cpp files in a folder (recursively).

    Parameters
    ----------
    src_dir : str
        Folder berisi source code C/C++
    out_dir : str
        Folder output binary
    optimize : str
        Optimization flag (-O0, -O2, dll)
    extra_flags : list[str] | None
        Additional gcc/g++ flags
    """
    src_dir = Path(src_dir)
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    extra_flags = extra_flags or []

    sources = list(src_dir.rglob("*.c")) + list(src_dir.rglob("*.cpp"))

    if not sources:
        raise ValueError(f"No C/C++ files found in {src_dir}")

    for src in sources:
        compiler = "gcc" if src.suffix == ".c" else "g++"
        output = out_dir / src.stem

        cmd = [
            compiler,
            str(src),
            "-o",
            str(output),
            optimize,
            *extra_flags
        ]

        print(f"[compile] {' '.join(cmd)}")

        try:
            subprocess.run(
                cmd,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
        except subprocess.CalledProcessError as e:
            raise RuntimeError(
                f"Compilation failed for {src}\n{e.stderr.decode()}"
            )
