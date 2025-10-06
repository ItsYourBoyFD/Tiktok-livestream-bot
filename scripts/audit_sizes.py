#!/usr/bin/env python3
import os
import sys
from typing import List, Tuple

EXCLUDES = {'.git', '__pycache__', '.venv', 'venv', 'env', 'node_modules'}


def iter_files(root: str) -> List[Tuple[str, int]]:
    results: List[Tuple[str, int]] = []
    for dirpath, dirnames, filenames in os.walk(root):
        # Prune excluded directories
        dirnames[:] = [d for d in dirnames if d not in EXCLUDES]
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            try:
                size = os.path.getsize(filepath)
                results.append((filepath, size))
            except OSError:
                continue
    return results


def main() -> None:
    root = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()
    files = iter_files(root)
    files.sort(key=lambda x: x[1], reverse=True)
    top_n = int(sys.argv[2]) if len(sys.argv) > 2 else 20
    print(f"Top {top_n} largest files under {root}:\n")
    for path, size in files[:top_n]:
        print(f"{size/1024/1024:.2f} MB\t{path}")


if __name__ == '__main__':
    main()
