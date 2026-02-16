from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Config:
    input_filename: str = "context_files.txt"
    output_filename: str = "context_output.txt"
    wrap_code_block: bool = True
    max_file_bytes: int = 2_000_000  # 2 MB safety limit
