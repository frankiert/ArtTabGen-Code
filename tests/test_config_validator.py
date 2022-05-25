import pytest
from arttabgen import config_validator


class TestSeedValidator:
    @pytest.mark.parametrize(
        "seed",
        [
            pytest.param(123, id="positive"),
            pytest.param(0, id="zero"),
        ],
    )
    def test_true_condition(self, seed):
        try:
            config_validator.validate_seed(seed)
            assert True
        except RuntimeError:
            assert False

    @pytest.mark.parametrize(
        "seed",
        [
            pytest.param("1", id="string"),
            pytest.param(-45, id="negative"),
            pytest.param(1.23, id="float"),
        ],
    )
    def test_false_condition(self, seed):
        with pytest.raises(RuntimeError, match="parameter not valid: .*"):
            config_validator.validate_seed(seed)


class TestFontSizeValidator:
    def test_is_valid(self):
        config_validator.validate_font_size(
            {
                "name": "font-size",
                "type": "continuous",
                "unit": "px",
                "value": {"start": 5, "stop": 50, "step": 5},
            },
        )

    def test_not_valid(self):
        with pytest.raises(RuntimeError, match="parameter not valid: .*"):
            config_validator.validate_font_size(
                {
                    "name": "font-size",
                    "type": "discrete",
                    "unit": "px",
                    "value": ["foo", "bar"],
                },
            )


class TestFontFamilyValidator:
    def test_is_valid(self):
        config_validator.validate_font_family(
            {
                "name": "font-family",
                "type": "discrete",
                "unit": "px",
                "value": ["roboto", "comic sans"],
            },
        )

    def test_not_valid(self):
        with pytest.raises(RuntimeError, match="parameter not valid: .*"):
            config_validator.validate_font_family(
                {
                    "name": "font-family",
                    "type": "discrete",
                    "unit": "px",
                    "value": [10, "comic sans"],
                },
            )


class TestFontWeightValidator:
    def test_is_valid(self):
        config_validator.validate_font_weight(
            {
                "name": "font-weight",
                "type": "continuous",
                "unit": "px",
                "value": {"start": 100, "stop": 500, "step": 50},
            },
        )

    def test_not_valid(self):
        with pytest.raises(RuntimeError, match="parameter not valid: .*"):
            config_validator.validate_font_weight(
                {
                    "name": "font-weight",
                    "type": "discrete",
                    "unit": "",
                    "value": ["foo", "oblique"],
                },
            )


class TestFontStyleValidator:
    def test_is_valid(self):
        config_validator.validate_font_style(
            {
                "name": "font-style",
                "type": "discrete",
                "unit": "px",
                "value": ["italic", "normal"],
            },
        )

    def test_not_valid(self):
        with pytest.raises(RuntimeError, match="parameter not valid: .*"):
            config_validator.validate_font_style(
                {
                    "name": "font-style",
                    "type": "discrete",
                    "unit": "px",
                    "value": [1, 2, 3],
                },
            )


class TestTextDecorationLineValidator:
    def test_is_valid(self):
        config_validator.validate_text_decoration_line(
            {
                "name": "text-decoration-line",
                "type": "discrete",
                "unit": "px",
                "value": ["underline", "none", "overline"],
            },
        )

    def test_not_valid(self):
        with pytest.raises(RuntimeError, match="parameter not valid: .*"):
            config_validator.validate_text_decoration_line(
                {
                    "name": "text-decoration-line",
                    "type": "choice",
                    "unit": "px",
                    "value": ["none", "underline"],
                },
            )


class TestTextDecorationStyleValidator:
    def test_is_valid(self):
        config_validator.validate_text_decoration_style(
            {
                "name": "text-decoration-style",
                "type": "discrete",
                "unit": "px",
                "value": ["solid", "double"],
            },
        )

    def test_not_valid(self):
        # NOTE: having type == choice is the error condition being checked for.
        with pytest.raises(RuntimeError, match="parameter not valid: .*"):
            config_validator.validate_text_decoration_style(
                {
                    "name": "text-decoration-style",
                    "type": "choice",
                    "unit": "px",
                    "value": ["none", "underline"],
                },
            )


class TestTextTransformValidator:
    def test_is_valid(self):
        config_validator.validate_text_transform(
            {
                "name": "text-transform",
                "type": "discrete",
                "unit": "px",
                "value": ["none", "uppercase", "lowercase"],
            },
        )

    def test_not_valid(self):
        with pytest.raises(RuntimeError, match="parameter not valid: .*"):
            config_validator.validate_text_transform(
                {
                    "name": "text-transform",
                    "type": "continuous",
                    "unit": "px",
                    "value": {"start": 100, "stop": 500, "step": 50},
                },
            )


class TestTextAlign:
    def test_is_valid(self):
        config_validator.validate_text_align(
            {
                "name": "text-align",
                "type": "discrete",
                "unit": "px",
                "value": ["start", "end", "center"],
            },
        )

    def test_not_valid(self):
        with pytest.raises(RuntimeError, match="parameter not valid: .*"):
            config_validator.validate_text_align(
                {
                    "name": "text-align",
                    "type": "discrete",
                    "unit": "px",
                    "value": ["none", "normal"],
                },
            )


class TestVerticalAlignValidator:
    def test_is_valid(self):
        config_validator.validate_vertical_align(
            {
                "name": "vertical-align",
                "type": "discrete",
                "unit": "px",
                "value": ["baseline", "top", "bottom"],
            },
        )

    def test_not_valid(self):
        with pytest.raises(RuntimeError, match="parameter not valid: .*"):
            config_validator.validate_vertical_align(
                {
                    "name": "vertical-align",
                    "type": "discrete",
                    "unit": "px",
                    "value": [4, 5, 6],
                },
            )


class TestPaddingValidator:
    def test_is_valid(self):
        config_validator.validate_padding(
            {
                "name": "padding",
                "type": "continuous",
                "unit": "px",
                "value": {"start": 5, "stop": 20, "step": 5},
            },
        )

    def test_not_valid(self):
        with pytest.raises(RuntimeError, match="parameter not valid: .*"):
            config_validator.validate_padding(
                {
                    "name": "padding",
                    "type": "discrete",
                    "unit": "px",
                    "value": ["5", "6"],
                },
            )


class TestBorderColorValidator:
    def test_is_valid(self):
        config_validator.validate_border_color(
            {
                "name": "border-color",
                "type": "discrete",
                "unit": "px",
                "value": ["black", "blue", "gray"],
            },
        )

    def test_not_valid(self):
        with pytest.raises(RuntimeError, match="parameter not valid: .*"):
            config_validator.validate_border_color(
                {
                    "name": "border-color",
                    "type": "continuous",
                    "unit": "px",
                    "value": {"start": 5, "stop": 20, "step": 5},
                },
            )


class TestBorderStyleValidator:
    def test_is_valid(self):
        config_validator.validate_border_style(
            {
                "name": "border-style",
                "type": "discrete",
                "unit": "px",
                "value": ["solid", "dotted"],
            },
        )

    def test_not_valid(self):
        with pytest.raises(RuntimeError, match="parameter not valid: .*"):
            config_validator.validate_border_style(
                {
                    "name": "border-style",
                    "type": "discrete",
                    "unit": "px",
                    "value": ["foo"],
                },
            )


class TestBorderWidthValidator:
    def test_is_valid(self):
        config_validator.validate_border_width(
            {
                "name": "border-width",
                "type": "continuous",
                "unit": "px",
                "value": {"start": 1, "stop": 4, "step": 0.5},
            },
        )

    def test_not_valid(self):
        with pytest.raises(RuntimeError, match="parameter not valid: .*"):
            config_validator.validate_border_width(
                {
                    "name": "border-width",
                    "type": "discrete",
                    "unit": "px",
                    "value": ["thicc", "thin"],
                },
            )


class TestBorderSpacingValidator:
    def test_is_valid(self):
        config_validator.validate_border_spacing(
            {
                "name": "border-spacing",
                "type": "continuous",
                "unit": "px",
                "value": {"start": 1, "stop": 4, "step": 0.5},
            },
        )

    def test_not_valid(self):
        with pytest.raises(RuntimeError, match="parameter not valid: .*"):
            config_validator.validate_border_spacing(
                {
                    "name": "border-spacing",
                    "type": "discrete",
                    "unit": "px",
                    "value": ["4", "8"],
                },
            )


class TestBorderCollapseValidator:
    def test_is_valid(self):
        config_validator.validate_border_collapse(
            {
                "name": "border-collapse",
                "type": "discrete",
                "unit": "px",
                "value": ["separate", "collapse"],
            },
        )

    def test_not_valid(self):
        with pytest.raises(RuntimeError, match="parameter not valid: .*"):
            config_validator.validate_border_collapse(
                {
                    "name": "border-collapse",
                    "type": "discrete",
                    "unit": "px",
                    "value": ["dotted", "separate"],
                },
            )


class TestColorValidator:
    def test_is_valid(self):
        config_validator.validate_color(
            {
                "name": "color",
                "type": "discrete",
                "unit": "px",
                "value": ["white", "gray", "blue"],
            },
        )

    def test_not_valid(self):
        with pytest.raises(RuntimeError, match="parameter not valid: .*"):
            config_validator.validate_color(
                {
                    "name": "color",
                    "type": "discrete",
                    "unit": "px",
                    "value": {"start": 1, "stop": 4, "step": 0.5},
                },
            )


class TestColorAlternatingRowValidator:
    def test_is_valid(self):
        config_validator.validate_color_alternating_row(
            {
                "name": "color-alternating-row",
                "type": "discrete",
                "unit": "px",
                "value": [["white", "gray", "blue"], ["red", "green", "yellow"]],
            },
        )

    def test_not_valid(self):
        with pytest.raises(RuntimeError, match="parameter not valid: .*"):
            config_validator.validate_color_alternating_row(
                {
                    "name": "color-alternating-row",
                    "type": "discrete",
                    "unit": "px",
                    "value": [123, 456],
                },
            )


class TestColorAlternatingColumnValidator:
    def test_is_valid(self):
        config_validator.validate_color_alternating_column(
            {
                "name": "color-alternating-column",
                "type": "discrete",
                "unit": "px",
                "value": [["white", "gray", "blue"], ["red", "green", "yellow"]],
            },
        )

    def test_not_valid(self):
        with pytest.raises(RuntimeError, match="parameter not valid: .*"):
            config_validator.validate_color_alternating_column(
                {
                    "name": "color-alternating-column",
                    "type": "discrete",
                    "unit": "px",
                    "value": [123, 456],
                },
            )


class TestBackgroundColorValidator:
    def test_is_valid(self):
        config_validator.validate_background_color(
            {
                "name": "background-color",
                "type": "discrete",
                "unit": "px",
                "value": ["white", "gray", "blue"],
            },
        )

    def test_not_valid(self):
        with pytest.raises(RuntimeError, match="parameter not valid: .*"):
            config_validator.validate_background_color(
                {
                    "name": "background-color",
                    "type": "choice",
                    "unit": "px",
                    "value": ["bold", "normal"],
                },
            )


class TestBackgroundColorAlternatingRowValidator:
    def test_is_valid(self):
        config_validator.validate_background_color_alternating_row(
            {
                "name": "background-color-alternating-row",
                "type": "discrete",
                "unit": "px",
                "value": [["white", "gray", "blue"], ["red", "green", "yellow"]],
            },
        )

    def test_not_valid(self):
        with pytest.raises(RuntimeError, match="parameter not valid: .*"):
            config_validator.validate_background_color_alternating_row(
                {
                    "name": "background-color-alternating-row",
                    "type": "discrete",
                    "unit": "px",
                    "value": [123, 456],
                },
            )


class TestBackgroundColorAlternatingColumnValidator:
    def test_is_valid(self):
        config_validator.validate_background_color_alternating_column(
            {
                "name": "background-color-alternating-column",
                "type": "discrete",
                "unit": "px",
                "value": [["white", "gray", "blue"], ["red", "green", "yellow"]],
            },
        )

    def test_not_valid(self):
        with pytest.raises(RuntimeError, match="parameter not valid: .*"):
            config_validator.validate_background_color_alternating_column(
                {
                    "name": "background-color-alternating-column",
                    "type": "discrete",
                    "unit": "px",
                    "value": [123, 456],
                },
            )


class TestTableWidthValidator:
    def test_is_valid(self):
        config_validator.validate_table_width(
            {
                "name": "table-width",
                "type": "continuous",
                "unit": "px",
                "value": {"start": 500, "stop": 700, "step": 50},
            },
        )

    def test_not_valid(self):
        with pytest.raises(RuntimeError, match="parameter not valid: .*"):
            config_validator.validate_table_width(
                {
                    "name": "table-width",
                    "type": "discrete",
                    "unit": "px",
                    "value": ["100", "normal"],
                },
            )


class TestTableHeightValidator:
    def test_is_valid(self):
        config_validator.validate_table_height(
            {
                "name": "table-height",
                "type": "continuous",
                "unit": "px",
                "value": {"start": 500, "stop": 700, "step": 50},
            },
        )

    def test_not_valid(self):
        with pytest.raises(RuntimeError, match="parameter not valid: .*"):
            config_validator.validate_table_height(
                {
                    "name": "table-height",
                    "type": "continuous",
                    "unit": "px",
                    "value": {"start": 500, "step": 50},
                },
            )


class TestMarginTopValidator:
    def test_is_valid(self):
        config_validator.validate_margin_top(
            {
                "name": "margin-top",
                "type": "continuous",
                "unit": "px",
                "value": {"start": 0, "stop": 30, "step": 5},
            },
        )

    def test_not_valid(self):
        with pytest.raises(RuntimeError, match="parameter not valid: .*"):
            config_validator.validate_margin_top(
                {
                    "name": "margin-top",
                    "type": "discrete",
                    "unit": "px",
                    "value": [0, "100%"],
                },
            )


class TestMarginBottomValidator:
    def test_is_valid(self):
        config_validator.validate_margin_bottom(
            {
                "name": "margin-bottom",
                "type": "discrete",
                "unit": "px",
                "value": [0, 10, 30],
            },
        )

    def test_not_valid(self):
        with pytest.raises(RuntimeError, match="parameter not valid: .*"):
            config_validator.validate_margin_bottom(
                {
                    "name": "margin-bottom",
                    "type": "discrete",
                    "unit": "px",
                    "value": ["4", 3],
                },
            )


class TestMarginLeftValidator:
    def test_is_valid(self):
        config_validator.validate_margin_left(
            {
                "name": "margin-left",
                "type": "continuous",
                "unit": "px",
                "value": {"start": 0, "stop": 30, "step": 5},
            },
        )

    def test_not_valid(self):
        with pytest.raises(RuntimeError, match="parameter not valid: .*"):
            config_validator.validate_margin_left(
                {
                    "name": "margin-left",
                    "type": "continuous",
                    "unit": "px",
                    "value": {"stop": 30, "step": 5},
                },
            )


class TestMarginRightValidator:
    def test_is_valid(self):
        config_validator.validate_margin_right(
            {
                "name": "margin-right",
                "type": "continuous",
                "unit": "px",
                "value": {"start": 0, "stop": 30, "step": 5},
            },
        )

    def test_not_valid(self):
        with pytest.raises(RuntimeError, match="parameter not valid: .*"):
            config_validator.validate_margin_right(
                {
                    "name": "margin-right",
                    "type": "choice",
                    "unit": "px",
                    "value": [10, 20],
                },
            )


class TestTableValueLimitValidator:
    def test_no_int(self):
        with pytest.raises(RuntimeError, match="parameter not valid: .*"):
            config_validator.validate_table_value_limit("2")

    def test_negative_value(self):
        with pytest.raises(RuntimeError, match="parameter not valid: .*"):
            config_validator.validate_table_value_limit(-1)

    def test_correct(self):
        config_validator.validate_table_value_limit(1)


class TestRowManipulationOddsValidator:
    def test_no_float(self):
        with pytest.raises(RuntimeError, match="parameter not valid: .*"):
            config_validator.validate_row_manipulation_odds(1)

    def test_negative_value(self):
        with pytest.raises(RuntimeError, match="parameter not valid: .*"):
            config_validator.validate_row_manipulation_odds(-1.0)

    def test_correct(self):
        config_validator.validate_row_manipulation_odds(0.5)


class TestGenModesOddsValidator:
    def test_correct_types(self):
        config_validator.validate_gen_modes_odds({"1": 0.1, "2": 0.2})

    def test_non_string_key_type(self):
        with pytest.raises(RuntimeError, match="parameter not valid: .*"):
            config_validator.validate_gen_modes_odds({1: 0.1, 2: 0.2})

    def test_non_float_value_type(self):
        with pytest.raises(RuntimeError, match="parameter not valid: .*"):
            config_validator.validate_gen_modes_odds({"1": 1, "2": 2})


class TestNumberOfColumnsOddsValidator:
    def test_correct_types(self):
        config_validator.validate_number_of_columns_odds({"1": 0.1, "2": 0.2})

    def test_non_string_key_type(self):
        with pytest.raises(RuntimeError, match="parameter not valid: .*"):
            config_validator.validate_number_of_columns_odds({1: 0.1, 2: 0.2})

    def test_non_float_value_type(self):
        with pytest.raises(RuntimeError, match="parameter not valid: .*"):
            config_validator.validate_number_of_columns_odds({"1": 1, "2": 2})


class TestHasHeaderValidator:
    def test_invalid_value(self):
        with pytest.raises(RuntimeError, match="parameter not valid: .*"):
            config_validator.validate_has_header(
                {
                    "name": "has-header",
                    "type": "discrete",
                    "value": [10, "comic sans"],
                    "unit": "px",
                },
            )

    def test_correct_value(self):
        config_validator.validate_has_header(
            {
                "name": "has-header",
                "type": "discrete",
                "unit": "px",
                "value": [True, False],
            },
        )

    def test_invalid_type(self):
        with pytest.raises(RuntimeError, match="parameter not valid: .*"):
            config_validator.validate_has_header(
                {
                    "name": "has-header",
                    "type": "foo",
                    "unit": "px",
                    "value": [True, False],
                },
            )

    def test_correct_type(self):
        config_validator.validate_has_header(
            {
                "name": "has-header",
                "type": "discrete",
                "unit": "px",
                "value": [True, False],
            },
        )


class TestTableOrientationValidator:
    def test_invalid_value(self):
        with pytest.raises(RuntimeError, match="parameter not valid: .*"):
            config_validator.validate_table_orientation(
                {
                    "name": "table-orientation",
                    "type": "discrete",
                    "unit": "px",
                    "value": [10, "comic sans"],
                },
            )

    def test_correct_value(self):
        config_validator.validate_table_orientation(
            {
                "name": "table-orientation",
                "type": "discrete",
                "unit": "px",
                "value": ["vertical", "horizontal"],
            },
        )

    def test_invalid_type(self):
        with pytest.raises(RuntimeError, match="parameter not valid: .*"):
            config_validator.validate_table_orientation(
                {
                    "name": "table-orientation",
                    "type": "foo",
                    "unit": "px",
                    "value": [True, False],
                },
            )

    def test_correct_type(self):
        config_validator.validate_table_orientation(
            {
                "name": "table-orientation",
                "type": "discrete",
                "unit": "px",
                "value": ["vertical", "horizontal"],
            },
        )


class TestMinTableLengthValidator:
    def test_value_zero(self):
        config_validator.validate_min_table_length(0)

        assert True

    def test_value_negative(self):
        with pytest.raises(RuntimeError, match="parameter not valid: .*"):
            config_validator.validate_min_table_length(-1)

        assert True

    def test_value_100(self):
        config_validator.validate_min_table_length(100)

        assert True

    def test_non_int_value(self):
        with pytest.raises(RuntimeError, match="parameter not valid: .*"):
            config_validator.validate_min_table_length("100")


class TestMaxTableLengthValidator:
    def test_value_zero(self):
        config_validator.validate_max_table_length(0)

        assert True

    def test_value_negative(self):
        with pytest.raises(RuntimeError, match="parameter not valid: .*"):
            config_validator.validate_max_table_length(-1)

        assert True

    def test_value_100(self):
        config_validator.validate_max_table_length(100)

        assert True

    def test_non_int_value(self):
        with pytest.raises(RuntimeError, match="parameter not valid: .*"):
            config_validator.validate_max_table_length("100")


class TestJpgQualityValidator:
    def test_value_zero(self):
        config_validator.validate_jpg_quality(0)

        assert True

    def test_value_negative(self):
        with pytest.raises(RuntimeError, match="parameter not valid: .*"):
            config_validator.validate_max_table_length(-1)

    def test_value_100(self):
        config_validator.validate_jpg_quality(100)

        assert True

    def test_value_over_100(self):
        with pytest.raises(RuntimeError, match="parameter not valid: .*"):
            config_validator.validate_jpg_quality(500)

    def test_non_int_value(self):
        with pytest.raises(RuntimeError, match="parameter not valid: .*"):
            config_validator.validate_jpg_quality("100")


class TestNumberOfTablesValidator:
    def test_value_zero(self):
        with pytest.raises(RuntimeError, match="parameter not valid: .*"):
            config_validator.validate_number_of_tables(0)

    def test_value_one(self):
        config_validator.validate_number_of_tables(1)

        assert True

    def test_value_negative(self):
        with pytest.raises(RuntimeError, match="parameter not valid: .*"):
            config_validator.validate_number_of_tables(-1)

    def test_value_100(self):
        config_validator.validate_number_of_tables(100)

        assert True


class TestKeyChanceValidator:
    def test_value_zero(self):
        config_validator.validate_keyword_chance(0.0)

        assert True

    def test_value_one(self):
        config_validator.validate_keyword_chance(1.0)

        assert True

    def test_value_negative(self):
        with pytest.raises(RuntimeError, match="parameter not valid: .*"):
            config_validator.validate_keyword_chance(-1.0)

    def test_value_above_max(self):
        with pytest.raises(RuntimeError, match="parameter not valid: .*"):
            config_validator.validate_keyword_chance(100.0)


class TestLetterSpacingValidator:
    def test_is_valid(self):
        config_validator.validate_letter_spacing(
            {
                "name": "letter-spacing",
                "type": "continuous",
                "unit": "px",
                "value": {"start": 5, "stop": 50, "step": 5},
            },
        )

    def test_not_valid(self):
        with pytest.raises(RuntimeError, match="parameter not valid: .*"):
            config_validator.validate_letter_spacing(
                {
                    "name": "letter-spacing",
                    "type": "discrete",
                    "unit": "px",
                    "value": ["foo", "bar"],
                },
            )


class TestParameterValidator:
    def test_successful(self):
        style_parameters = [
            {
                "name": "font-family",
                "type": "discrete",
                "unit": "px",
                "value": [
                    "Arial",
                    "Impact",
                    "Didot",
                    "American Typewriter",
                    "Times New Roman",
                    "Courier",
                    "Comic Sans MS",
                ],
            },
            {
                "name": "font-size",
                "type": "continuous",
                "value": {"start": 5, "stop": 50, "step": 5},
            },
        ]

        config_validator.validate_parameter(style_parameters)
        assert True

    def test_font_family_invalid(self):
        style_parameters = [
            {
                "name": "font-family",
                "type": "continuous",
                "unit": "px",
                "value": [
                    "Arial",
                    "Impact",
                    "Didot",
                    "American Typewriter",
                    "Times New Roman",
                    "Courier",
                    "Comic Sans MS",
                ],
            },
            {
                "name": "font-size",
                "type": "continuous",
                "value": {"start": 5, "stop": 50, "step": 5},
            },
        ]

        with pytest.raises(RuntimeError, match="parameter not valid: .*"):
            config_validator.validate_parameter(style_parameters)


class TestStructureParameterValidator:
    def test_successful(self):
        structure_parameters = [
            {"name": "has-header", "type": "discrete", "value": [True, False]},
            {
                "name": "table-orientation",
                "type": "discrete",
                "value": ["vertical", "horizontal"],
            },
        ]

        config_validator.validate_structure_parameter(structure_parameters)
        assert True

    def test_font_family_invalid(self):
        structure_parameters = [
            {"name": "has-header", "type": "continuous", "value": [True, False]},
            {
                "name": "table-orientation",
                "type": "discrete",
                "value": ["vertical", "horizontal"],
            },
        ]

        with pytest.raises(RuntimeError, match="parameter not valid: .*"):
            config_validator.validate_structure_parameter(structure_parameters)
