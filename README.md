# context-builder

A simple CLI tool to build a single text context file from absolute file paths.

This helps you quickly collect code from multiple files into one output file for analysis, sharing, or AI workflows.

---

## Installation

### Local development (recommended)

```bash
pip install -e .
```

## Usage

### 1) Initialize input file

```bash
context-builder init
```

This creates:

```
context_files.txt
```

Add absolute paths (one per line), for example:

```
C:\Projects\MyApp\src\main.py
C:\Projects\MyApp\src\service.py
```

Lines starting with `#` are ignored.

### 2) Build context output

```bash
context-builder build
```

This creates:

```
context_output.txt
```

## Output Format

Each file is written like:

```
================================
FILE: main.py
PATH: C:\Projects\MyApp\src\main.py
================================

[file content here]
```

Warnings appear at the top if files are missing or invalid.

## Features

- Absolute paths only
- Duplicate path removal
- UTF-8 safe reading (`errors="replace"`)
- File size safety limit
- Clean output formatting
- Simple CLI workflow

## Project Structure

```
context_builder/
├── __init__.py
├── cli.py
├── config.py
└── core.py
```

## Commands

```bash
context-builder init
context-builder build
context-builder --version
```

## Version

Current version: 0.1.0

## License

MIT