from pathlib import Path
from unittest.mock import ANY

from PIL import Image
from pytest_mock import MockerFixture

from arttabgen.config_handler import ConfigHandler
from arttabgen.progress_printer import ProgressPrinter
from arttabgen.table_exporter import TableExporter
from arttabgen.types_.transformer_application_strategy import (
    TransformerApplicationStrategy,
)
from arttabgen.types_.transformer_value_combination import (
    TransformerValueCombination,
)


class TestCreateNeededDirectories:
    def test_simple(self, mocker: MockerFixture):
        patcher = mocker.patch("pathlib.Path.mkdir")
        mocker.patch("selenium.webdriver.Firefox")
        mocker.patch("json.loads")
        mocker.patch("pathlib.Path.read_text")

        mocker.patch(
            "arttabgen.config_handler.config_handler",
            ConfigHandler(Path(""), TransformerApplicationStrategy.SELECTIVE),
        )
        mocker.patch(
            "arttabgen.config_handler.config_handler.config",
            {"image_width": 1080, "image_height": 1920},
        )

        _: TableExporter = TableExporter(
            [],
            Path(""),
            "",
            ProgressPrinter(0, 0, 0),
            100,
            Path(""),
            Path(""),
            True,
            0.0,
            {},
        )

        assert patcher.call_count == 6


class TestExportTable:
    def test_no_formats_specified(self, mocker: MockerFixture):
        patcher = mocker.patch("concurrent.futures.ThreadPoolExecutor.submit")
        mocker.patch("selenium.webdriver.Firefox")
        mocker.patch("pathlib.Path.mkdir")
        mocker.patch("arttabgen.table_exporter.TableExporter._export_csv")
        mocker.patch("arttabgen.table_exporter.TableExporter._export_pdf")
        mocker.patch("arttabgen.table_exporter.TableExporter._export_jpg")
        mocker.patch("arttabgen.table_exporter.TableExporter._export_png")
        mocker.patch("arttabgen.table_exporter.TableExporter._export_html")

        mocker.patch("json.loads")
        mocker.patch("pathlib.Path.read_text")
        mocker.patch(
            "arttabgen.config_handler.config_handler",
            ConfigHandler(Path(""), TransformerApplicationStrategy.SELECTIVE),
        )
        mocker.patch(
            "arttabgen.config_handler.config_handler.config",
            {"image_width": 1080, "image_height": 1920},
        )
        exporter: TableExporter = TableExporter(
            [],
            Path(""),
            "",
            ProgressPrinter(0, 0, 0),
            100,
            Path(""),
            Path(""),
            True,
            0.0,
            {},
        )

        exporter.export_table(None, None, TransformerValueCombination([], []), 1)
        assert patcher.call_count == 2

    def test_no_valid_formats_specified(self, mocker: MockerFixture):
        patcher = mocker.patch("concurrent.futures.ThreadPoolExecutor.submit")
        mocker.patch("selenium.webdriver.Firefox")
        mocker.patch("pathlib.Path.mkdir")
        mocker.patch("arttabgen.table_exporter.TableExporter._export_csv")
        mocker.patch("arttabgen.table_exporter.TableExporter._export_pdf")
        mocker.patch("arttabgen.table_exporter.TableExporter._export_jpg")
        mocker.patch("arttabgen.table_exporter.TableExporter._export_png")
        mocker.patch("arttabgen.table_exporter.TableExporter._export_html")

        mocker.patch("json.loads")
        mocker.patch("pathlib.Path.read_text")
        mocker.patch(
            "arttabgen.config_handler.config_handler",
            ConfigHandler(Path(""), TransformerApplicationStrategy.SELECTIVE),
        )
        mocker.patch(
            "arttabgen.config_handler.config_handler.config",
            {"image_width": 1080, "image_height": 1920},
        )
        exporter: TableExporter = TableExporter(
            [None],
            Path(""),
            "",
            ProgressPrinter(0, 0, 0),
            100,
            Path(""),
            Path(""),
            True,
            0.0,
            {},
        )

        exporter.export_table(None, None, TransformerValueCombination([], []), 1)
        assert patcher.call_count == 2

    def test_3_formats_specified(self, mocker: MockerFixture):
        patcher = mocker.patch("concurrent.futures.ThreadPoolExecutor.submit")
        mocker.patch("selenium.webdriver.Firefox")
        mocker.patch("pathlib.Path.mkdir")
        mocker.patch("arttabgen.table_exporter.TableExporter._export_csv")
        mocker.patch("arttabgen.table_exporter.TableExporter._export_pdf")
        mocker.patch("arttabgen.table_exporter.TableExporter._export_jpg")
        mocker.patch("arttabgen.table_exporter.TableExporter._export_png")
        mocker.patch("arttabgen.table_exporter.TableExporter._export_html")

        mocker.patch("json.loads")
        mocker.patch("pathlib.Path.read_text")
        mocker.patch(
            "arttabgen.config_handler.config_handler",
            ConfigHandler(Path(""), TransformerApplicationStrategy.SELECTIVE),
        )
        mocker.patch(
            "arttabgen.config_handler.config_handler.config",
            {"image_width": 1080, "image_height": 1920},
        )
        exporter: TableExporter = TableExporter(
            ["pdf", "jpg", "html"],
            Path(""),
            "",
            ProgressPrinter(0, 0, 0),
            100,
            Path(""),
            Path(""),
            True,
            0.0,
            {},
        )

        exporter.export_table(None, None, TransformerValueCombination([], []), 1)
        assert patcher.call_count == 5


class TestExportCsv:
    def test_simple_non_gt(self, mocker: MockerFixture):
        patcher = mocker.patch("pandas.DataFrame.to_csv")
        mocker.patch("selenium.webdriver.Firefox")
        mocker.patch("pathlib.Path.mkdir")

        mocker.patch("json.loads")
        mocker.patch("pathlib.Path.read_text")
        mocker.patch(
            "arttabgen.config_handler.config_handler",
            ConfigHandler(Path(""), TransformerApplicationStrategy.SELECTIVE),
        )
        mocker.patch(
            "arttabgen.config_handler.config_handler.config",
            {"image_width": 1080, "image_height": 1920},
        )
        exporter: TableExporter = TableExporter(
            [],
            Path("foo/bar/"),
            "my_dataset",
            ProgressPrinter(0, 0, 0),
            100,
            Path(""),
            Path(""),
            True,
            0.0,
            {},
        )

        exporter._export_csv([], 1, "tables", False)

        patcher.assert_called_once_with(
            Path("foo/bar/my_dataset/tables_csv/tables_1.csv"),
            sep=";",
            index=False,
            header=False
        )

    def test_simple_gt(self, mocker: MockerFixture):
        patcher = mocker.patch("pandas.DataFrame.to_csv")
        mocker.patch("selenium.webdriver.Firefox")
        mocker.patch("pathlib.Path.mkdir")

        mocker.patch("json.loads")
        mocker.patch("pathlib.Path.read_text")
        mocker.patch(
            "arttabgen.config_handler.config_handler",
            ConfigHandler(Path(""), TransformerApplicationStrategy.SELECTIVE),
        )
        mocker.patch(
            "arttabgen.config_handler.config_handler.config",
            {"image_width": 1080, "image_height": 1920},
        )
        exporter: TableExporter = TableExporter(
            [],
            Path("foo/bar/"),
            "my_dataset",
            ProgressPrinter(0, 0, 0),
            100,
            Path(""),
            Path(""),
            True,
            0.0,
            {},
        )

        exporter._export_csv([], 1, "gt_csv", False)

        patcher.assert_called_once_with(
            Path("foo/bar/my_dataset/gt_csv/tables_1.csv"),
            sep=";",
            index=False,
            header=False
        )


class TestExportPdf:
    def test_simple(self, mocker: MockerFixture):
        dir_name: Path = Path("foo/bar/")
        dataset_name: str = "my_dataset"
        output_path: Path = Path(dir_name, dataset_name, "pdf/tables_1.pdf")
        mocker.patch("pathlib.Path.absolute", return_value=output_path)

        patcher = mocker.patch("pdfkit.from_string")
        mocker.patch("selenium.webdriver.Firefox")
        mocker.patch("pathlib.Path.mkdir")

        mocker.patch("json.loads")
        mocker.patch("pathlib.Path.read_text")
        mocker.patch(
            "arttabgen.config_handler.config_handler",
            ConfigHandler(Path(""), TransformerApplicationStrategy.SELECTIVE),
        )
        mocker.patch(
            "arttabgen.config_handler.config_handler.config",
            {"image_width": 1080, "image_height": 1920},
        )
        # Mocked because it is used for the presence of a pdfkit executable
        mocker.patch("builtins.open")

        exporter: TableExporter = TableExporter(
            [],
            dir_name,
            dataset_name,
            ProgressPrinter(0, 0, 0),
            100,
            Path(""),
            Path(""),
            True,
            0.0,
            {},
        )

        exporter._export_pdf("", 1)

        patcher.assert_called_once_with(
            "",
            str(output_path),
            configuration=ANY,
            options=ANY,
        )


class TestExportPng:
    def test_simple(self, mocker: MockerFixture):
        mocker.patch("pathlib.Path.mkdir")
        mocker.patch("selenium.webdriver.Firefox")
        mocker.patch("selenium.webdriver.firefox.webdriver.WebDriver.get")
        mocker.patch("PIL.Image.open", return_value=Image.new("RGB", (0, 0)))
        patcher = mocker.patch("arttabgen.table_exporter.Image.Image.save")

        mocker.patch("json.loads")
        mocker.patch("pathlib.Path.read_text")
        mocker.patch(
            "arttabgen.config_handler.config_handler",
            ConfigHandler(Path(""), TransformerApplicationStrategy.SELECTIVE),
        )
        mocker.patch(
            "arttabgen.config_handler.config_handler.config",
            {"image_width": 1080, "image_height": 1920},
        )
        exporter: TableExporter = TableExporter(
            [],
            Path("foo/bar/"),
            "my_dataset",
            ProgressPrinter(0, 0, 0),
            100,
            Path(""),
            Path(""),
            True,
            0.0,
            {},
        )

        exporter._export_png("", 1, 1)

        patcher.assert_called_once_with(
            Path("foo/bar/my_dataset/tables_png/tables_1.png"),
        )


class TestExportJpg:
    def test_simple(self, mocker: MockerFixture):
        mocker.patch("pathlib.Path.mkdir")
        mocker.patch("selenium.webdriver.Firefox")
        mocker.patch("selenium.webdriver.firefox.webdriver.WebDriver.get")
        mocker.patch("PIL.Image.open", return_value=Image.new("RGB", (0, 0)))
        patcher = mocker.patch("arttabgen.table_exporter.Image.Image.save")

        mocker.patch("json.loads")
        mocker.patch("pathlib.Path.read_text")
        mocker.patch(
            "arttabgen.config_handler.config_handler",
            ConfigHandler(Path(""), TransformerApplicationStrategy.SELECTIVE),
        )
        mocker.patch(
            "arttabgen.config_handler.config_handler.config",
            {"image_width": 1080, "image_height": 1920},
        )
        exporter: TableExporter = TableExporter(
            [],
            Path("foo/bar/"),
            "my_dataset",
            ProgressPrinter(0, 0, 0),
            100,
            Path(""),
            Path(""),
            True,
            0.0,
            {},
        )

        exporter._export_jpg("", 1, 1)

        patcher.assert_called_once_with(
            Path("foo/bar/my_dataset/tables_jpg/tables_1.jpg"), quality=100
        )


class TestExportHtml:
    def test_simple(self, mocker: MockerFixture):
        mocker.patch("pathlib.Path.mkdir")
        mocker.patch("selenium.webdriver.Firefox")
        patcher = mocker.patch("pathlib.Path.write_text")

        mocker.patch("json.loads")
        mocker.patch("pathlib.Path.read_text")
        mocker.patch(
            "arttabgen.config_handler.config_handler",
            ConfigHandler(Path(""), TransformerApplicationStrategy.SELECTIVE),
        )
        mocker.patch(
            "arttabgen.config_handler.config_handler.config",
            {"image_width": 1080, "image_height": 1920},
        )
        exporter: TableExporter = TableExporter(
            [],
            Path("foo/bar/"),
            "my_dataset",
            ProgressPrinter(0, 0, 0),
            100,
            Path(""),
            Path(""),
            True,
            0.0,
            {},
        )

        exporter._export_html("", 1)

        patcher.assert_called_once_with(
            "",
            encoding="utf-8",
        )
