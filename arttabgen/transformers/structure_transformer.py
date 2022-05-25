"""Holds functions to manipulate the structure of tables, acting as *structure transformers*.

STRUCTURE_TRANSFORMERS: A list of all defined *structure transformers*.
"""
from typing import Callable, Dict, Union


def transformer_table_orientation(parameter_value: str) -> str:
    """Returns a table orientation.

    Args:
        parameter_value: An orientation to use.

    Returns:
        str: string setting an orientation.

    """

    return parameter_value


def transformer_has_header(parameter_value: bool) -> bool:
    """Returns a flag dictating whetever generated tables have a header.

    Args:
        parameter_value: An flag to use.

    Returns:
        bool: bool setting the header.

    """

    return parameter_value


STRUCTURE_TRANSFORMERS: Dict[str, Callable[[Union[str, bool]], Union[str, bool]]] = {
    "table-orientation": transformer_table_orientation,
    "has-header": transformer_has_header,
}
"""Holds all defined *structure transformers*."""
