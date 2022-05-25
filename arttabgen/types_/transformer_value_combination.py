"""Holds the dataclass TransformerValueCombination, which bundles a combination of different transformer parameter
values ready for usage."""
from dataclasses import dataclass
from typing import Dict, Iterable, Union


@dataclass
class TransformerValueCombination:
    """Holds a combination of different *transformer* parameter values."""

    style_parameters: Iterable[Union[str, int, float]]
    """A list of *style parameter* values ready for insertion."""
    structure_parameters: Dict[str, Union[str, bool]]
    """A list of *structure parameters* and values ready for insertion."""
