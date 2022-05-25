"""Holds a dataclass for the configuration of a *image manipulator*.

See also:
    :ref:`Transformers`
"""
from dataclasses import dataclass
from typing import Any


@dataclass()
class ImageManipulationParameter:
    """Holds the configuration of a *image manipulator*."""

    name: str
    """The name of the parameter, e.g. ``"blur"``."""
    type: str
    """The type of the parameter, e.g. ``"continuous"``."""
    value: Any
    """The value of the parameter, e.g. ``500``."""
