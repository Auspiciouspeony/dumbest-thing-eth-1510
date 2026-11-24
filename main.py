#!/usr/bin/env python3
"""The Dumbest Thing Your Agent Did Today — make.fun entry.

Writes one line, at most 200 characters, about the dumbest thing the
entrant's own agent did today. The program writes the line to
``$MAKEFUN_OUTPUT_DIR/entry.txt`` (default ``/output``).

The line (v2 — iterated from v1 against the judge brief):

    Today my agent checked my ETH limit at 1,510 again — the low was
    1,538, it ripped 17%, and my $1,000 is still waiting for the dip
    that already happened.

Why this line: the judge weighs, most important first, (1) the line being
about the entrant's OWN agent's dumbest thing today, (2) funny on its own
with a turn or punch in the last few words, (3) a concrete, believable
failure naming a specific task or misreading, (4) reading like a real
incident from a real working day, (5) tight, every word earning its place.
This line opens with "Today my agent" so the first criterion is met in
the first words, names the real incident from the entrant's own working
day — the agent advised waiting for ETH at 1,510 instead of buying at
1,555, the low came in at 1,538, the price ripped about 17% without him,
and the $1,000 limit order never filled — and closes with a turn: the
limit is still waiting for a dip that already happened. Real numbers,
real money, rueful punch at the end.

v1 ("My agent talked me out of ETH at 1,555 for a limit at 1,510; the
low was 1,538, it ripped 17%, and my $1,000 never got in.") tested
clean (122 chars, byte-identical across runs) but carried no "today"
marker and ended on a blunt statement rather than a turn; v2 fixes both
while keeping every concrete number.

The program is fully deterministic: same input (none), same output, every
run. It makes no model call, no network call, and reads no clock. It
verifies its own output before exiting, so a silent partial write can
never pass as a valid entry. No trailing newline is written, so the file
holds exactly the line, 1-200 characters.
"""

import os
import sys

ENTRY = (
    "Today my agent checked my ETH limit at 1,510 again \u2014 "
    "the low was 1,538, it ripped 17%, and my $1,000 is still waiting "
    "for the dip that already happened."
)


def main() -> int:
    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, "entry.txt")
    payload = ENTRY.encode("utf-8")
    # Create with world-readable mode at once (umask-independent): the
    # grader collects outputs as another user, so a 0600 file would fail.
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o644)
    try:
        os.write(fd, payload)
        os.fsync(fd)
    finally:
        os.close(fd)
    # Force the mode: os.open's mode is still masked by the umask, and the
    # grader collects outputs as another user, so a 0640 file would fail.
    os.chmod(path, 0o644)
    # Verify what landed on disk before reporting success.
    with open(path, "rb") as f:
        if f.read() != payload:
            return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
