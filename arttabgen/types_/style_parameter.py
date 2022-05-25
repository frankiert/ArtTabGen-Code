"""Holds a dataclass for the configuration of a *style parameter*.

See also:
    :ref:`Transformers`
"""
from dataclasses import dataclass
from typing import Any


@dataclass()
class StyleParameter:
    """Holds the configuration of a *style parameter*."""

    name: str
    """The name of the parameter, e.g. ``"font-size"``."""
    type: str
    """The type of the parameter, e.g. ``"continuous"``."""
    unit: str
    """The unit of the parameter, e.g. ``"px"``."""
    value: Any
    """The value of the parameter, e.g. ``500``."""
