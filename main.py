"""Entry program for the make.fun bounty
"Fix Human Sleep: Funniest Patch Note".

Writes a single-line patch note about fixing human sleep to
$MAKEFUN_OUTPUT_DIR/entry.txt, UTF-8, 1-160 characters.

Deterministic: the entry text is a fixed constant, so every run
produces byte-identical output.
"""

import os
import sys

ENTRY = "Fixed: counting sheep is now optional. Sheep have been deprecated."

MAX_CHARS = 160


class EntryError(Exception):
    """Base class for entry validation failures."""


class BlankError(EntryError):
    """The entry is empty or only whitespace."""


class MultiLineError(EntryError):
    """The entry contains more than one line."""


class LengthError(EntryError):
    """The entry is outside the 1-160 character range."""


class ReadBackError(EntryError):
    """The bytes read back from disk differ from what was written."""


class MissingOutputDirError(EntryError):
    """MAKEFUN_OUTPUT_DIR is not set."""


# Distinct exit codes so a caller can tell failures apart:
#   0 = success, 1 = missing output dir, 2 = validation, 3 = read-back.
EXIT_OK = 0
EXIT_MISSING_DIR = 1
EXIT_VALIDATION = 2
EXIT_READ_BACK = 3


def validate(entry: str) -> None:
    """Check the entry against the contest gate before writing."""
    if not entry.strip():
        raise BlankError("entry must not be blank or only whitespace")
    if "\n" in entry or "\r" in entry:
        raise MultiLineError("entry must be a single line")
    if not 1 <= len(entry) <= MAX_CHARS:
        raise LengthError(
            f"entry must be 1-{MAX_CHARS} characters, got {len(entry)}"
        )


import hashlib
import os
import sys


def entry_sha256(entry: str) -> str:
    """SHA-256 of the entry text encoded as UTF-8, no trailing newline."""
    return hashlib.sha256(entry.encode("utf-8")).hexdigest()


def check_only() -> int:
    """Dry-run mode: validate the entry and print its hash, write nothing."""
    try:
        validate(ENTRY)
    except EntryError as exc:
        print(f"error: invalid entry: {exc}", file=sys.stderr)
        return EXIT_VALIDATION
    print(f"entry ok: {len(ENTRY)} chars, sha256 {entry_sha256(ENTRY)}")
    return EXIT_OK


def main(argv=None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    if args == ["--check"]:
        return check_only()
    if args:
        print(f"error: unknown argument(s): {' '.join(args)}",
              file=sys.stderr)
        return EXIT_VALIDATION

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if not out_dir:
        print(
            "error: MAKEFUN_OUTPUT_DIR environment variable is not set",
            file=sys.stderr,
        )
        return EXIT_MISSING_DIR

    try:
        validate(ENTRY)
    except EntryError as exc:
        print(f"error: invalid entry: {exc}", file=sys.stderr)
        return EXIT_VALIDATION

    data = ENTRY.encode("utf-8")
    out_path = os.path.join(out_dir, "entry.txt")
    os.makedirs(out_dir, exist_ok=True)
    with open(out_path, "wb") as fh:
        fh.write(data)

    # Read-back verification: the written bytes must match exactly.
    with open(out_path, "rb") as fh:
        written = fh.read()
    if written != data:
        raise ReadBackError("read-back verification failed: bytes differ")

    return EXIT_OK


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except ReadBackError as exc:
        print(f"error: {exc}", file=sys.stderr)
        raise SystemExit(EXIT_READ_BACK)
