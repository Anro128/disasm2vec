# disasm2vec

**disasm2vec** is a research framework designed to generate vector representations from disassembled C/C++ binaries. It provides a modular pipeline that handles compilation, disassembly, tokenization, and vectorization, enabling researchers and security analysts to transform raw code into machine-learning-ready features.

## Features

- **Automated Compilation**: Seamlessly compiles C and C++ source files using GCC.
- **Disassembly Wrapper**: Extracts assembly instructions using `objdump`, supporting both full and function-specific disassembly.
- **Intelligent Tokenization**: Normalizes and cleans assembly instructions, with options to preserve or abstract register names.
- **Vectorization**: Implements TF-IDF vectorization with a flexible factory pattern for easy model management.
- **End-to-End Pipeline**: Orchestrates the entire process from source code to vector embedding.
- **Extensible Architecture**: Built with abstract base classes to easily support new compilers, disassemblers, or vectorizers.

## Prerequisites

- **Python**: version 3.10 or higher.
- **Operating System**: Linux or Windows Subsystem for Linux (WSL).
- **GCC**: Required for compiling source files.
- **Objdump**: Required for disassembling binaries.

**Note**: The compilation (`gcc`) and disassembly (`objdump`) modules rely on system-level tools typically found in Linux environments. If you are on Windows, please use WSL.

Ensure both `gcc` and `objdump` are installed and available in your system's PATH.

## Installation

Install directly from PyPI:

```bash
pip install disasm2vec
```

Or install from source:

```bash
git clone https://github.com/yourusername/disasm2vec.git
cd disasm2vec
pip install .
```

## Usage

The core of the framework is the `PipelineRunner`, which processes a source file based on a configuration object.

### Basic Example

```python
from disasm2vec.pipeline import PipelineConfig, run_pipeline

# Configure the pipeline
config = PipelineConfig(
    source_file="examples/sample.c",
    build_dir="build",
    asm_dir="asm",
    model_path="models/base_tfidf_asm.pkl"  # Path to pre-trained model or where to save a new one
)

# Run the pipeline
# returns:
#   vector: The vector representation of the source file
#   vectorizer: The fitted vectorizer instance
vector, vectorizer = run_pipeline(config)

print(f"Generated Vector Shape: {vector.shape}")
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.