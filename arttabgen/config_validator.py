"""Holds functions to validate config files used for dataset generation.

PARAMETER_VALIDATORS: A list of validation functions for style parameters.
TOP_LEVEL_KEY_VALIDATORS: A list of validation functions for top level keys.
"""
from typing import Any, Callable, Dict, List, Set

from arttabgen.helper import StyleParameterConfiguration, values_match_any_type


def validate_seed(seed: int) -> None:
    """Validate the seed configured in the config file.

    Note:
        The following properties must be satisfied for a validation:
        seed is an integer and >= 0

    Args:
        seed: The seed to validate.

    Raises:
        RuntimeError: If the validation fails.

    """

    if not isinstance(seed, int) or seed < 0:
        raise RuntimeError(f"parameter not valid: {seed}")


def validate_parameter(style_parameters: List[StyleParameterConfiguration]) -> None:
    """Validate the style parameters configured in the config file.

    Args:
        style_parameters: The defined style parameters to validate.

    Raises:
        RuntimeError: If the validation fails.

    """

    for parameter in style_parameters:
        PARAMETER_VALIDATORS[parameter["name"]](parameter)


def validate_structure_parameter(
        style_parameters: List[StyleParameterConfiguration],
) -> None:
    """Validate the structure parameters configured in the config file.

    Args:
        style_parameters: The defined style parameters to validate.

    Raises:
        RuntimeError if the validation fails.

    """

    for parameter in style_parameters:
        STRUCTURE_PARAMETER_VALIDATORS[parameter["name"]](parameter)


def validate_image_manipulators(
        style_parameters: List[StyleParameterConfiguration],
) -> None:
    """Validate the image effects configured in the config file.

    Args:
        style_parameters: The defined style parameters to validate.

    Raises:
        RuntimeError if the validation fails.

    """

    for parameter in style_parameters:
        IMAGE_MANIPULATORS_VALIDATORS[parameter["name"]](parameter)


def validate_font_family(parameter: StyleParameterConfiguration) -> None:
    """Validate the style parameter font-family.

    Note:
        The following properties must be satisfied for a validation:
        type: discrete
        value: list of strings

    Args:
        parameter: The style parameter definition to validate.

    Raises:
        RuntimeError: If the validation fails.

    """

    if not _check_discrete_parameter(parameter, str):
        raise RuntimeError(f"parameter not valid: {parameter}")


def validate_font_size(parameter: StyleParameterConfiguration) -> None:
    """Validate the style parameter font-size.

    Note:
        The following properties must be satisfied for a validation:
        type: discrete or continuous
        value: list of strings or continuous value definition

    Args:
        parameter: The style parameter definition to validate.

    Raises:
        RuntimeError: If the validation fails.

    """

    if not (
            _check_discrete_parameter(parameter, float, int)
            or _check_continuous_parameter(parameter)
    ):
        raise RuntimeError(f"parameter not valid: {parameter}")


def validate_font_weight(parameter: StyleParameterConfiguration) -> None:
    """Validate the style parameter font-weight.

    Note:
        The following properties must be satisfied for a validation:
        type: discrete or continuous
        value: list of strings or continuous value definition

    Args:
        parameter: The style parameter definition to validate.

    Raises:
        RuntimeError: If the validation fails.

    """

    if not any(
            (
                    _check_discrete_parameter(parameter, float, int),
                    set(parameter["value"]).issubset(
                        ALLOWED_DISCRETE_VALUES_PER_PARAMETER[parameter["name"]]
                    ),
                    _check_continuous_parameter(parameter) or parameter["unit"] != "",
            ),
    ):
        raise RuntimeError(f"parameter not valid: {parameter}")


def validate_font_style(parameter: StyleParameterConfiguration) -> None:
    """Validate the style parameter font-style.

    Note:
        The following properties must be satisfied for a validation:
        type: discrete
        value: list of strings

    Args:
        parameter: The style parameter definition to validate.

    Raises:
        RuntimeError: If the validation fails.

    """

    if not (
            _check_discrete_parameter(parameter, str)
            and set(parameter["value"]).issubset(
        ALLOWED_DISCRETE_VALUES_PER_PARAMETER[parameter["name"]]
    )
            and (parameter["unit"] in ALLOWED_UNITS or not parameter["unit"])
    ):
        raise RuntimeError(f"parameter not valid: {parameter}")


def validate_text_decoration_line(parameter: StyleParameterConfiguration) -> None:
    """Validate the style parameter text-decoration.

    Note:
        The following properties must be satisfied for a validation:
        type: discrete
        value: list of strings

    Args:
        parameter: The style parameter definition to validate.

    Raises:
        RuntimeError: If the validation fails.

    """

    if not (
            _check_discrete_parameter(parameter, str)
            and set(parameter["value"]).issubset(
        ALLOWED_DISCRETE_VALUES_PER_PARAMETER[parameter["name"]]
    )
            and (parameter["unit"] in ALLOWED_UNITS or not parameter["unit"])
    ):
        raise RuntimeError(f"parameter not valid: {parameter}")


def validate_text_decoration_style(parameter: StyleParameterConfiguration) -> None:
    """Validate the style parameter text-decoration.

    Note:
        The following properties must be satisfied for a validation:
        type: discrete
        value: list of strings

    Args:
        parameter: The style parameter definition to validate.

    Raises:
        RuntimeError: If the validation fails.

    """

    if not (
            _check_discrete_parameter(parameter, str)
            and set(parameter["value"]).issubset(
        ALLOWED_DISCRETE_VALUES_PER_PARAMETER[parameter["name"]]
    )
            and (parameter["unit"] in ALLOWED_UNITS or not parameter["unit"])
    ):
        raise RuntimeError(f"parameter not valid: {parameter}")


def validate_text_transform(parameter: StyleParameterConfiguration) -> None:
    """Validate the style parameter text-transform.

    Note:
        The following properties must be satisfied for a validation:
        type: discrete
        value: list of strings

    Args:
        parameter: The style parameter definition to validate.

    Raises:
        RuntimeError: If the validation fails.

    """

    if not (
            _check_discrete_parameter(parameter, str)
            and set(parameter["value"]).issubset(
        ALLOWED_DISCRETE_VALUES_PER_PARAMETER[parameter["name"]]
    )
            and (parameter["unit"] in ALLOWED_UNITS or not parameter["unit"])
    ):
        raise RuntimeError(f"parameter not valid: {parameter}")


def validate_text_align(parameter: StyleParameterConfiguration) -> None:
    """Validate the style parameter text-align.

    Note:
        The following properties must be satisfied for a validation:
        type: discrete
        value: list of strings

    Args:
        parameter: The style parameter definition to validate.

    Raises:
        RuntimeError: If the validation fails.

    """

    if not (
            _check_discrete_parameter(parameter, str)
            and set(parameter["value"]).issubset(
        ALLOWED_DISCRETE_VALUES_PER_PARAMETER[parameter["name"]]
    )
            and (parameter["unit"] in ALLOWED_UNITS or not parameter["unit"])
    ):
        raise RuntimeError(f"parameter not valid: {parameter}")


def validate_letter_spacing(parameter: StyleParameterConfiguration) -> None:
    """Validate the style parameter letter-spacing.

    Note:
        The following properties must be satisfied for a validation:
        type: discrete or continuous
        value: list of strings or continuous value definition

    Args:
        parameter: The style parameter definition to validate.

    Raises:
        RuntimeError: If the validation fails.

    """

    if not (
            _check_discrete_parameter(parameter, float, int)
            or _check_continuous_parameter(parameter)
            and (parameter["unit"] in ALLOWED_UNITS or not parameter["unit"])
    ):
        raise RuntimeError(f"parameter not valid: {parameter}")


def validate_vertical_align(parameter: StyleParameterConfiguration) -> None:
    """Validate the style parameter vertical-align.

    Note:
        The following properties must be satisfied for a validation:
        type: discrete
        value: list of strings

    Args:
        parameter: The style parameter definition to validate.

    Raises:
        RuntimeError: If the validation fails.

    """

    if not (
            _check_discrete_parameter(parameter, str)
            and set(parameter["value"]).issubset(
        ALLOWED_DISCRETE_VALUES_PER_PARAMETER[parameter["name"]]
    )
            and (parameter["unit"] in ALLOWED_UNITS or not parameter["unit"])
    ):
        raise RuntimeError(f"parameter not valid: {parameter}")


def validate_padding(parameter: StyleParameterConfiguration) -> None:
    """Validate the style parameter padding.

    Note:
        The following properties must be satisfied for a validation:
        type: discrete or continuous
        value: list of strings or continuous value definition

    Args:
        parameter: The style parameter definition to validate.

    Raises:
        RuntimeError: If the validation fails.

    """

    if not (
            _check_discrete_parameter(parameter, float, int)
            or _check_continuous_parameter(parameter)
            and (parameter["unit"] in ALLOWED_UNITS or not parameter["unit"])
    ):
        raise RuntimeError(f"parameter not valid: {parameter}")


def validate_border_color(parameter: StyleParameterConfiguration) -> None:
    """Validate the style parameter border-color.

    Note:
        The following properties must be satisfied for a validation:
        type: discrete
        value: list of strings

    Args:
        parameter: The style parameter definition to validate.

    Raises:
        RuntimeError: If the validation fails.

    """

    if not _check_discrete_parameter(parameter, str):
        raise RuntimeError(f"parameter not valid: {parameter}")


def validate_border_style(parameter: StyleParameterConfiguration) -> None:
    """Validate the style parameter border-style.

    Note:
        The following properties must be satisfied for a validation:
        type: discrete
        value: list of strings

    Args:
        parameter: The style parameter definition to validate.

    Raises:
        RuntimeError: If the validation fails.

    """

    if not (
            _check_discrete_parameter(parameter, str)
            and set(parameter["value"]).issubset(
        ALLOWED_DISCRETE_VALUES_PER_PARAMETER[parameter["name"]]
    )
            and (parameter["unit"] in ALLOWED_UNITS or not parameter["unit"])
    ):
        raise RuntimeError(f"parameter not valid: {parameter}")


def validate_border_width(parameter: StyleParameterConfiguration) -> None:
    """Validate the style parameter border-width.

    Note:
        The following properties must be satisfied for a validation:
        type: discrete or continuous
        value: list of strings or continuous value definition

    Args:
        parameter: The style parameter definition to validate.

    Raises:
        RuntimeError: If the validation fails.

    """

    if not any(  # noqa: WPS337
            (
                    _check_continuous_parameter(parameter),
                    _check_discrete_parameter(parameter, float, int)
                    or (
                            values_match_any_type(parameter["value"], str)
                            and set(parameter["value"])
                            == ALLOWED_DISCRETE_VALUES_PER_PARAMETER[parameter["name"]]
                    )
                    and (parameter["unit"] in ALLOWED_UNITS or not parameter["unit"]),
            ),
    ):
        raise RuntimeError(f"parameter not valid: {parameter}")


def validate_border_spacing(parameter: StyleParameterConfiguration) -> None:
    """Validate the style parameter border-spacing.

    Note:
        The following properties must be satisfied for a validation:
        type: discrete or continuous
        value: list of strings or continuous value definition

    Args:
        parameter: The style parameter definition to validate.

    Raises:
        RuntimeError: If the validation fails.

    """

    if not (
            _check_discrete_parameter(parameter, float, int)
            or _check_continuous_parameter(parameter)
            and (parameter["unit"] in ALLOWED_UNITS or not parameter["unit"])
    ):
        raise RuntimeError(f"parameter not valid: {parameter}")


def validate_border_collapse(parameter: StyleParameterConfiguration) -> None:
    """Validate the style parameter border-collapse.

    Note:
        The following properties must be satisfied for a validation:
        type: discrete
        value: list of strings

    Args:
        parameter: The style parameter definition to validate.

    Raises:
        RuntimeError: If the validation fails.

    """

    if not (
            _check_discrete_parameter(parameter, str)
            and set(parameter["value"])
            == ALLOWED_DISCRETE_VALUES_PER_PARAMETER[parameter["name"]]
            and (parameter["unit"] in ALLOWED_UNITS or not parameter["unit"])
    ):
        raise RuntimeError(f"parameter not valid: {parameter}")


def validate_background_color(parameter: StyleParameterConfiguration) -> None:
    """Validate the style parameter background-color.

    Note:
        The following properties must be satisfied for a validation:
        type: discrete
        value: list of strings

    Args:
        parameter: The style parameter definition to validate.

    Raises:
        RuntimeError: If the validation fails.

    """

    if not _check_discrete_parameter(parameter, str):
        raise RuntimeError(f"parameter not valid: {parameter}")


def validate_background_color_alternating_row(
        parameter: StyleParameterConfiguration,
) -> None:
    """Validate the style parameter background-color for alternating row background-color.

    Note:
        The following properties must be satisfied for a validation:
        type: discrete
        value: list of strings

    Args:
        parameter: The style parameter definition to validate.

    Raises:
        RuntimeError: If the validation fails.

    """

    if (
            parameter["type"] != "discrete"
            or not values_match_any_type(parameter["value"], list)
            or len(parameter["value"]) < 2
            or not values_match_any_type(parameter["value"][0], str)
            or not values_match_any_type(parameter["value"][1], str)
    ):
        raise RuntimeError(f"parameter not valid: {parameter}")


def validate_background_color_alternating_column(
        parameter: StyleParameterConfiguration,
) -> None:
    """Validate the style parameter background-color for alternating column background-color.

    Note:
        The following properties must be satisfied for a validation:
        type: discrete
        value: list of strings

    Args:
        parameter: The style parameter definition to validate.

    Raises:
        RuntimeError: If the validation fails.

    """

    if (
            parameter["type"] != "discrete"
            or not values_match_any_type(parameter["value"], list)
            or len(parameter["value"]) < 2
            or not values_match_any_type(parameter["value"][0], str)
            or not values_match_any_type(parameter["value"][1], str)
    ):
        raise RuntimeError(f"parameter not valid: {parameter}")


def validate_color(parameter: StyleParameterConfiguration) -> None:
    """Validate the style parameter color.

    Note:
        The following properties must be satisfied for a validation:
        type: discrete
        value: list of strings

    Args:
        parameter: The style parameter definition to validate.

    Raises:
        RuntimeError: If the validation fails.

    """

    if not _check_discrete_parameter(parameter, str):
        raise RuntimeError(f"parameter not valid: {parameter}")


def validate_color_alternating_row(parameter: StyleParameterConfiguration) -> None:
    """Validate the style parameter color for alternating row color.

    Note:
        The following properties must be satisfied for a validation:
        type: discrete
        value: list of strings

    Args:
        parameter: The style parameter definition to validate.

    Raises:
        RuntimeError: If the validation fails.

    """

    if (
            parameter["type"] != "discrete"
            or not values_match_any_type(parameter["value"], list)
            or len(parameter["value"]) < 2
            or not values_match_any_type(parameter["value"][0], str)
            or not values_match_any_type(parameter["value"][1], str)
    ):
        raise RuntimeError(f"parameter not valid: {parameter}")


def validate_color_alternating_column(parameter: StyleParameterConfiguration) -> None:
    """Validate the style parameter color for alternating column color.

    Note:
        The following properties must be satisfied for a validation:
        type: discrete
        value: list of strings

    Args:
        parameter: The style parameter definition to validate.

    Raises:
        RuntimeError: If the validation fails.

    """

    if (
            parameter["type"] != "discrete"
            or not values_match_any_type(parameter["value"], list)
            or len(parameter["value"]) < 2
            or not values_match_any_type(parameter["value"][0], str)
            or not values_match_any_type(parameter["value"][1], str)
    ):
        raise RuntimeError(f"parameter not valid: {parameter}")


def validate_margin_top(parameter: StyleParameterConfiguration) -> None:
    """Validate the style parameter margin-top.

    Note:
        The following properties must be satisfied for a validation:
        type: discrete or continuous
        value: list of strings or continuous value definition

    Args:
        parameter: The style parameter definition to validate.

    Raises:
        RuntimeError: If the validation fails.

    """

    if not (
            _check_discrete_parameter(parameter, float, int)
            or _check_continuous_parameter(parameter)
            and (parameter["unit"] in ALLOWED_UNITS or not parameter["unit"])
    ):
        raise RuntimeError(f"parameter not valid: {parameter}")


def validate_margin_bottom(parameter: StyleParameterConfiguration) -> None:
    """Validate the style parameter margin-bottom.

    Note:
        The following properties must be satisfied for a validation:
        type: discrete or continuous
        value: list of strings or continuous value definition

    Args:
        parameter: The style parameter definition to validate.

    Raises:
        RuntimeError: If the validation fails.

    """

    if not (
            _check_discrete_parameter(parameter, float, int)
            or _check_continuous_parameter(parameter)
            and (parameter["unit"] in ALLOWED_UNITS or not parameter["unit"])
    ):
        raise RuntimeError(f"parameter not valid: {parameter}")


def validate_margin_left(parameter: StyleParameterConfiguration) -> None:
    """Validate the style parameter margin-left.

    Note:
        The following properties must be satisfied for a validation:
        type: discrete or continuous
        value: list of strings or continuous value definition

    Args:
        parameter: The style parameter definition to validate.

    Raises:
        RuntimeError: If the validation fails.

    """

    if not (
            _check_discrete_parameter(parameter, float, int)
            or _check_continuous_parameter(parameter)
            and (parameter["unit"] in ALLOWED_UNITS or not parameter["unit"])
    ):
        raise RuntimeError(f"parameter not valid: {parameter}")


def validate_margin_right(parameter: StyleParameterConfiguration) -> None:
    """Validate the style parameter margin-right.

    Note:
        The following properties must be satisfied for a validation:
        type: discrete or continuous
        value: list of strings or continuous value definition

    Args:
        parameter: The style parameter definition to validate.

    Raises:
        RuntimeError: If the validation fails.

    """

    if not (
            _check_discrete_parameter(parameter, float, int)
            or _check_continuous_parameter(parameter)
            and (parameter["unit"] in ALLOWED_UNITS or not parameter["unit"])
    ):
        raise RuntimeError(f"parameter not valid: {parameter}")


def validate_table_height(parameter: StyleParameterConfiguration) -> None:
    """Validate the style parameter height.

    Note:
        The following properties must be satisfied for a validation:
        type: discrete or continuous
        value: list of strings or continuous value definition

    Args:
        parameter: The style parameter definition to validate.

    Raises:
        RuntimeError: If the validation fails.

    """

    if not (
            _check_discrete_parameter(parameter, float, int)
            or _check_continuous_parameter(parameter)
            and (parameter["unit"] in ALLOWED_UNITS or not parameter["unit"])
    ):
        raise RuntimeError(f"parameter not valid: {parameter}")


def validate_table_width(parameter: StyleParameterConfiguration) -> None:
    """Validate the style parameter height.

    Note:
        The following properties must be satisfied for a validation:
        type: discrete or continuous
        value: list of strings or continuous value definition

    Args:
        parameter: The style parameter definition to validate.

    Raises:
        RuntimeError: If the validation fails.

    """

    if not (
            _check_discrete_parameter(parameter, float, int)
            or _check_continuous_parameter(parameter)
            and (parameter["unit"] in ALLOWED_UNITS or not parameter["unit"])
    ):
        raise RuntimeError(f"parameter not valid: {parameter}")


def validate_table_value_limit(table_value_limit: int) -> None:
    """Validate the config parameter table_value_limit.

    Note:
        The following properties must be satisfied for a validation:
        value: int > 0

    Args:
         table_value_limit: the config parameter to validate.

    Raises:
        RuntimeError: If the validation fails.

    """

    if not (isinstance(table_value_limit, int) and table_value_limit > 0):
        raise RuntimeError(f"parameter not valid: {table_value_limit}")


def validate_gen_modes_odds(gen_modes_odds: Dict[str, float]) -> None:
    """Validate the config parameter generation_modes_odds.

    Note:
        The following properties must be satisfied for a validation:
        value: mapping from str to float

    Args:
         gen_modes_odds: the config parameter to validate.

    Raises:
        RuntimeError: If the validation fails.

    """

    if not (
            values_match_any_type(gen_modes_odds.keys(), str)
            and values_match_any_type(gen_modes_odds.values(), float)
    ):
        raise RuntimeError(f"parameter not valid: {gen_modes_odds}")


def validate_gt_odds_per_mode(gt_odds: Dict[str, float]) -> None:
    """Validate the config parameter ft_odds_per_mode.

    Note:
        The following properties must be satisfied for a validation:
        value: mapping from str to float

    Args:
         gt_odds: the config parameter to validate.

    Raises:
        RuntimeError: If the validation fails.

    """

    if not (
            values_match_any_type(gt_odds.keys(), str)
            and values_match_any_type(gt_odds.values(), float)
    ):
        raise RuntimeError(f"parameter not valid: {gt_odds}")


def validate_number_of_columns_odds(number_of_columns_odds: Dict[str, int]) -> None:
    """Validate the config parameter number_of_columns_odds.

    Note:
        The following properties must be satisfied for a validation:
        value: mapping from str to float

    Args:
        number_of_columns_odds: the config parameter to validate.

    Raises:
        RuntimeError: If the validation fails.

    """

    if not (
            values_match_any_type(number_of_columns_odds.keys(), str)
            and values_match_any_type(number_of_columns_odds.values(), float)
    ):
        raise RuntimeError(f"parameter not valid: {number_of_columns_odds}")


def validate_row_manipulation_odds(row_manipulation_odds: float) -> None:
    """Validate the config parameter row_manipulation_odds.

    Note:
        The following properties must be satisfied for a validation:
        value: floating point <= 1.0

    Args:
        row_manipulation_odds: the config parameter to validate.

    Raises:
        RuntimeError: If the validation fails.

    """

    if not (
            isinstance(row_manipulation_odds, float)
            and 0.0 <= row_manipulation_odds <= 1.0  # noqa WPS459
    ):
        raise RuntimeError(f"parameter not valid: {row_manipulation_odds}")


def validate_has_header(parameter: StyleParameterConfiguration) -> None:
    """Validate the structure parameter has-header.

    Note:
        The following properties must be satisfied for a validation:
        type: discrete
        value: list of strings

    Args:
        parameter: The style parameter definition to validate.

    Raises:
        RuntimeError: If the validation fails.

    """

    if not _check_discrete_parameter(parameter, bool):
        raise RuntimeError(f"parameter not valid: {parameter}")


def validate_min_table_length(min_table_length: int) -> None:
    """Validate the parameter min_table_length.

    Note:
        The following properties must be satisfied for a validation:
        type: int
        value: >= 0

    Args:
        min_table_length: the min_table_length value to validate.

    Raises:
        RuntimeError: If the validation fails.

    """

    if not (isinstance(min_table_length, int) and min_table_length >= 0):
        raise RuntimeError(f"parameter not valid: {min_table_length}")


def validate_max_table_length(max_table_length: int) -> None:
    """Validate the parameter max_table_length.

    Note:
        The following properties must be satisfied for a validation:
        type: int
        value: >= 0

    Args:
        max_table_length: the max_table_length value to validate.

    Raises:
        RuntimeError: If the validation fails.

    """

    if not (isinstance(max_table_length, int) and max_table_length >= 0):
        raise RuntimeError(f"parameter not valid: {max_table_length}")


def validate_do_complex_values(do_complex_values: str) -> None:
    if not isinstance(do_complex_values, str) and do_complex_values.lower() not in ["true", "false"]:
        raise RuntimeError(f"parameter not valid: {do_complex_values}")


def validate_complex_values_chance(complex_values_chance: float) -> None:
    if not isinstance(complex_values_chance, float) and 0.0 <= complex_values_chance <= 1.0:
        raise RuntimeError(f"parameter not valid: {complex_values_chance}")


def validate_jpg_quality(jpg_quality: int) -> None:
    """Validate the config parameter jpg_quality.

    Note:
        The following properties must be satisfied for a validation:
        type: int
        value: 0 <= jpg_quality <= 100

    Args:
        jpg_quality: the jpg_quality value to validate.

    Raises:
        RuntimeError: If the validation fails.

    """

    if not (isinstance(jpg_quality, int) and 0 <= jpg_quality <= 100):
        raise RuntimeError(f"parameter not valid: {jpg_quality}")


def validate_image_height(height: int) -> None:
    """Validate the structure parameter .

    Note:
        The following properties must be satisfied for a validation:
        type: int
        value: > 0

    Args:
        height: the image_height value to validate.

    Raises:
        RuntimeError: If the validation fails.

    """

    if not (isinstance(height, int) and height > 0):
        raise RuntimeError(f"parameter not valid: {height}")


def validate_image_width(width: int) -> None:
    """Validate the structure parameter .

    Note:
        The following properties must be satisfied for a validation:
        type: int
        value: > 0

    Args:
        width: the image_width value to validate.

    Raises:
        RuntimeError: If the validation fails.

    """

    if not (isinstance(width, int) and width > 0):
        raise RuntimeError(f"parameter not valid: {width}")


def validate_table_orientation(parameter: StyleParameterConfiguration) -> None:
    """Validate the structure parameter table-orientation.

    Note:
        The following properties must be satisfied for a validation:
        type: discrete
        value: list of strings

    Args:
        parameter: The style parameter definition to validate.

    Raises:
        RuntimeError: If the validation fails.

    """

    if not (
            _check_discrete_parameter(parameter, str)
            and set(parameter["value"]).issubset(
        ALLOWED_DISCRETE_VALUES_PER_PARAMETER[parameter["name"]]
    )
    ):
        raise RuntimeError(f"parameter not valid: {parameter}")


def validate_number_of_tables(number_of_tables: int) -> None:
    """Validate the config parameter number_of_tables.

    Note:
        The following properties must be satisfied for a validation:
        type: int

    Args:
        number_of_tables: the config parameter to validate.

    Raises:
        RuntimeError: If the validation fails.

    """

    if not (isinstance(number_of_tables, int) and number_of_tables > 0):
        raise RuntimeError(f"parameter not valid: {number_of_tables}")


def validate_keyword_chance(keyword_chance: float) -> None:
    """Validate the config parameter keyword_chance.

    Note:
        The following properties must be satisfied for a validation:
        type: float
        value: 0 <= key_chace <= 100

    Args:
        keyword_chance: the config parameter to validate.

    Raises:
        RuntimeError: If the validation fails.

    """

    if not (isinstance(keyword_chance, float) and 0.0 <= keyword_chance <= 1.0):
        raise RuntimeError(f"parameter not valid: {keyword_chance}")


def validate_blur_manipulation(parameter: StyleParameterConfiguration) -> None:
    """Validate the integrity of blur values.

    Note:
        The following properties must be satisfied for a validation:
        type: discrete or continuous
        value: list of strings or continuous value definition
        values must be odd

    Args:
        parameter: The style parameter definition to validate.

    Raises:
        RuntimeError: If the validation fails.

    """
    if not (
            _check_discrete_parameter(parameter, float, int)
            or _check_continuous_parameter(parameter)
    ):
        raise RuntimeError(f"parameter not valid: {parameter}")

    if (
            parameter["type"] == "continuous"
            and not all(
        value % 2 == 1
        for value in range(
            parameter["value"]["start"],
            parameter["value"]["stop"],
            parameter["value"]["stop"],
        )
    )
            or (
            parameter["type"] == "discrete"
            and not all(value % 2 == 1 for value in parameter)
    )
    ):
        raise RuntimeError(f"blur values need to be odd")


def validate_image_effect(parameter: StyleParameterConfiguration) -> None:
    """Validate the integrity of blur values.

    Note:
        The following properties must be satisfied for a validation:
        type: discrete or continuous
        value: list of strings or continuous value definition
        values must be odd

    Args:
        parameter: The style parameter definition to validate.

    Raises:
        RuntimeError: If the validation fails.

    """
    if not (
            _check_discrete_parameter(parameter, float, int)
            or _check_continuous_parameter(parameter)
    ):
        raise RuntimeError(f"parameter not valid: {parameter}")


def validate_image_manipulation_probability(value: float) -> None:
    """Validate the config parameter image_manipulation_probability.

    Note:
        The following properties must be satisfied for a validation:
        type: float
        value: 0 <= key_chace <= 100

    Args:
        value: the config parameter to validate.

    Raises:
        RuntimeError: If the validation fails.

    """

    if not (isinstance(float(value), float) and 0.0 <= value <= 1.0):
        raise RuntimeError(f"parameter not valid: {value}")


def validate_semantic_word_replacement_min_similarity(value: float) -> None:
    """Validate the config parameter semantic_word_replacement_min_similarity.

    Note:
        The following properties must be satisfied for a validation:
        type: float
        value: 0.0 <= value <= 1.0

    Args:
        value: the config parameter to validate.

    Raises:
        RuntimeError: If the validation fails.

    """

    if not (isinstance(value, float) and 0.0 <= value <= 1.0):
        raise RuntimeError(f"parameter not valid: {value}")


def validate_semantic_word_replacement_max_similarity(value: float) -> None:
    """Validate the config parameter semantic_word_replacement_max_similarity.

    Note:
        The following properties must be satisfied for a validation:
        type: float
        value: 0.0 <= value <= 1.0

    Args:
        value: the config parameter to validate.

    Raises:
        RuntimeError: If the validation fails.

    """

    if not (isinstance(value, float) and 0.0 <= value <= 1.0):
        raise RuntimeError(f"parameter not valid: {value}")


def validate_max_number_spaces(value: int) -> None:
    """Validate the config parameter max_number_spaces.

    Note:
        The following properties must be satisfied for a validation:
        type: int
        value: 1 <= value

    Args:
        value: the config parameter to validate.

    Raises:
        RuntimeError: If the validation fails.

    """

    if not (isinstance(value, int) and value >= 1):
        raise RuntimeError(f"parameter not valid: {value}")


PARAMETER_VALIDATORS: Dict[str, Callable[[StyleParameterConfiguration], None]] = {
    "font-family": validate_font_family,
    "font-size": validate_font_size,
    "font-weight": validate_font_weight,
    "font-style": validate_font_family,
    "text-decoration-line": validate_text_decoration_line,
    "text-decoration-style": validate_text_decoration_style,
    "text-transform": validate_text_transform,
    "text-align": validate_text_align,
    "letter-spacing": validate_letter_spacing,
    "vertical-align": validate_vertical_align,
    "padding": validate_padding,
    "border-color": validate_border_color,
    "border-style": validate_border_style,
    "border-width": validate_border_width,
    "border-spacing": validate_border_spacing,
    "border-collapse": validate_border_collapse,
    "background-color": validate_background_color,
    "background-color-alternating-row": validate_background_color_alternating_row,
    "background-color-alternating-column": validate_background_color_alternating_column,
    "color": validate_color,
    "color-alternating-row": validate_color_alternating_row,
    "color-alternating-column": validate_color_alternating_column,
    "width": validate_table_width,
    "height": validate_table_height,
    "margin-top": validate_margin_top,
    "margin-bottom": validate_margin_bottom,
    "margin-left": validate_margin_left,
    "margin-right": validate_margin_right,
}

"""
Holds all style parameter validators defined in config_validator.py.

:meta hide-value:
"""

STRUCTURE_PARAMETER_VALIDATORS: Dict[
    str,
    Callable[[StyleParameterConfiguration], None],
] = {
    "has-header": validate_has_header,
    "table-orientation": validate_table_orientation,
}

"""
Holds all structure parameter validators defined in config_validator.py.

:meta hide-value:
"""
IMAGE_MANIPULATORS_VALIDATORS: Dict[
    str,
    Callable[[StyleParameterConfiguration], None],
] = {
    "blur": validate_blur_manipulation,
    "contrast": validate_image_effect,
    "brightness": validate_image_effect,
    "sharpness": validate_image_effect,
    "noise": validate_image_effect,
}
"""
Holds all image effect validators defined in config_validator.py.

:meta hide-value:
"""
TOP_LEVEL_KEY_VALIDATORS: Dict[str, Callable[[Any], None]] = {
    "seed": validate_seed,
    "parameters": validate_parameter,
    "table_value_limit": validate_table_value_limit,
    "generation_modes_odds": validate_gen_modes_odds,
    "gt_odds_per_mode": validate_gt_odds_per_mode,
    "number_of_columns_odds": validate_number_of_columns_odds,
    "row_manipulation_odds": validate_row_manipulation_odds,
    "structure_parameters": validate_structure_parameter,
    "image_manipulators": validate_image_manipulators,
    "min_table_length": validate_min_table_length,
    "max_table_length": validate_max_table_length,
    "do_complex_values": validate_do_complex_values,
    "complex_values_chance": validate_complex_values_chance,
    "jpg_quality": validate_jpg_quality,
    "image_height": validate_image_height,
    "image_width": validate_image_width,
    "number_of_tables": validate_number_of_tables,
    "keyword_chance": validate_keyword_chance,
    "image_manipulation_probability": validate_image_manipulation_probability,
    "semantic_word_replacement_min_similarity": validate_semantic_word_replacement_min_similarity,
    "semantic_word_replacement_max_similarity": validate_semantic_word_replacement_max_similarity,
    "max_number_spaces": validate_max_number_spaces,
}

"""
Holds all top level config key validators defined in config_validator.py.

:meta hide-value:
"""

ALLOWED_DISCRETE_VALUES_PER_PARAMETER: Dict[str, Set[str]] = {
    "font-weight": {
        "normal",
        "bold",
        "lighter",
        "bolder",
    },
    "font-style": {
        "normal",
        "italic",
        "oblique",
    },
    "text-decoration-line": {
        "overline",
        "underline",
        "line-through",
        "blink",
        "none",
    },
    "text-decoration-style": {
        "solid",
        "double",
        "dotted",
        "dashed",
        "wavy",
    },
    "text-transform": {
        "capitalize",
        "uppercase",
        "lowercase",
        "full-width",
        "none",
    },
    "text-align": {
        "left",
        "right",
        "center",
        "justify",
        "justify-all",
        "start",
        "end",
        "match-parent",
    },
    "vertical-align": {
        "baseline",
        "sub",
        "super",
        "text-top",
        "text-bottom",
        "middle",
        "top",
        "bottom",
    },
    "border-style": {
        "none",
        "hidden",
        "dotted",
        "dashed",
        "solid",
        "double",
        "groove",
        "ridge",
        "inset",
        "outset",
    },
    "border-width": {
        "thin",
        "medium",
        "thick",
    },
    "border-collapse": {
        "collapse",
        "separate",
    },
    "table-orientation": {
        "horizontal",
        "vertical",
    },
}

"""
Holds allowed values per restricted style parameters in config_validator.py.

:meta hide-value:
"""

ALLOWED_UNITS: List[str] = ["px", "pt", "pc", "em", "rem", "mm", "cm", "in"]
"""A list of allowed units to specify for style transformers."""


def _check_discrete_parameter(
        parameter: StyleParameterConfiguration,
        *types: Any,
) -> bool:
    """Validate the structure of a discrete parameter value.

    Args:
        parameter: The parameter to validate.
        types: The allowed types_ for the parameter.

    Returns:
        True if the validation succeeded, False otherwise.

    """
    return (
            parameter["type"] == "discrete"
            and not isinstance(parameter["value"], dict)
            and values_match_any_type(
        parameter["value"],
        types,
    )
    )


def _check_continuous_parameter(parameter: StyleParameterConfiguration) -> bool:
    """Validate the structure of a continuous parameter value.

    Args:
        parameter: The parameter to validate.

    Returns:
        True if the validation succeeded, False otherwise.

    """
    return parameter["type"] == "continuous" and (
            "start" in parameter["value"] and "stop" in parameter["value"]
    )
