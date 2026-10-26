"""Running one example in a fresh kernel, when the kernel itself fails to start."""

import sys

import pytest

from cheatsheet import execute
from cheatsheet.execute import run_example

# A "kernel" that exits at once, as a real one does when another process took one of its ports first.
DIES = [sys.executable, "-c", "raise SystemExit(1)"]


def kernels_that_die_first(monkeypatch, deaths: int) -> list[None]:
    """Make the first `deaths` kernels die while starting; returns a list with one item per kernel started."""
    real = execute._kernel_argv
    starts: list[None] = []

    def argv() -> list[str]:
        starts.append(None)
        return DIES if len(starts) <= deaths else real()

    monkeypatch.setattr(execute, "_kernel_argv", argv)
    return starts


def test_a_kernel_that_dies_while_starting_is_started_again(monkeypatch):
    starts = kernels_that_die_first(monkeypatch, 2)

    assert run_example("print(6 * 7)").stdout == "42"
    assert len(starts) == 3


def test_a_kernel_that_keeps_dying_fails_after_three_starts(monkeypatch):
    starts = kernels_that_die_first(monkeypatch, 99)

    with pytest.raises(RuntimeError, match="Kernel died before replying"):
        run_example("print(1)")
    assert len(starts) == 3
