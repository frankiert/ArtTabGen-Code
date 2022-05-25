import os.path
from pathlib import Path
from typing import Set

from pytest_mock import MockerFixture

from arttabgen.config_handler import ConfigHandler
from tests.helper import set_up_table_generator


class TestGenerateTables:
    def test_generate_tables(self):
        generator = set_up_table_generator()
        generator.generate_tables_with_gt()

    def test_simple_single_table(self, mocker: MockerFixture):
        mocker.patch("json.loads")
        mocker.patch("pathlib.Path.read_text")
        mocker.patch(
            "arttabgen.config_handler.config_handler",
            ConfigHandler(Path(""), None),
        )
        mocker.patch(
            "arttabgen.config_handler.config_handler.config",
            {"gt_odds_per_mode": {1: 1}},
        )
        generator = set_up_table_generator()
        generator._generate_table_and_gt()


class TestLoadKeywords:
    def test_simple(self):
        generator = set_up_table_generator()
        generator.load_keywords(os.path.join(".", "data", "keywords_motor.txt"))

        assert generator.keywords != ""


class TestLoadUnits:
    def test_simple(self):
        generator = set_up_table_generator()
        generator.load_units(os.path.join(".", "data", "units_motor.json"))

        assert generator.units != ""


class TestBuildGtWordList:
    def test_simple(self):
        generator = set_up_table_generator()
        generator.keywords = [["foo", "bar"], ["baz", "baz2"]]
        generator.units = {
            "Air Gap Thickness": {
                "prefixed_units": [
                    "centimetre",
                    "nanometre",
                ],
                "prefixed_symbols": [
                    "dm",
                    "nm",
                ],
            },
            "Coil Resistance": {
                "prefixed_units": [
                    "centio",
                    "kiloo",
                ],
                "prefixed_symbols": [
                    "go",
                    "o",
                ],
            },
        }

        generator.build_gt_word_list()

        expected: Set[str] = {
            "foo",
            "bar",
            "baz",
            "baz2",
            "Air Gap Thickness",
            "centimetre",
            "nanometre",
            "dm",
            "nm",
            "Coil Resistance",
            "prefixed_units",
            "centio",
            "kiloo",
            "prefixed_symbols",
            "go",
            "o",
        }

        assert generator.gt_word_list == expected


class TestManipulateRow:

    def test_dont_generate_existing_data(self, mocker: MockerFixture):
        mocker.patch("random.uniform", return_value=0.2)
        mocker.patch("random.randrange", return_value=1)
        mocker.patch("random.choice", return_value=lambda _: "baz")

        generator = set_up_table_generator()
        generator.gt_word_list = {"foo", "bar", "baz"}

        row = ["burst pressure, npa", "bar"]

        expected = ["burst pressure, npa", "bar"]
        returned = generator._manipulate_row(row, 0.25)

        assert expected == returned


class TestChooseUnit:
    def test_true_mode_1(self, mocker: MockerFixture):
        mocker.patch("random.uniform", return_value=0.3)
        mocker.patch("json.loads")
        mocker.patch("pathlib.Path.read_text")
        mocker.patch(
            "arttabgen.config_handler.config_handler",
            ConfigHandler(Path(""), None),
        )
        mocker.patch(
            "arttabgen.config_handler.config_handler.config",
            {"gt_odds_per_mode": {1: 1}},
        )

        generator = set_up_table_generator()

        key = ["Air Gap Thickness"]

        returned_symbol, returned_gt = generator._choose_random_unit(key, 1)

    def test_true_mode_2(self, mocker: MockerFixture):
        mocker.patch("random.uniform", return_value=0.8)
        mocker.patch("json.loads")
        mocker.patch("pathlib.Path.read_text")
        mocker.patch(
            "arttabgen.config_handler.config_handler",
            ConfigHandler(Path(""), None),
        )
        mocker.patch(
            "arttabgen.config_handler.config_handler.config",
            {"gt_odds_per_mode": {2: 1}},
        )
        generator = set_up_table_generator()

        key = ["Air Gap Thickness"]

        returned_symbol, returned_gt = generator._choose_random_unit(key, 2)

    def test_false_mode_1(self, mocker: MockerFixture):
        mocker.patch("random.uniform", return_value=0.1)
        mocker.patch("json.loads")
        mocker.patch("pathlib.Path.read_text")
        mocker.patch(
            "arttabgen.config_handler.config_handler",
            ConfigHandler(Path(""), None),
        )
        mocker.patch(
            "arttabgen.config_handler.config_handler.config",
            {"gt_odds_per_mode": {1: 1}},
        )
        generator = set_up_table_generator()

        key = ["Air Gap Thickness"]

        returned_symbol, returned_gt = generator._choose_random_unit(key, 1)

    def test_false_mode_2(self, mocker: MockerFixture):
        mocker.patch("random.uniform", return_value=0.6)
        mocker.patch("json.loads")
        mocker.patch("pathlib.Path.read_text")
        mocker.patch(
            "arttabgen.config_handler.config_handler",
            ConfigHandler(Path(""), None),
        )
        mocker.patch(
            "arttabgen.config_handler.config_handler.config",
            {"gt_odds_per_mode": {2: 1}},
        )
        generator = set_up_table_generator()

        key = ["Air Gap Thickness"]

        returned_symbol, returned_gt = generator._choose_random_unit(key, 2)

    def test_not_in_unit_false_mode_2(self, mocker: MockerFixture):
        mocker.patch("random.uniform", return_value=0.6)
        mocker.patch("json.loads")
        mocker.patch("pathlib.Path.read_text")
        mocker.patch(
            "arttabgen.config_handler.config_handler",
            ConfigHandler(Path(""), None),
        )
        mocker.patch(
            "arttabgen.config_handler.config_handler.config",
            {"gt_odds_per_mode": {2: 1}},
        )
        generator = set_up_table_generator()

        key = ["Random Key"]

        returned_symbol, returned_gt = generator._choose_random_unit(key, 2)


class TestHandleKeys:
    def test_generate_wrong_key(self, mocker: MockerFixture):
        generator = set_up_table_generator()
        generator.keywords = [
            ["Air Gap Thickness", "air gap thickness"],
            ["Coil Resistance", "coil resistance", "electrical resistance"],
        ]
        generator._generate_random_wrong_keyword("er")

    def test_generate_key(self, mocker: MockerFixture):
        mocker.patch("random.uniform", return_value=0.2)
        mocker.patch("random.choice", return_value=["foo", "bar"])

        generator = set_up_table_generator()

        returned_key, returned_gt = generator._choose_random_keyword()

        assert returned_key == [
            "foo",
            "bar",
        ]
        assert returned_gt

    def test_generate_word_key(self, mocker: MockerFixture):
        mocker.patch("random.uniform", return_value=0.7)
        mocker.patch("random.sample", return_value=["two", "words"])

        generator = set_up_table_generator()

        returned_key, returned_gt = generator._choose_random_keyword()

        assert returned_key == [
            "two",
            "words",
        ]

        assert not returned_gt
