import subprocess
from pathlib import Path
from .errors import DisassemblyError


def disassemble_file(
    binary: str,
    output: str,
    arch: str | None = None,
    full: bool = False,
):
    """
    Disassemble a single binary using objdump.

    Parameters
    ----------
    binary : str
        Path to compiled binary
    output : str
        Output .asm file
    arch : str | None
        Optional architecture (e.g. i386:x86-64)
    full : bool
        If True, disassemble all functions.
        If False, exclude builtin / PLT functions.
    """
    binary = Path(binary)
    output = Path(output)

    if not binary.exists():
        raise FileNotFoundError(binary)

    output.parent.mkdir(parents=True, exist_ok=True)

    # Base command
    cmd = ["objdump", "-d", "--section=.text", str(binary)]

    if arch:
        cmd.extend(["-m", arch])

    try:
        result = subprocess.run(
            cmd,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
    except subprocess.CalledProcessError as e:
        raise DisassemblyError(
            f"objdump failed for {binary}:\n{e.stderr}"
        ) from e

    asm = result.stdout

    if not full:
        asm = _filter_builtin_functions(asm)

    output.write_text(asm)


def disassemble_folder(
    bin_dir: str,
    out_dir: str,
    full: bool = False,
):
    """
    Disassemble all binaries in a folder.

    Parameters
    ----------
    bin_dir : str
        Folder containing compiled binaries
    out_dir : str
        Folder to store .asm outputs
    full : bool
        If True, disassemble all functions.
        If False, exclude builtin / PLT functions.
    """
    bin_dir = Path(bin_dir)
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    binaries = [p for p in bin_dir.iterdir() if p.is_file()]

    if not binaries:
        raise ValueError(f"No binaries found in {bin_dir}")

    for binary in binaries:
        asm_out = out_dir / f"{binary.name}.asm"

        try:
            disassemble_file(binary, asm_out, full=full)
        except DisassemblyError as e:
            raise DisassemblyError(
                f"Disassembly failed for {binary}:\n{e}"
            ) from e


def _filter_builtin_functions(asm: str) -> str:
    """
    Remove builtin / PLT / runtime functions from objdump output.
    """
    filtered_lines = []

    skip = False
    for line in asm.splitlines():
        if "<" in line and ">" in line and line.strip().endswith(":"):
            name = line.split("<")[1].split(">")[0]

            if (
                name.endswith("@plt")
                or name.startswith("_start")
                or name.startswith("frame_dummy")
                or name.startswith("register_tm_clones")
                or name.startswith("deregister_tm_clones")
                or name.startswith("__")
            ):
                skip = True
                continue
            else:
                skip = False

        if not skip:
            filtered_lines.append(line)

    return "\n".join(filtered_lines)
