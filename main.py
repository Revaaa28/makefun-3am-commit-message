#!/usr/bin/env python3
"""The 3AM Commit Message — make.fun entry (program/v1).

Entry (102 chars, one line):
    fix: resolved merge conflict between me at 2am and me at 3am, 3am me won, 2am me has filed a complaint

Writes the winning one-line git commit message to /output/entry.txt
and prints it to stdout, byte-identical every run. The gate is
1-139 chars, single line, UTF-8, not only whitespace; the pinned
EXPECTED_LEN below guards against silent edits to the winning line.
"""

import os
import sys

ENTRY = "fix: resolved merge conflict between me at 2am and me at 3am, 3am me won, 2am me has filed a complaint"

MIN_CHARS = 1
MAX_CHARS = 139
EXPECTED_LEN = 102


def validate_entry(line: str) -> None:
    """Sealed-gate mirror: UTF-8 text, 1-139 chars, single line, not only whitespace."""
    if not isinstance(line, str):
        raise ValueError("entry is not text")
    if "\n" in line or "\r" in line:
        raise ValueError("entry must be a single line")
    if not line.strip():
        raise ValueError("entry must not be only whitespace")
    n = len(line)
    if not (MIN_CHARS <= n <= MAX_CHARS):
        raise ValueError(f"entry is {n} chars, must be {MIN_CHARS}-{MAX_CHARS}")
    if n != EXPECTED_LEN:
        raise ValueError(f"entry is {n} chars, expected exactly {EXPECTED_LEN} (winning line changed?)")
    line.encode("utf-8")  # raises if not valid UTF-8 text


def main() -> int:
    validate_entry(ENTRY)
    # Kit contract: program writes one text to /output/entry.txt.
    out_dir = "/output" if os.path.isdir("/output") else "output"
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.txt")
    with open(out_path, "w", encoding="utf-8", newline="") as f:
        f.write(ENTRY)
    # Read back and verify byte-identical.
    with open(out_path, "r", encoding="utf-8", newline="") as f:
        back = f.read()
    if back != ENTRY:
        raise ValueError("read-back mismatch: entry.txt differs from ENTRY")
    validate_entry(back)
    sys.stdout.write(ENTRY + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
