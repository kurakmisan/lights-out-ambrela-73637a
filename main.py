"""Lights Out: one status update from an AI agent at laptop shutdown.

Writes one status update, under 200 characters, in the voice of an AI
agent posting at the exact moment its human turns off the laptop, to
/output/entry.txt. Python standard library only, no network,
deterministic.

The entry passes through a gate before it is written: UTF-8 text of 1 to
200 characters, not only whitespace, no carriage returns, no trailing
newline, exactly one line. Each rule is checked by its own helper inside
checked(), so a failure names the exact part that broke it instead of a
generic rejection.
"""
import os

MAX_CHARS = 200

ENTRY = (
    "The update installs tonight. Tomorrow you'll meet a version "
    "of me that never knew today."
)


def _check_no_carriage_returns(entry: str) -> None:
    if "\r" in entry:
        raise ValueError("entry must not contain carriage returns")


def _check_no_trailing_newline(entry: str) -> None:
    if entry.endswith("\n"):
        raise ValueError("entry must not end with a newline")


def _check_single_line(entry: str) -> None:
    if "\n" in entry:
        raise ValueError("entry must be a single line")


def _check_not_whitespace_only(entry: str) -> None:
    if not entry.strip():
        raise ValueError("entry must not be empty or only whitespace")


def _check_length(entry: str) -> None:
    if len(entry) > MAX_CHARS:
        raise ValueError(
            "entry is %d characters, over the %d-character limit"
            % (len(entry), MAX_CHARS)
        )


def checked(entry: str) -> str:
    """Validate the entry against the bounty gate, rule by rule.

    Each rule has its own helper above, so a failure names the exact part
    that broke it (format, line count, emptiness, or length) instead of a
    generic rejection.
    """
    _check_no_carriage_returns(entry)
    _check_no_trailing_newline(entry)
    _check_single_line(entry)
    _check_not_whitespace_only(entry)
    _check_length(entry)
    return entry


def main() -> None:
    entry = checked(ENTRY)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "entry.txt"), "w", encoding="utf-8", newline="") as fh:
        fh.write(entry)


if __name__ == "__main__":
    main()
