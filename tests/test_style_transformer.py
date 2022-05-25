from typing import List

from pytest_mock import MockerFixture

from arttabgen.helper import (
    ContinuousParameter,
    DiscreteParameter,
    random_value_from_continuous,
    random_value_from_discrete,
)
from arttabgen.transformers import style_transformer
from tests.helper import get_first_element_in_range, get_first_element_in_sequence


class TestTransformerFontFamily:
    def test_discrete(self, mocker: MockerFixture):
        mocker.patch(
            "arttabgen.helper.random_value_from_discrete",
            get_first_element_in_sequence,
        )

        parameter: str = "Arial"

        returned: str = style_transformer.transformer_font_family(parameter, "")

        assert returned == "table, tr, td {font-family: Arial;}"


class TestTransformerFontSize:
    def test_discrete(self, mocker: MockerFixture):
        mocker.patch(
            "arttabgen.helper.random_value_from_discrete",
            get_first_element_in_sequence,
        )

        parameter: str = "Arial"

        returned: str = style_transformer.transformer_font_size(parameter, "px")

        assert returned == "table, tr, td {font-size: Arialpx;}"

    def test_continuous(self, mocker: MockerFixture):
        mocker.patch(
            "arttabgen.helper.randrange_float",
            get_first_element_in_range,
        )

        parameter: int = 10

        returned: str = style_transformer.transformer_font_size(parameter, "px")

        assert returned == "table, tr, td {font-size: 10px;}"


class TestTransformerFontWeight:
    def test_discrete(self, mocker: MockerFixture):
        mocker.patch(
            "arttabgen.helper.random_value_from_discrete",
            get_first_element_in_sequence,
        )

        parameter: str = "Arial"

        returned: str = style_transformer.transformer_font_weight(parameter, "")

        assert returned == "table, tr, td {font-weight: Arial;}"

    def test_continuous(self, mocker: MockerFixture):
        mocker.patch(
            "arttabgen.helper.randrange_float",
            get_first_element_in_range,
        )
        parameter: int = 10

        returned: str = style_transformer.transformer_font_weight(parameter, "")

        assert returned == "table, tr, td {font-weight: 10;}"


class TestTransformerFontStyle:
    def test_discrete(self, mocker: MockerFixture):
        mocker.patch(
            "arttabgen.helper.random_value_from_discrete",
            get_first_element_in_sequence,
        )

        parameter: str = "Arial"

        returned: str = style_transformer.transformer_font_style(parameter, "")

        assert returned == "table, tr, td {font-style: Arial;}"


class TestTransformerBorderCollapse:
    def test_discrete(self, mocker: MockerFixture):
        mocker.patch(
            "arttabgen.helper.random_value_from_discrete",
            get_first_element_in_sequence,
        )

        parameter: str = "Arial"

        returned: str = style_transformer.transformer_border_collapse(parameter, "")

        assert returned == "table, tr, td {border-collapse: Arial;}"


class TestTransformerBorderSpacing:
    def test_discrete(self, mocker: MockerFixture):
        mocker.patch(
            "arttabgen.helper.random_value_from_discrete",
            get_first_element_in_sequence,
        )

        parameter: str = "Arial"

        returned: str = style_transformer.transformer_border_spacing(parameter, "px")

        assert returned == "table, tr, td {border-spacing: Arialpx;}"

    def test_continuous(self, mocker: MockerFixture):
        mocker.patch(
            "arttabgen.helper.randrange_float",
            get_first_element_in_range,
        )
        parameter: int = 10

        returned: str = style_transformer.transformer_border_spacing(parameter, "px")

        assert returned == "table, tr, td {border-spacing: 10px;}"


class TestTransformerBorderWidth:
    def test_discrete(self, mocker: MockerFixture):
        mocker.patch(
            "arttabgen.helper.random_value_from_discrete",
            get_first_element_in_sequence,
        )

        parameter: str = "Arial"

        returned: str = style_transformer.transformer_border_width(parameter, "px")

        assert returned == "table, tr, td {border-width: Arialpx;}"

    def test_continuous(self, mocker: MockerFixture):
        mocker.patch(
            "arttabgen.helper.randrange_float",
            get_first_element_in_range,
        )
        parameter: int = 10

        returned: str = style_transformer.transformer_border_width(parameter, "px")

        assert returned == "table, tr, td {border-width: 10px;}"


class TestTransformerBorderStyle:
    def test_discrete(self, mocker: MockerFixture):
        mocker.patch(
            "arttabgen.helper.random_value_from_discrete",
            get_first_element_in_sequence,
        )

        parameter: str = "Arial"

        returned: str = style_transformer.transformer_border_style(parameter, "")

        assert returned == "table, tr, td {border-style: Arial;}"


class TestTransformerBorderColor:
    def test_discrete(self, mocker: MockerFixture):
        mocker.patch(
            "arttabgen.helper.random_value_from_discrete",
            get_first_element_in_sequence,
        )

        parameter: str = "Arial"

        returned: str = style_transformer.transformer_border_color(parameter, "")

        assert returned == "table, tr, td {border-color: Arial;}"


class TestTransformerTextTransform:
    def test_discrete(self, mocker: MockerFixture):
        mocker.patch(
            "arttabgen.helper.random_value_from_discrete",
            get_first_element_in_sequence,
        )

        parameter: str = "Arial"

        returned: str = style_transformer.transformer_text_transform(parameter, "")

        assert returned == "table, tr, td {text-transform: Arial;}"


class TestTransformerTextAlign:
    def test_discrete(self, mocker: MockerFixture):
        mocker.patch(
            "arttabgen.helper.random_value_from_discrete",
            get_first_element_in_sequence,
        )

        parameter: str = "Arial"

        returned: str = style_transformer.transformer_text_align(parameter, "")

        assert returned == "table, tr, td {text-align: Arial;}"


class TestTransformerLetterSpacing:
    def test_discrete(self, mocker: MockerFixture):
        mocker.patch(
            "arttabgen.helper.random_value_from_discrete",
            get_first_element_in_sequence,
        )

        parameter: str = "Arial"

        returned: str = style_transformer.transformer_letter_spacing(parameter, "px")

        assert returned == "table, tr, td {letter-spacing: Arialpx;}"

    def test_continuous(self, mocker: MockerFixture):
        mocker.patch(
            "arttabgen.helper.randrange_float",
            get_first_element_in_range,
        )
        parameter: int = 10

        returned: str = style_transformer.transformer_letter_spacing(parameter, "px")

        assert returned == "table, tr, td {letter-spacing: 10px;}"


class TestTransformerVerticalAlign:
    def test_discrete(self, mocker: MockerFixture):
        mocker.patch(
            "arttabgen.helper.random_value_from_discrete",
            get_first_element_in_sequence,
        )

        parameter: str = "Arial"

        returned: str = style_transformer.transformer_vertical_align(parameter, "")

        assert returned == "table, tr, td {vertical-align: Arial;}"


class TestTransformerTextDecorationLine:
    def test_discrete(self, mocker: MockerFixture):
        mocker.patch(
            "arttabgen.helper.random_value_from_discrete",
            get_first_element_in_sequence,
        )

        parameter: str = "Arial"

        returned: str = style_transformer.transformer_text_decoration_line(
            parameter, ""
        )

        assert returned == "table, tr, td {text-decoration-line: Arial;}"


class TestTransformerTextDecorationStyle:
    def test_discrete(self, mocker: MockerFixture):
        mocker.patch(
            "arttabgen.helper.random_value_from_discrete",
            get_first_element_in_sequence,
        )

        parameter: str = "Arial"

        returned: str = style_transformer.transformer_text_decoration_style(
            parameter, ""
        )

        assert returned == "table, tr, td {text-decoration-style: Arial;}"


class TestTransformerPadding:
    def test_discrete(self, mocker: MockerFixture):
        mocker.patch(
            "arttabgen.helper.random_value_from_discrete",
            get_first_element_in_sequence,
        )

        parameter: str = "Arial"

        returned: str = style_transformer.transformer_padding(parameter, "px")

        assert returned == "td {padding: Arialpx;}"

    def test_continuous(self, mocker: MockerFixture):
        mocker.patch(
            "arttabgen.helper.randrange_float",
            get_first_element_in_range,
        )
        parameter: int = 10

        returned: str = style_transformer.transformer_padding(parameter, "px")

        assert returned == "td {padding: 10px;}"


class TestTransformerMarginLeft:
    def test_discrete(self, mocker: MockerFixture):
        mocker.patch(
            "arttabgen.helper.random_value_from_discrete",
            get_first_element_in_sequence,
        )

        parameter: str = "Arial"

        returned: str = style_transformer.transformer_margin_left(parameter, "px")

        assert returned == "table {margin-left: Arialpx;}"

    def test_continuous(self, mocker: MockerFixture):
        mocker.patch(
            "arttabgen.helper.randrange_float",
            get_first_element_in_range,
        )
        parameter: int = 10

        returned: str = style_transformer.transformer_margin_left(parameter, "px")

        assert returned == "table {margin-left: 10px;}"


class TestTransformerMarginRight:
    def test_discrete(self, mocker: MockerFixture):
        mocker.patch(
            "arttabgen.helper.random_value_from_discrete",
            get_first_element_in_sequence,
        )

        parameter: str = "Arial"

        returned: str = style_transformer.transformer_margin_right(parameter, "px")

        assert returned == "table {margin-right: Arialpx;}"

    def test_continuous(self, mocker: MockerFixture):
        mocker.patch(
            "arttabgen.helper.randrange_float",
            get_first_element_in_range,
        )
        parameter: int = 10

        returned: str = style_transformer.transformer_margin_right(parameter, "px")

        assert returned == "table {margin-right: 10px;}"


class TestTransformerMarginTop:
    def test_discrete(self, mocker: MockerFixture):
        mocker.patch(
            "arttabgen.helper.random_value_from_discrete",
            get_first_element_in_sequence,
        )

        parameter: str = "Arial"

        returned: str = style_transformer.transformer_margin_top(parameter, "px")

        assert returned == "table {margin-top: Arialpx;}"

    def test_continuous(self, mocker: MockerFixture):
        mocker.patch(
            "arttabgen.helper.randrange_float",
            get_first_element_in_range,
        )
        parameter: int = 10

        returned: str = style_transformer.transformer_margin_top(parameter, "px")

        assert returned == "table {margin-top: 10px;}"


class TestTransformerMarginBottom:
    def test_discrete(self, mocker: MockerFixture):
        mocker.patch(
            "arttabgen.helper.random_value_from_discrete",
            get_first_element_in_sequence,
        )

        parameter: str = "Arial"

        returned: str = style_transformer.transformer_margin_bottom(parameter, "px")

        assert returned == "table {margin-bottom: Arialpx;}"

    def test_continuous(self, mocker: MockerFixture):
        mocker.patch(
            "arttabgen.helper.randrange_float",
            get_first_element_in_range,
        )
        parameter: int = 10

        returned: str = style_transformer.transformer_margin_bottom(parameter, "px")

        assert returned == "table {margin-bottom: 10px;}"


class TestTransformerTableWidth:
    def test_discrete(self, mocker: MockerFixture):
        mocker.patch(
            "arttabgen.helper.random_value_from_discrete",
            get_first_element_in_sequence,
        )

        parameter: str = "Arial"

        returned: str = style_transformer.transformer_table_width(parameter, "px")

        assert returned == "table {width: Arialpx;}"

    def test_continuous(self, mocker: MockerFixture):
        mocker.patch(
            "arttabgen.helper.randrange_float",
            get_first_element_in_range,
        )
        parameter: int = 10

        returned: str = style_transformer.transformer_table_width(parameter, "px")

        assert returned == "table {width: 10px;}"


class TestTransformerTableHeight:
    def test_discrete(self, mocker: MockerFixture):
        mocker.patch(
            "arttabgen.helper.random_value_from_discrete",
            get_first_element_in_sequence,
        )

        parameter: str = "Arial"

        returned: str = style_transformer.transformer_table_height(parameter, "px")

        assert returned == "table {height: Arialpx;}"

    def test_continuous(self, mocker: MockerFixture):
        mocker.patch(
            "arttabgen.helper.randrange_float",
            get_first_element_in_range,
        )
        parameter: int = 10

        returned: str = style_transformer.transformer_table_height(parameter, "px")

        assert returned == "table {height: 10px;}"


class TestTransformerBackgroundColor:
    def test_discrete(self, mocker: MockerFixture):
        mocker.patch(
            "arttabgen.helper.random_value_from_discrete",
            get_first_element_in_sequence,
        )

        parameter: str = "Arial"

        returned: str = style_transformer.transformer_background_color(parameter, "")

        assert returned == "td {background-color: Arial;}"


class TestTransformerColor:
    def test_discrete(self, mocker: MockerFixture):
        mocker.patch(
            "arttabgen.helper.random_value_from_discrete",
            get_first_element_in_sequence,
        )

        parameter: str = "Arial"

        returned: str = style_transformer.transformer_color(parameter, "")

        assert returned == "td {color: Arial;}"


class TestTransformerColorAlternatingRow:
    def test_discrete(self, mocker: MockerFixture):
        mocker.patch(
            "arttabgen.helper.random_value_from_discrete",
            get_first_element_in_sequence,
        )

        parameter: List[DiscreteParameter] = [
            "Arial",
            "Comic Sans MS",
        ]

        returned: str = style_transformer.transformer_color_alternating_row(
            parameter, ""
        )

        assert (
                returned
                == "tr:nth-child(even) {color: Arial;}\ntr:nth-child(odd) {color: Comic Sans MS;}"
        )


class TestTransformerColorAlternatingColumn:
    def test_discrete(self, mocker: MockerFixture):
        mocker.patch(
            "arttabgen.helper.random_value_from_discrete",
            get_first_element_in_sequence,
        )

        parameter: List[DiscreteParameter] = [
            "Arial",
            "Comic Sans MS",
        ]

        returned: str = style_transformer.transformer_color_alternating_column(
            parameter, ""
        )

        assert (
                returned
                == "td:nth-child(even) {color: Arial;}\ntd:nth-child(odd) {color: Comic Sans MS;}"
        )


class TestTransformerBackgroundColorAlternatingRow:
    def test_discrete(self, mocker: MockerFixture):
        mocker.patch(
            "arttabgen.helper.random_value_from_discrete",
            get_first_element_in_sequence,
        )

        parameter: List[DiscreteParameter] = [
            "Arial",
            "Comic Sans MS",
        ]

        returned: str = style_transformer.transformer_background_color_alternating_row(
            parameter, ""
        )

        assert (
                returned
                == "tr:nth-child(even) {background-color: Arial;}\ntr:nth-child(odd) {background-color: Comic Sans MS;}"
        )


class TestTransformerBackgroundColorAlternatingColumn:
    def test_discrete(self, mocker: MockerFixture):
        mocker.patch(
            "arttabgen.helper.random_value_from_discrete",
            get_first_element_in_sequence,
        )

        parameter: List[DiscreteParameter] = [
            "Arial",
            "Comic Sans MS",
        ]

        returned: str = (
            style_transformer.transformer_background_color_alternating_column(
                parameter, ""
            )
        )

        assert (
                returned
                == "td:nth-child(even) {background-color: Arial;}\ntd:nth-child(odd) {background-color: Comic Sans MS;}"
        )


class TestRandomValueFromDiscrete:
    def test_simple(self, mocker: MockerFixture):
        mocker.patch(
            "random.choice",
            get_first_element_in_sequence,
        )
        assert random_value_from_discrete([1, 2]) == 1


class TestRandomValueFromRange:
    def test_with_stop(self, mocker: MockerFixture):
        mocker.patch("random.uniform", get_first_element_in_sequence)
        mocker.patch(
            "arttabgen.helper.randrange_float",
            get_first_element_in_range,
        )

        parameter: ContinuousParameter = {
            "start": 10,
            "stop": 100,
            "step": 10,
        }
        returned = random_value_from_continuous(parameter)

        assert returned == 10

    def test_without_stop(self, mocker: MockerFixture):
        mocker.patch("random.uniform", get_first_element_in_range)
        mocker.patch(
            "arttabgen.helper.randrange_float",
            get_first_element_in_range,
        )

        parameter: ContinuousParameter = {
            "start": 10,
            "stop": 100,
        }
        returned = random_value_from_continuous(parameter)

        assert returned == 10
