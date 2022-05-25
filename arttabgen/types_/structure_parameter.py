"""Holds a dataclass for the configuration of a *structure parameter*.

See also:
    :ref:`Transformers`
"""
from dataclasses import dataclass
from typing import Any


@dataclass()
class StructureParameter:
    """Holds the configuration of a *structure parameter*."""

    name: str
    """The name of the parameter, e.g. ``"orientation"``."""
    type: str
    """The type of the parameter, e.g. ``"continuous"``."""
    value: Any
    """The value of the parameter, e.g. ``500``."""
