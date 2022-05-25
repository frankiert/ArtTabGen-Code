from pathlib import Path

from pytest_mock import MockFixture

from arttabgen.config_handler import ConfigHandler
from arttabgen.types_.transformer_application_strategy import (
    TransformerApplicationStrategy,
)


class TestConvertNumberOfColumnsOdds:
    def test_simple(self, mocker: MockFixture):
        mocker.patch("pathlib.Path.read_text")
        mocker.patch(
            "json.loads",
            return_value={"number_of_columns_odds": {"1": None}},
        )

        handler: ConfigHandler = ConfigHandler(
            Path(""), TransformerApplicationStrategy.SELECTIVE
        )

        handler._convert_number_of_columns_odds()

        assert handler.config == {"number_of_columns_odds": {1: None}}


class TestConvertGenModesOdds:
    def test_simple(self, mocker: MockFixture):
        mocker.patch("pathlib.Path.read_text")
        mocker.patch(
            "json.loads",
            return_value={"generation_modes_odds": {"1": None}},
        )

        handler: ConfigHandler = ConfigHandler(
            Path(""), TransformerApplicationStrategy.SELECTIVE
        )

        handler._convert_gen_modes_odds()

        assert handler.config == {"generation_modes_odds": {1: None}}


class TestValidateConfig:
    def test_simple_one_top_level_key(self, mocker: MockFixture):
        def dummy_validator(_):
            pass

        mocker.patch("pathlib.Path.read_text")
        mocker.patch(
            "json.loads",
            return_value={"generation_modes_odds": {"1": None}},
        )
        mocker.patch(
            "json.loads",
            return_value={
                "generation_modes_odds": {"1": None},
                "number_of_columns_odds": {"1": None},
                "dummy_key": None,
                "gt_odds_per_mode": {"1": None},
                "do_complex_values": "True"
            },
        )
        mocker.patch(
            "arttabgen.config_validator.TOP_LEVEL_KEY_VALIDATORS",
            {
                "dummy_key": dummy_validator,
                "generation_modes_odds": dummy_validator,
                "number_of_columns_odds": dummy_validator,
                "gt_odds_per_mode": dummy_validator,
                "do_complex_values": dummy_validator,
            },
        )

        handler: ConfigHandler = ConfigHandler(
            Path(""), TransformerApplicationStrategy.SELECTIVE
        )

        handler.validate_config()

        assert True
