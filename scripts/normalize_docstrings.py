#!/usr/bin/env python3
"""Normalize docstrings to use triple double-quotes.

This script locates module, class, and function docstrings and replaces
their source with triple double-quoted equivalents. It's conservative and
operates by AST position information, preserving surrounding code.
"""

import ast
from pathlib import Path
import argparse


def normalize_file(path: Path):
    src = path.read_text()
    try:
        mod = ast.parse(src)
    except SyntaxError:
        print(f"Skipping {path}: syntax error")
        return
    lines = src.splitlines()
    edits = []

    def process_node(node):
        if not getattr(node, "body", None):
            return
        first = node.body[0]
        if isinstance(first, ast.Expr) and isinstance(getattr(first, "value", None), ast.Constant) and isinstance(first.value.value, str):
            lineno = first.lineno - 1
            end_lineno = getattr(first, "end_lineno", lineno)
            doc = first.value.value
            indent = lines[lineno][: len(lines[lineno]) - len(lines[lineno].lstrip())]
            safe_doc = doc.replace('"""', '\\"\\"\\"')
            rep = f"{indent}\"\"\"" + safe_doc + '"""'
            edits.append((lineno, end_lineno, rep))

    process_node(mod)
    for node in ast.walk(mod):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            process_node(node)

    if not edits:
        print(f"No docstrings to normalize in {path}")
        return

    new_lines = lines[:]
    for start, end, rep in sorted(edits, key=lambda x: x[0], reverse=True):
        new_lines[start:end + 1] = rep.splitlines()

    path.write_text("\n".join(new_lines) + "\n")
    print(f"Normalized {path}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", nargs="+", help="Files to normalize")
    args = parser.parse_args()
    for p in args.paths:
        normalize_file(Path(p))


if __name__ == "__main__":
    main()
