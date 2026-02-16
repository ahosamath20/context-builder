from __future__ import annotations

from pathlib import Path

from context_builder.config import Config

CFG = Config()


def project_root() -> Path:
    # Wherever you run the command from = project root
    return Path.cwd()


def init_files() -> Path:
    root = project_root()
    input_path = root / CFG.input_filename
    if not input_path.exists():
        input_path.write_text(
            "# Paste ABSOLUTE file paths, one per line.\n"
            "# Lines starting with # are ignored.\n"
            "# Example:\n"
            "# C:\\Projects\\MyApp\\src\\main.py\n",
            encoding="utf-8",
        )
    return input_path


def _read_input_paths(input_path: Path) -> list[Path]:
    lines = input_path.read_text(encoding="utf-8").splitlines()
    out: list[Path] = []
    seen: set[str] = set()

    for raw in lines:
        s = raw.strip()
        if not s or s.startswith("#"):
            continue

        p = Path(s)

        # absolute paths only (your rule)
        if not p.is_absolute():
            raise ValueError(f"Not an absolute path: {s}")

        key = str(p).lower()
        if key in seen:
            continue
        seen.add(key)
        out.append(p)

    return out


def build_output() -> Path:
    root = project_root()
    input_path = root / CFG.input_filename
    if not input_path.exists():
        raise FileNotFoundError(
            f"Missing {CFG.input_filename}. Run: context-builder init"
        )

    paths = _read_input_paths(input_path)

    output_path = root / CFG.output_filename
    blocks: list[str] = []
    warnings: list[str] = []

    for p in paths:
        if not p.exists():
            warnings.append(f"[MISSING] {p}")
            continue
        if p.is_dir():
            warnings.append(f"[SKIP DIR] {p}")
            continue

        try:
            size = p.stat().st_size
        except Exception as e:
            warnings.append(f"[STAT ERROR] {p} :: {e}")
            continue

        if size > CFG.max_file_bytes:
            warnings.append(f"[TOO LARGE] {p} ({size} bytes)")
            continue

        try:
            content = p.read_text(encoding="utf-8", errors="replace")
        except Exception as e:
            warnings.append(f"[READ ERROR] {p} :: {e}")
            continue

        header = (
            "================================\n"
            f"FILE: {p.name}\n"
            f"PATH: {p}\n"
            "================================\n\n"
        )

        if CFG.wrap_code_block:
            body = f"```text\n{content.rstrip()}\n```\n"
        else:
            body = content.rstrip() + "\n"

        blocks.append(header + body)

    final_text = ""
    if warnings:
        final_text += "######## WARNINGS ########\n"
        final_text += "\n".join(warnings) + "\n"
        final_text += "##########################\n\n"

    final_text += "\n\n".join(blocks).rstrip() + "\n"

    output_path.write_text(final_text, encoding="utf-8")
    return output_path


def check_inputs() -> tuple[bool, list[str]]:
    root = project_root()
    input_path = root / CFG.input_filename
    if not input_path.exists():
        return False, [f"[MISSING INPUT] {input_path} (run: context-builder init)"]

    try:
        paths = _read_input_paths(input_path)
    except Exception as e:
        return False, [f"[INVALID INPUT] {e}"]

    warnings: list[str] = []
    for p in paths:
        if not p.exists():
            warnings.append(f"[MISSING] {p}")
            continue
        if p.is_dir():
            warnings.append(f"[SKIP DIR] {p}")
            continue
        try:
            size = p.stat().st_size
        except Exception as e:
            warnings.append(f"[STAT ERROR] {p} :: {e}")
            continue
        if size > CFG.max_file_bytes:
            warnings.append(f"[TOO LARGE] {p} ({size} bytes)")
            continue

    ok = len(warnings) == 0
    return ok, warnings

