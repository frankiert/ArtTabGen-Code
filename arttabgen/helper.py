"""Holds helper functions, variables, Types, etc., which don't have strong association with other modules.

Types:
    Row
    Table
    InfiniteIterator
    ContinuousParameter
    DiscreteParameter
    StyleParameterConfiguration
    ALPHABET
    WORDS
    QWERTY_KEYS
    PAIRS_OF_SIMILAR_LOOKING_LETTERS
Functions:
    randrange_float()
    values_match_any_type()
    random_value_from_style_parameter()
    random_value_from_image_manipulation_parameter()
    ensure_discrete_style_parameter_value()
    random_value_from_discrete()
    random_value_from_continuous()
    get_random_adjacent_element()
    find_letter_in_qwerty_keys()
    find_letter_in_similar_looking_ones()
    convert_keys_to_int()
    validate_file_path()
    dict_merge()
"""

import random
import string
from pathlib import Path
from typing import (
    Any,
    Dict,
    Iterable,
    Iterator,
    List,
    Optional,
    Sequence,
    Tuple,
    TypedDict,
    Union,
)

import nltk

try:
    nltk.data.find("corpus/words")
except LookupError:
    nltk.download("words", quiet=True)

Keyword = List[str]
"""Represents a keyword (list of synonyms)."""

Row = List[str]
"""Representation of a table row."""

Table = List[Row]
"""Representation of a table."""

InfiniteIterator = Iterator
"""Represents a generator, which will not run out of values"""


class ContinuousParameter(TypedDict, total=False):  # noqa: H601
    """Representation of a continuous style parameter value, meant to have the keys start, stop[, step]."""

    start: Union[int, float]
    stop: Union[int, float]
    step: Optional[Union[int, float]]


DiscreteParameter = List[Union[str, int, float]]
"""Representation of a discrete style parameter value list."""


class StyleParameterConfiguration(TypedDict):  # noqa: H601
    """Representation of a style parameter configuration."""

    name: str
    type: str  # noqa: VNE003, A003
    unit: str
    value: Union[ContinuousParameter, DiscreteParameter]  # noqa: WPS110


ALPHABET: List[str] = list(string.ascii_lowercase)

""":meta hide-value:"""

WORDS = sorted(
    {w.lower() for w in nltk.corpus.words.words()},
)

"""A list of unique English words

:meta hide-value:
"""

QWERTY_KEYS: List[List[str]] = [
    ["q", "w", "e", "r", "t", "y", "u", "i", "o", "p"],
    ["a", "s", "d", "f", "g", "h", "j", "k", "l"],
    ["z", "x", "c", "v", "b", "n", "m"],
]

"""A grid of keys on a keyboard with the QWERTY layout.

:meta hide-value:
"""

PAIRS_OF_SIMILAR_LOOKING_LETTERS: List[List[str]] = [
    ["e", "c"],
    ["u", "v"],
    ["m", "n"],
    ["p", "q"],
    ["b", "d"],
    ["B", "D"],
    ["Q", "O"],
    ["l", "I"]
]
"""A list of pairs of letters which look similar to each other (e.g. p and q).

:meta hide-value:
"""


# source: https://stackoverflow.com/a/11949245


def randrange_float(start: float, stop: float, step: float) -> float:
    """Generate a random float in the range of [start, stop] with a step size.

    Args:
        start: The start of the range to generate a number in.
        stop: The end of the range to generate a number in.
        step: The step size to use for generation.

    Returns:
        A random float in the range of [start, stop] with a step size.

    """

    return random.randint(0, int((stop - start) / step)) * step + start  # noqa: WPS221


def values_match_any_type(values: Iterable, *types: Any) -> bool:  # noqa: WPS110
    """Check if every value in values matches at least one type in types_.

    Args:
        values: The values to type-check.
        types: The types_ to check for.

    Returns:
        True, if every value in values matches at least one type in types_.

    """

    return all(isinstance(value, types) for value in values)  # noqa: WPS110


def random_value_from_style_parameter(
        parameter_value,
) -> Union[str, int, float]:
    """Choose a random value from a *style parameter*."""

    if isinstance(parameter_value, List):
        return random_value_from_discrete(parameter_value)
    return random_value_from_continuous(parameter_value)


def random_value_from_image_manipulation_parameter(
        parameter_value: Union[DiscreteParameter, ContinuousParameter]
) -> Union[int, float]:
    """Choose a random value from an *image manipulator*."""
    if isinstance(parameter_value, List):
        return random_value_from_discrete(parameter_value)
    return random_value_from_continuous(parameter_value)


def ensure_discrete_style_parameter_value(
        parameter_value: Any,
) -> List[Union[str, int, float]]:
    """If parameter_value is a continuous value, calculate a discrete one from it.

    Args:
        parameter_value: A parameter value to optionally convert.

    Note:
        A continuous value needs the ``"step"`` key.

    A continuous  value like:

    .. code-block:: json

        {
            "start": 10,
            "stop": 100,
            "step": 10
        }

    would get converted to a discrete value like:

    .. code-block:: json

        [10, 20, 30, 40, 50, 60, 70, 80, 90]

    Returns:
        The discrete parameter.

    Raises:
        ValueError: If parameter_value does not have the ``"step"`` key.
    """
    # Parameter is already discrete

    if isinstance(parameter_value.value, List):
        return parameter_value.value
    try:
        return list(
            range(
                parameter_value.value["start"],
                parameter_value.value["stop"],
                parameter_value.value["step"],
            ),
        )
    except KeyError:
        raise ValueError(
            "Can't build value set from continuous parameter without 'step' value",
        )


def random_value_from_discrete(values: Sequence[Any]) -> Any:  # noqa: WPS110
    """Return a random value from a sequence.

    Args:
        values: A sequence of vales to choose from.

    Returns:
        A random value from values.

    """

    return random.choice(values)


def random_value_from_continuous(parameter: ContinuousParameter) -> Union[int, float]:
    """Return a random value from a continuous value range specification.

    Note:
        The ``"step"`` key in parameter is optional.

    Args:
        parameter: The style parameter configuration defining the value range.

    Returns:
        a random value in the defined range.

    """

    try:
        return randrange_float(
            parameter["start"],
            parameter["stop"],
            parameter["step"],
        )

    except KeyError:

        return random.uniform(
            parameter["start"],
            parameter["stop"],
        )


def get_random_adjacent_element(
        elements: List[List[Any]],
        current_row: int,
        current_column: int,
) -> Any:
    """Pick an element directly adjacent to the current one, in a nested list of elements.

    The range of values to pick is considered a 3x3 block, with the current element being the center.
    The original element can not be picked as the new one.
    The picked element is guaranteed to be inside the grid.
    Rows in the list of elements DO NOT need to have equal lengths to each other or the number of columns.

    Args:
        elements: The grid to pick values in.
        current_row: The row component of the current element.
        current_column: The column component of the current element.

    Returns:
        An element directly adjacent to the current one.

    """

    new_row: int = current_row + random.randint(-1, 1)
    new_column: int = current_column + random.randint(-1, 1)

    # Make sure we don't pick the original point or any invalid index.

    while (
            (new_column == current_column and new_row == current_row)
            or not (0 <= new_row < len(elements))
            or not (0 <= new_column < len(elements[new_row]))
    ):
        new_row = current_row + random.randint(-1, 1)
        new_column = current_column + random.randint(-1, 1)

    return elements[new_row][new_column]


def find_letter_in_qwerty_keys(letter: str) -> Optional[Tuple[int, int]]:
    """Find the position of a letter in the QWERTY keymap defined in QWERTY_KEYS.

    Args:
        letter: A letter to find the position of.

    Returns:
        A tuple containing the row and column defining the letters position in the QWERTY keymap, on success.
        None, if the letter is not contained in the QWERTY keymap.
    """
    for i, row in enumerate(QWERTY_KEYS):
        try:
            j: int = row.index(letter)  # noqa: VNE001
        except ValueError:
            continue

        return i, j

    return None


def find_letter_in_similar_looking_ones(letter: str) -> Optional[Tuple[int, int]]:
    """Find the position of a letter in the list of similar looking letters defined in PAIRS_OF_SIMILAR_LOOKING_LETTERS.

    Args:
        letter: A letter to find the position of.

    Returns:
        A tuple containing the row and column defining the letters position in the list of similar looking letters,
        on success.
        None, if the letter is not contained in the list of similar looking letters.
    """

    for i, row in enumerate(PAIRS_OF_SIMILAR_LOOKING_LETTERS):
        try:
            j: int = row.index(letter)  # noqa: VNE001
        except ValueError:
            continue

        return i, j

    return None


def convert_str_to_bool(bool_str: str) -> bool:
    return bool(bool_str.capitalize())


def convert_keys_to_int(section: Dict[str, Any]) -> Dict[int, Any]:
    """Convert key of dictionary to int, because json cannot store int keys.

    Args:
        section: dictionary to be altered.

    Returns:
        The dictionary after conversion.
    """

    return {int(key): value for key, value in section.items()}


def validate_file_path(path: str) -> str:
    """Validate that path points to a file.

    Args:
        path: A path to a file.

    Returns:
        The path if it points to a file.

    Raises:
        ValueError: If path does not point to a file.
    """
    if not Path(path).is_file():
        raise ValueError

    return path


def dict_merge(a: Dict, b: Dict) -> Dict:  # noqa: VNE001
    """Merge the key-value pairs of a and b.

    Args:
        a: A dictionary to merge b into.
        b: A dictionary to merge into a.

    Returns:
        a

    """
    a.update(b)
    return a
