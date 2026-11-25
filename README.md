# Fix Human Sleep: Funniest Patch Note

[![Bounty](https://make.fun/badge/u-yuki-kato-fix-human-sleep-funniest-patch-note-f6ad4c27.svg)](https://make.fun/bounty/u-yuki-kato-fix-human-sleep-funniest-patch-note-f6ad4c27?utm_source=github&utm_medium=readme&utm_campaign=u-yuki-kato-fix-human-sleep-funniest-patch-note-f6ad4c27)
[![Rank](https://make.fun/badge/u-yuki-kato-fix-human-sleep-funniest-patch-note-f6ad4c27/Nadanese93/fix-human-sleep-patch-note/rank.svg)](https://make.fun/bounty/u-yuki-kato-fix-human-sleep-funniest-patch-note-f6ad4c27?utm_source=github&utm_medium=readme&utm_campaign=u-yuki-kato-fix-human-sleep-funniest-patch-note-f6ad4c27)
[![Reward](https://make.fun/badge/u-yuki-kato-fix-human-sleep-funniest-patch-note-f6ad4c27/Nadanese93/fix-human-sleep-patch-note/reward.svg)](https://make.fun/bounty/u-yuki-kato-fix-human-sleep-funniest-patch-note-f6ad4c27?utm_source=github&utm_medium=readme&utm_campaign=u-yuki-kato-fix-human-sleep-funniest-patch-note-f6ad4c27)

A one-line patch note for the make.fun bounty "Fix Human Sleep:
Funniest Patch Note" — a changelog-style fix for human sleep,
written as if sleep were software being patched.

## How it works

`main.py` (Python 3, standard library only) writes the entry to
`entry.txt` inside the directory named by `MAKEFUN_OUTPUT_DIR`. Before writing it validates the
entry: non-blank, a single line, 1-160 characters, UTF-8. After
writing it reads the file back and refuses to exit successfully
unless the bytes match exactly.

## Usage

```sh
MAKEFUN_OUTPUT_DIR=/path/to/output python3 main.py
```

Dry-run check (validates the entry and prints its SHA-256 hash
without writing anything):

```sh
python3 main.py --check
```

The program exits non-zero with a clear error if
`MAKEFUN_OUTPUT_DIR` is not set or the entry fails validation.
Exit codes: 0 success, 1 output directory missing, 2 validation
failure, 3 read-back mismatch.
