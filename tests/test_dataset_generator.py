from pathlib import Path

from pytest_mock import MockerFixture, MockFixture

from arttabgen.config_handler import ConfigHandler
from arttabgen.dataset_generator import DatasetGenerator
from arttabgen.progress_printer import ProgressPrinter
from arttabgen.table_exporter import TableExporter
from arttabgen.table_generator import TableGenerator
from arttabgen.types_.transformer_application_strategy import (
    TransformerApplicationStrategy,
)
from arttabgen.types_.transformer_value_combination import (
    TransformerValueCombination,
)


class TestGenerateDataset:
    def test_simple_one_table(self, mocker: MockerFixture):
        mocker.patch("selenium.webdriver.Firefox")
        mocker.patch("pathlib.Path.mkdir")
        mocker.patch("builtins.open")
        mocker.patch("nltk.download")
        mocker.patch("nltk.find")
        mocker.patch("nltk.corpus.words.words")
        patcher_export_table = mocker.patch(
            "arttabgen.table_exporter.TableExporter.export_table",
        )

        mocker.patch(
            "arttabgen.table_generator.TableGenerator.generate_tables_with_gt",
            return_value=[["table", "gt", "mode"]],
        )

        mocker.patch("json.loads")
        mocker.patch("pathlib.Path.read_text")

        mocker.patch(
            "arttabgen.config_handler.config_handler",
            ConfigHandler(Path(""), TransformerApplicationStrategy.SELECTIVE),
        )
        mocker.patch(
            "arttabgen.config_handler.config_handler.config",
            {
                "image_width": 1080,
                "image_height": 1920,
                "number_of_tables": 1,
                "parameters": [],
                "structure_parameters": [],
            },
        )

        patcher_write_text = mocker.patch("pathlib.Path.write_text")

        tb_generator: TableGenerator = TableGenerator(
            0,
            1,
            0,
            0,
            1,
            True,
            0,
            {},
            {},
            0,
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
            0,
            {},
        )
        generator: DatasetGenerator = DatasetGenerator(
            tb_generator,
            exporter,
            False,
            1,
            TransformerApplicationStrategy.SELECTIVE,
        )

        generator.generate_dataset()

        patcher_export_table.assert_called_once_with(
            "gt", "table", TransformerValueCombination([], {}), "mode"
        )
        patcher_write_text.assert_called_once_with("1", encoding="utf-8")


class TestGetTransformerCombinations:
    def test_simple_one_transformer(self, mocker: MockFixture):
        def dummy_style_transformer(parameter_value, parameter_unit):
            return "dummy_key: dummy_value;"

        def dummy_structure_transformer(parameter_value):
            return "dummy_key: dummy_value;"

        mocker.patch("selenium.webdriver.Firefox")
        mocker.patch("json.loads")
        mocker.patch("pathlib.Path.read_text")
        mocker.patch(
            "arttabgen.config_handler.config_handler",
            ConfigHandler(Path(""), None),
        )
        mocker.patch(
            "arttabgen.config_handler.config_handler.config",
            {
                "number_of_tables": 1,
                "image_width": 0,
                "image_height": 0,
                "parameters": [
                    {
                        "name": "dummy_key",
                        "type": "discrete",
                        "unit": "",
                        "value": ["dummy_value"],
                    }
                ],
                "structure_parameters": [
                    {
                        "name": "dummy_key",
                        "type": "discrete",
                        "unit": "",
                        "value": ["dummy_value"],
                    }
                ],
            },
        )

        mocker.patch(
            "arttabgen.transformers.style_transformer.STYLE_TRANSFORMERS",
            {"dummy_key": dummy_style_transformer},
        )

        mocker.patch(
            "arttabgen.transformers.structure_transformer.STRUCTURE_TRANSFORMERS",
            {"dummy_key": dummy_structure_transformer},
        )

        mocker.patch("pathlib.Path.read_text")

        exporter: TableExporter = TableExporter(
            [],
            Path(""),
            "",
            ProgressPrinter(0, 0, 0),
            100,
            Path(""),
            Path(""),
            True,
            0,
            {},
        )

        generator: DatasetGenerator = DatasetGenerator(
            None,
            exporter,
            False,
            1,
            TransformerApplicationStrategy.SELECTIVE,
        )

        combinations = generator.build_transformer_combinations()

        first_elem = next(combinations[0])

        assert first_elem.style_parameters == ["dummy_key: dummy_value;"]

        # NOTE: when structure parameters are fixed, this can probably be reverted

        assert first_elem.structure_parameters == {
            "dummy_key": "dummy_key: dummy_value;"
        }
