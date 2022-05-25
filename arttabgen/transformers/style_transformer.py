"""Holds functions to visually manipulate tables, acting as *style transformers*.

STYLE_TRANSFORMERS: A list of all defined *style transformers*.
"""

from typing import Callable, Dict, List, Union


def transformer_font_family(
        parameter_value: Union[int, float, str],
        parameter_unit: str,
) -> str:
    """Return a CSS Declaration with a font-family.

    Args:
        parameter_value: A list to choose fonts from.
        parameter_unit: unit to be used in the CSS declaration

    Returns:
        str: A CSS declaration setting a font-family.

    """

    return f"table, tr, td {{font-family: {parameter_value}{parameter_unit};}}"


def transformer_font_size(
        parameter_value: Union[int, float, str],
        parameter_unit: str,
) -> str:
    """Return a CSS Declaration with a font-size.

    Args:
        parameter_value: A list to choose font sizes from or a definition of a continuous value range.
        parameter_unit: unit to be used in the CSS declaration

    Returns:
        str: A CSS declaration setting a font-size.

    """

    return f"table, tr, td {{font-size: {parameter_value}{parameter_unit};}}"


def transformer_font_weight(
        parameter_value: Union[int, float, str],
        parameter_unit: str,
) -> str:
    """Return a CSS Declaration with a font-weight.

    Args:
        parameter_value: A list to choose font weights from or a definition of a continuous value range.
        parameter_unit: unit to be used in the CSS declaration

    Returns:
        str: A CSS declaration setting a font-weight.

    """

    return f"table, tr, td {{font-weight: {parameter_value}{parameter_unit};}}"


def transformer_font_style(
        parameter_value: Union[int, float, str],
        parameter_unit: str,
) -> str:
    """Return a CSS Declaration with a font-style.

    Args:
        parameter_value: A list to choose font styles from.
        parameter_unit: unit to be used in the CSS declaration

    Returns:
        str: A CSS declaration setting a font-style.

    """

    return f"table, tr, td {{font-style: {parameter_value}{parameter_unit};}}"


def transformer_border_collapse(
        parameter_value: Union[int, float, str],
        parameter_unit: str,
) -> str:
    """Return a CSS Declaration with a border-collapse value.

    Args:
        parameter_value: A list to choose values from.
        parameter_unit: unit to be used in the CSS declaration

    Returns:
        str: A CSS declaration setting a border-collapse value.

    """

    return f"table, tr, td {{border-collapse: {parameter_value}{parameter_unit};}}"


def transformer_border_spacing(
        parameter_value: Union[int, float, str],
        parameter_unit: str,
) -> str:
    """Return a CSS Declaration with a border spacing.

    Args:
        parameter_value: A list to choose border spacings from or a definition of a continuous value range.
        parameter_unit: unit to be used in the CSS declaration

    Returns:
        str: A CSS declaration setting a border-spacing.

    """

    return f"table, tr, td {{border-spacing: {parameter_value}{parameter_unit};}}"


def transformer_border_width(
        parameter_value: Union[int, float, str],
        parameter_unit: str,
) -> str:
    """Return a CSS Declaration with a border width.

    Args:
        parameter_value: A list to choose border widths from or a definition of a continuous value range.
        parameter_unit: unit to be used in the CSS declaration

    Returns:
        str: A CSS declaration setting a border-width.

    """

    return f"table, tr, td {{border-width: {parameter_value}{parameter_unit};}}"


def transformer_border_style(
        parameter_value: Union[int, float, str],
        parameter_unit: str,
) -> str:
    """Return a CSS Declaration with a border-style value.

    Args:
        parameter_value: A list to choose values from.
        parameter_unit: unit to be used in the CSS declaration

    Returns:
        str: A CSS declaration setting a border-style value.

    """

    return f"table, tr, td {{border-style: {parameter_value}{parameter_unit};}}"


def transformer_border_color(
        parameter_value: Union[int, float, str],
        parameter_unit: str,
) -> str:
    """Return a CSS Declaration with a border-color value.

    Args:
        parameter_value: A list to choose values from.
        parameter_unit: unit to be used in the CSS declaration

    Returns:
        str: A CSS declaration setting a border-color value.

    """

    return f"table, tr, td {{border-color: {parameter_value}{parameter_unit};}}"


def transformer_text_transform(
        parameter_value: Union[int, float, str],
        parameter_unit: str,
) -> str:
    """Return a CSS Declaration with a text-transform value.

    Args:
        parameter_value: A list to choose values from.
        parameter_unit: unit to be used in the CSS declaration

    Returns:
        str: A CSS declaration setting a text-transform value.

    """

    return f"table, tr, td {{text-transform: {parameter_value}{parameter_unit};}}"


def transformer_text_align(
        parameter_value: Union[int, float, str],
        parameter_unit: str,
) -> str:
    """Return a CSS Declaration with a text-align value.

    Args:
        parameter_value: A list to choose values from.
        parameter_unit: unit to be used in the CSS declaration

    Returns:
        str: A CSS declaration setting a text-align value.

    """

    return f"table, tr, td {{text-align: {parameter_value}{parameter_unit};}}"


def transformer_letter_spacing(
        parameter_value: Union[int, float, str],
        parameter_unit: str,
) -> str:
    """Return a CSS Declaration with a letter-spacing value.

    Args:
        parameter_value: A list to choose values from.
        parameter_unit: unit to be used in the CSS declaration

    Returns:
        str: A CSS declaration setting a letter-spacing value.

    """

    return f"table, tr, td {{letter-spacing: {parameter_value}{parameter_unit};}}"


def transformer_vertical_align(
        parameter_value: Union[int, float, str],
        parameter_unit: str,
) -> str:
    """Return a CSS Declaration with a vertical-align value.

    Args:
        parameter_value: A list to choose values from.
        parameter_unit: unit to be used in the CSS declaration

    Returns:
        str: A CSS declaration setting a vertical-align value.

    """

    return f"table, tr, td {{vertical-align: {parameter_value}{parameter_unit};}}"


def transformer_text_decoration_line(
        parameter_value: Union[int, float, str],
        parameter_unit: str,
) -> str:
    """Return a CSS Declaration with a text-decoration-line value.

    Args:
        parameter_value: A list to choose values from.
        parameter_unit: unit to be used in the CSS declaration

    Returns:
        str: A CSS declaration setting a text-decoration-line value.

    """

    return f"table, tr, td {{text-decoration-line: {parameter_value}{parameter_unit};}}"


def transformer_text_decoration_style(
        parameter_value: Union[int, float, str],
        parameter_unit: str,
) -> str:
    """Return a CSS Declaration with a text-decoration-style value.

    Args:
        parameter_value: A list to choose values from.
        parameter_unit: unit to be used in the CSS declaration

    Returns:
        str: A CSS declaration setting a text-decoration-style value.

    """

    return f"table, tr, td {{text-decoration-style: {parameter_value}{parameter_unit};}}"


def transformer_padding(
        parameter_value: Union[int, float, str],
        parameter_unit: str,
) -> str:
    """Return a CSS Declaration with a cell padding value.

    Args:
        parameter_value: A list to choose values from.
        parameter_unit: unit to be used in the CSS declaration

    Returns:
        str: A CSS declaration setting a padding value.

    """

    return f"td {{padding: {parameter_value}{parameter_unit};}}"


def transformer_margin_left(
        parameter_value: Union[int, float, str],
        parameter_unit: str,
) -> str:
    """Return a CSS Declaration with a left margin value for the table.

    Args:
        parameter_value: A list to choose values from.
        parameter_unit: unit to be used in the CSS declaration

    Returns:
        str: A CSS declaration setting a left margin value for the table.

    """

    return f"table {{margin-left: {parameter_value}{parameter_unit};}}"


def transformer_margin_right(
        parameter_value: Union[int, float, str],
        parameter_unit: str,
) -> str:
    """Return a CSS Declaration with a right margin value for the table.

    Args:
        parameter_value: A list to choose values from.
        parameter_unit: unit to be used in the CSS declaration

    Returns:
        str: A CSS declaration setting a right margin value for the table.

    """

    return f"table {{margin-right: {parameter_value}{parameter_unit};}}"


def transformer_margin_top(
        parameter_value: Union[int, float, str],
        parameter_unit: str,
) -> str:
    """Return a CSS Declaration with a top margin value for the table.

    Args:
        parameter_value: A list to choose values from.
        parameter_unit: unit to be used in the CSS declaration

    Returns:
        str: A CSS declaration setting a top margin value for the table.

    """

    return f"table {{margin-top: {parameter_value}{parameter_unit};}}"


def transformer_margin_bottom(
        parameter_value: Union[int, float, str],
        parameter_unit: str,
) -> str:
    """Return a CSS Declaration with a bottom margin value for the table.

    Args:
        parameter_value: A list to choose values from.
        parameter_unit: unit to be used in the CSS declaration

    Returns:
        str: A CSS declaration setting a bottom margin value for the table.

    """

    return f"table {{margin-bottom: {parameter_value}{parameter_unit};}}"


def transformer_table_width(
        parameter_value: Union[int, float, str],
        parameter_unit: str,
) -> str:
    """Return a CSS Declaration with a width value for the table.

    Args:
        parameter_value: A list to choose values from.
        parameter_unit: unit to be used in the CSS declaration

    Returns:
        str: A CSS declaration setting a width value for the table.

    """

    return f"table {{width: {parameter_value}{parameter_unit};}}"


def transformer_table_height(
        parameter_value: Union[int, float, str],
        parameter_unit: str,
) -> str:
    """Return a CSS Declaration with a height value for the table.

    Args:
        parameter_value: A list to choose values from.
        parameter_unit: unit to be used in the CSS declaration

    Returns:
        str: A CSS declaration setting a height value for the table.

    """

    return f"table {{height: {parameter_value}{parameter_unit};}}"


def transformer_background_color(
        parameter_value: Union[int, float, str],
        parameter_unit: str,
) -> str:
    """Return a CSS Declaration with a background color for the table.

    Args:
        parameter_value: A list to choose values from.
        parameter_unit: unit to be used in the CSS declaration

    Returns:
        str: A CSS declaration setting a background color for the table.

    """

    return f"td {{background-color: {parameter_value}{parameter_unit};}}"


def transformer_color(
        parameter_value: Union[int, float, str],
        parameter_unit: str,
) -> str:
    """Return a CSS Declaration with a color for the table.

    Args:
        parameter_value: A list to choose values from.
        parameter_unit: unit to be used in the CSS declaration

    Returns:
        str: A CSS declaration setting a color for the table.

    """

    return f"td {{color: {parameter_value}{parameter_unit};}}"


def transformer_color_alternating_row(
        parameter_value: List[Union[int, float, str]],
        parameter_unit: str,
) -> str:
    """Return a CSS Declaration with two random, alternating colors for the table rows.

    Args:
        parameter_value: A list to choose values from.
        parameter_unit: unit to be used in the CSS declaration

    Returns:
        str: A CSS declaration setting two random, alternating colors for the table rows.

    """

    color1 = parameter_value[0]
    color2 = parameter_value[1]

    return (
            f"tr:nth-child(even) {{color: {color1};}}\n"
            + f"tr:nth-child(odd) {{color: {color2};}}"
    )


def transformer_color_alternating_column(
        parameter_value: List[Union[int, float, str]],
        parameter_unit: str,
) -> str:
    """Return a CSS Declaration with two random, alternating colors for the table columns.

    Args:
        parameter_value: A list to choose values from.
        parameter_unit: unit to be used in the CSS declaration

    Returns:
        str: A CSS declaration setting two random, alternating colors for the table columns.

    """

    color1 = parameter_value[0]
    color2 = parameter_value[1]

    return (
            f"td:nth-child(even) {{color: {color1};}}\n"
            + f"td:nth-child(odd) {{color: {color2};}}"
    )


def transformer_background_color_alternating_row(
        parameter_value: List[Union[int, float, str]],
        parameter_unit: str,
) -> str:
    """Return a CSS Declaration with two random, alternating background colors for the table rows.

    Args:
        parameter_value: A list to choose values from.
        parameter_unit: unit to be used in the CSS declaration

    Returns:
        str: A CSS declaration setting two random, alternating background colors for the table rows.

    """

    color1 = parameter_value[0]
    color2 = parameter_value[1]

    return (
            f"tr:nth-child(even) {{background-color: {color1};}}\n"
            + f"tr:nth-child(odd) {{background-color: {color2};}}"
    )


def transformer_background_color_alternating_column(
        parameter_value: List[Union[int, float, str]],
        parameter_unit: str,
) -> str:
    """Return a CSS Declaration with two random, alternating background colors for the table columns.

    Args:
        parameter_value: A list to choose values from.
        parameter_unit: unit to be used in the CSS declaration

    Returns:
        str: A CSS declaration setting two random, alternating background colors for the table columns.

    """

    color1 = parameter_value[0]
    color2 = parameter_value[1]

    return (
            f"td:nth-child(even) {{background-color: {color1};}}\n"
            + f"td:nth-child(odd) {{background-color: {color2};}}"
    )


STYLE_TRANSFORMERS: Dict[
    str,
    Callable[[Union[List[Union[int, float, str]], Union[int, float, str]], str], str],
] = {
    "font-family": transformer_font_family,
    "font-size": transformer_font_size,
    "font-style": transformer_font_style,
    "font-weight": transformer_font_weight,
    "border-collapse": transformer_border_collapse,
    "border-spacing": transformer_border_spacing,
    "border-width": transformer_border_width,
    "border-style": transformer_border_style,
    "border-color": transformer_border_color,
    "text-transform": transformer_text_transform,
    "text-align": transformer_text_align,
    "letter-spacing": transformer_letter_spacing,
    "vertical-align": transformer_vertical_align,
    "text-decoration-line": transformer_text_decoration_line,
    "text-decoration-style": transformer_text_decoration_style,
    "padding": transformer_padding,
    "margin-left": transformer_margin_left,
    "margin-right": transformer_margin_right,
    "margin-top": transformer_margin_top,
    "margin-bottom": transformer_margin_bottom,
    "width": transformer_table_width,
    "height": transformer_table_height,
    "background-color": transformer_background_color,
    "background-color-alternating-row": transformer_background_color_alternating_row,
    "background-color-alternating-column": transformer_background_color_alternating_column,
    "color": transformer_color,
    "color-alternating-row": transformer_color_alternating_row,
    "color-alternating-column": transformer_color_alternating_column,
}
"""Holds all defined *style transformers*."""
