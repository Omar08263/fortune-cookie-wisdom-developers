"""Fortune Cookie Wisdom for Developers — entry program (program/v1).

Writes one original fortune-cookie line for a software developer
(a single sentence, at most 120 characters) to /output/entry.txt
(or $MAKEFUN_OUTPUT_DIR/entry.txt when set, for local runs).
Deterministic: identical bytes on every run. No network, no randomness,
no reads outside this file.
"""

import os

LINE = "The code you delete on Friday is the bug you will not meet on Monday."

# Gate the line itself: one sentence, 1-120 characters, not only whitespace.
assert 1 <= len(LINE) <= 120, f"line is {len(LINE)} chars, must be 1-120"
assert LINE.strip(), "line must not be only whitespace"
assert LINE.count(".") == 1 and LINE.endswith("."), "line must be a single sentence"


def main() -> None:
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(LINE)
    # Deterministic permissions: the entry must be readable (0644)
    # no matter what umask the sandbox runs with.
    os.chmod(path, 0o644)
    # Read-back check: the file on disk must hold exactly the approved
    # line, byte for byte; otherwise fail loudly, never silently.
    with open(path, "r", encoding="utf-8", newline="\n") as f:
        written = f.read()
    if written != LINE:
        raise SystemExit("entry.txt does not match the approved line")


if __name__ == "__main__":
    main()
