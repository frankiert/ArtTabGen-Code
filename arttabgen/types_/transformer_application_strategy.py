"""
Defines an enum with strategies for the application of transformers during the dataset generation.

See also:
    | :ref:`Transformer application strategies`
    | :ref:`Transformers`
"""

from enum import Enum


class TransformerApplicationStrategy(Enum):
    """
    Defines strategies for the application of transformers during the dataset generation.

    See also:
        | :ref:`Transformer application strategies`
        | :ref:`Transformers`
    """
    COMBINATORICAL = 1
    """
    Apply all possible combinations of all values of all transformers.
    
    Note:
        Using this option overrides the specified number of tables to generate.
    """

    SELECTIVE = 2
    """For each transformer, choose a single value to apply it with."""
