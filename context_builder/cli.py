from __future__ import annotations

import argparse
import sys

from context_builder import __version__
from context_builder.core import build_output, check_inputs, init_files


def main() -> None:
    parser = argparse.ArgumentParser(prog="context-builder")
    parser.add_argument("--version", action="version", version=__version__)

    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("init", help="Create context_files.txt")
    sub.add_parser("check", help="Validate context_files.txt and exit non-zero on problems")
    sub.add_parser("build", help="Generate context_output.txt")

    args = parser.parse_args()

    if args.cmd == "init":
        path = init_files()
        print(f"Created: {path}")
        return

    if args.cmd == "check":
        ok, warnings = check_inputs()
        if warnings:
            print("######## CHECK ########")
            print("\n".join(warnings))
            print("#######################")
        sys.exit(0 if ok else 1)

    if args.cmd == "build":
        out = build_output()
        print(f"Wrote: {out}")
        return
