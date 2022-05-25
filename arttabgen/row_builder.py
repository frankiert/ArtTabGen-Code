"""Holds functions to build table rows.

ROW_BUILDERS: A list of all functions.
"""

import random
from typing import Callable, List

from arttabgen.helper import Row


def build_1_col_kuv(key: str, value: str, unit: str) -> Row:
    """Build a table row with 1 column in the format |<key> <unit> <value>|.

    Args:
        key: A keyword to associate a values with
        value: A value to associate with a key
        unit: A unit to associate with the value

    Returns:
        A row holding the specified key, value and unit.

    """

    return [f"{key} {unit} {value}"]


def build_1_col_kvu(key: str, value: str, unit: str) -> Row:
    """Build a table row with 1 column the format |<key> <value> <unit>|.

    Args:
        key: A keyword to associate a values with
        value: A value to associate with a key
        unit: A unit to associate with the value

    Returns:
        A row holding the specified key, value and unit.

    """

    return [f"{key} {value} {unit}"]


def build_2_cols_square_brackets(key: str, value: str, unit: str) -> Row:
    """Build a table row with 2 columns and the format |<key> [<unit>]|<value>|.

    Args:
        key: A keyword to associate a values with
        value: A value to associate with a key
        unit: A unit to associate with the value

    Returns:
        A row holding the specified key, value and unit.

    """

    return [f"{key}, [{unit}]", value]


def build_2_cols_round_brackets(key: str, value: str, unit: str) -> Row:
    """Build a table row with 2 columns and the format |<key> (<unit>)|<value>|.

    Args:
        key: A keyword to associate a values with
        value: A value to associate with a key
        unit: A unit to associate with the value

    Returns:
        A row holding the specified key, value and unit.

    """

    return [f"{key} ({unit})", value]


def build_2_cols_comma(key: str, value: str, unit: str) -> Row:
    """Build a table row with 2 columns and the format |<key>, <unit>|<value>|.

    Args:
        key: A keyword to associate a values with
        value: A value to associate with a key
        unit: A unit to associate with the value

    Returns:
        A row holding the specified key, value and unit.

    """

    return [f"{key}, {unit}", value]


def build_2_cols_space(key: str, value: str, unit: str) -> Row:
    """Build a table row with 2 columns and the format |<key>|<value> <unit>|.

    Args:
        key: A keyword to associate a values with
        value: A value to associate with a key
        unit: A unit to associate with the value

    Returns:
        A row holding the specified key, value and unit.

    """

    return [key, f"{value} {unit}"]


def build_3_cols_kvu(key: str, value: str, unit: str) -> Row:
    """Build a table row with 3 columns and the format |<key>|<value>|<unit>|.

    Args:
        key: A keyword to associate a values with
        value: A value to associate with a key
        unit: A unit to associate with the value

    Returns:
        A row holding the specified key, value and unit.

    """

    return [key, value, unit]


def build_3_cols_kuv(key: str, value: str, unit: str) -> Row:
    """Build a table row with 3 columns and the format |<key>|<unit>|<value>|.

    Args:
        key: A keyword to associate a values with
        value: A value to associate with a key
        unit: A unit to associate with the value

    Returns:
        A row holding the specified key, value and unit.

    """

    return [key, unit, value]


ROW_BUILDERS: List[Callable[[str, str, str], Row]] = [
    build_1_col_kuv,
    build_1_col_kvu,
    build_2_cols_square_brackets,
    build_2_cols_round_brackets,
    build_2_cols_comma,
    build_2_cols_space,
    build_3_cols_kvu,
    build_3_cols_kuv,
]
"""Holds all defined row builders."""


def build_random_row(col_no: int, key: str, value: str, unit: str) -> Row:
    """Use a random row builder to build a row with the provided number of columns and content.

    Args:
        col_no: The number of columns to generate a row with.
        key: A keyword to associate a values with
        value: A value to associate with a key
        unit: A unit to associate with the value

    Returns:
        A row

    """
    row_method: int = _get_random_row_method_by_col_no(col_no)

    return ROW_BUILDERS[row_method](key, value, unit)


def _get_random_row_method_by_col_no(col_no: int) -> int:
    """Chooses a random row building method based on the the number of columns provided.

    Args:
        col_no: The number of columns to generate a row with.

    Returns:
        An index into ROW_BUILDERS for a function returning a row with the provided number of columns.
    """
    method_numbers_by_col_no: List[int] = [
        random.randint(0, 1),
        random.randint(2, 5),
        random.randint(6, 7),
    ]

    return method_numbers_by_col_no[col_no - 1]
