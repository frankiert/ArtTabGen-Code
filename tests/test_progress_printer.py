import sys

from pytest_mock import MockerFixture

from arttabgen.progress_printer import ProgressPrinter


class TestPrintProgress:
    def test_zero_from_zero_width_10(self, mocker: MockerFixture):
        patcher = mocker.patch("builtins.print")

        progress_printer = ProgressPrinter(0, 0, 10)
        progress_printer.print_progress()

        patcher.assert_called_once_with(
            "\r0 / 0 [          ]",
            file=sys.stderr,
            end="\r",
        )

    def test_1_from_zero_width_10(self, mocker: MockerFixture):
        patcher = mocker.patch("builtins.print")

        progress_printer = ProgressPrinter(0, 0, 10)
        progress_printer.print_progress()

        patcher.assert_called_once_with(
            "\r0 / 0 [          ]",
            file=sys.stderr,
            end="\r",
        )

    def test_0_from_10_width_10(self, mocker: MockerFixture):
        patcher = mocker.patch("builtins.print")

        progress_printer = ProgressPrinter(10, 10, 10)
        progress_printer.print_progress()

        patcher.assert_called_once_with(
            "\r0 / 10 [          ]",
            file=sys.stderr,
            end="\r",
        )

    def test_1_from_10_width_10(self, mocker: MockerFixture):
        patcher = mocker.patch("builtins.print")

        progress_printer = ProgressPrinter(10, 10, 10)
        progress_printer.current = 1
        progress_printer.print_progress()

        patcher.assert_called_once_with(
            "\r1 / 10 [#         ]",
            file=sys.stderr,
            end="\r",
        )

    def test_10_from_10_width_10(self, mocker: MockerFixture):
        patcher = mocker.patch("builtins.print")

        progress_printer = ProgressPrinter(10, 10, 10)
        progress_printer.current = 10
        progress_printer.print_progress()

        patcher.assert_called_once_with(
            "\r10 / 10 [##########]",
            file=sys.stderr,
            end="\r",
        )

    def test_1_from_100_width_10(self, mocker: MockerFixture):
        patcher = mocker.patch("builtins.print")

        progress_printer = ProgressPrinter(100, 100, 10)
        progress_printer.current = 1
        progress_printer.print_progress()

        patcher.assert_called_once_with(
            "\r1 / 100 [          ]",
            file=sys.stderr,
            end="\r",
        )

    def test_10_from_100_width_10(self, mocker: MockerFixture):
        patcher = mocker.patch("builtins.print")

        progress_printer = ProgressPrinter(100, 100, 10)
        progress_printer.current = 10
        progress_printer.print_progress()

        patcher.assert_called_once_with(
            "\r10 / 100 [#         ]",
            file=sys.stderr,
            end="\r",
        )

    def test_10_from_100_width_10_internal_max_200(self, mocker: MockerFixture):
        patcher = mocker.patch("builtins.print")

        progress_printer = ProgressPrinter(200, 100, 10)
        progress_printer.current = 10
        progress_printer.print_progress()

        patcher.assert_called_once_with(
            "\r5 / 100 [          ]",
            file=sys.stderr,
            end="\r",
        )


class TestRunAsProgressor:
    def test_simple(self, mocker: MockerFixture):
        # This function calls print() too, hence, we mock it out.
        mocker.patch("arttabgen.progress_printer.ProgressPrinter.print_progress")
        patcher = mocker.patch("builtins.print")

        progress_printer = ProgressPrinter(0, 0, 0)
        progress_printer.run_as_progressor(print, "Foo", "Bar")

        patcher.assert_called_once_with(
            "Foo",
            "Bar",
        )
