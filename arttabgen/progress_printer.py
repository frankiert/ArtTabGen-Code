"""Holds the ProgressPrinter class, a helper class for accurate progress tracking in concurrent code."""
import sys
from math import floor
from typing import Any, Callable


class ProgressPrinter:  # noqa: D101
    def __init__(
            self,
            total_progress: int,
            max_printed_progress: int,
            progress_bar_width: int,
    ) -> None:
        """A helper class for accurate progress tracking in concurrent code.

        Note:
            The point of the max_printed_progress parameter is when each item needs multiple steps for completion,
            which would otherwise affect the progress printing.

        Args:
            total_progress: The total progress value used for internal tracking.
            max_printed_progress: The total progress value used for progress printing.
            progress_bar_width: The number of characters to use for the progress bar.

        """
        self.total_progress: int = total_progress
        self.max_printed_progress: int = max_printed_progress
        self.current: int = 0
        self.progress_bar_width: int = progress_bar_width

    def print_progress(self) -> None:
        """Print the current progress to stderr."""
        try:
            scaled_progess: int = int(
                self.current / (self.total_progress / self.max_printed_progress),
            )
        except ZeroDivisionError:
            scaled_progess = 0

        progress_counter: str = f"{scaled_progess} / {self.max_printed_progress}"

        progress_bar: str = _build_progress_bar(
            scaled_progess,
            self.max_printed_progress,
            self.progress_bar_width,
        )
        print(  # noqa: WPS421
            f"\r{progress_counter} {progress_bar}",
            file=sys.stderr,
            end="\r",
        )

    def run_as_progressor(self, progressor: Callable[[Any], None], *args: Any) -> None:
        """Run a function and use its completion to track the current progress.

        Args:
            progressor: A function to run and use for tracking progress.
            args: Arguments to pass to the progressor function.

        """
        progressor(*args)
        self.current += 1
        self.print_progress()


def _build_progress_bar(current: int, total: int, width: int) -> str:
    """A helper function to build a progress bar

    The progress bar is accompanied by a numeric progress indicator like 5/10.

    Args:
        current: The current progress towards total.
        total: The total progress.
        width: The width of the progress bar.

    Returns:
        The printable progress bar.
    """
    try:
        num_filled: int = floor(width * current / total)
    except ZeroDivisionError:
        num_filled = 0

    num_unfilled: int = width - num_filled

    filled_part: str = "#" * num_filled
    unfilled_part: str = " " * num_unfilled

    return f"[{filled_part}{unfilled_part}]"
