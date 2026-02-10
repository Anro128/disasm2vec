import subprocess
from pathlib import Path
from .errors import DisassemblyError


def disassemble_file(
    binary: str,
    output: str,
    arch: str | None = None,
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
    """
    binary = Path(binary)
    output = Path(output)

    if not binary.exists():
        raise FileNotFoundError(binary)

    output.parent.mkdir(parents=True, exist_ok=True)

    cmd = ["objdump", "-d", str(binary)]

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

    output.write_text(result.stdout)


def disassemble_folder(
    bin_dir: str,
    out_dir: str,
):
    """
    Disassemble all binaries in a folder.

    Parameters
    ----------
    bin_dir : str
        Folder containing compiled binaries
    out_dir : str
        Folder to store .asm outputs
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
            disassemble_file(binary, asm_out)
        except DisassemblyError as e:
            raise DisassemblyError(
                f"Disassembly failed for {binary}:\n{e}"
            ) from e
