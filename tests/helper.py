from typing import Any, Callable, List, Optional, Sequence, Union

from arttabgen.table_generator import TableGenerator


def get_first_element_in_sequence(sequence: Sequence) -> Any:
    """Replacement for random.choice() always returning the first element.

    Args:
        sequence: A sequence to return a value from.

    Returns:
        The first value of sequence.

    """

    return sequence[0]


def get_first_element_in_range(
    start: Union[float, int],
    _stop: Union[float, int] = None,
    _step: Optional[Union[float, int]] = None,
) -> Union[float, int]:
    """Replacement for random.randrange() always returning the start value.

    Args:
        start: A start value for a vale range.

    Returns:
        the value of start.

    """

    return start


def set_up_table_generator() -> TableGenerator:
    generator = TableGenerator(
        keyword_chance=0.5,
        seed=0,
        min_table_length=3,
        max_table_length=3,
        generation_modes_odds={1: 1.0},
        do_complex_value=False,
        complex_value_chance=0.0,
        row_manipulation_odds=0.25,
        table_value_limit=10,
        number_of_columns_odds={
            1: 1,
        },
    )
    generator.keywords = [["Air Gap Thickness"], ["Coil Resistance"]]
    generator.units = {
        "Air Gap Thickness": {
            "base_units": ["millimetre"],
            "prefixed_units": [
                "decametre",
                "micrometre",
                "decimetre",
                "millimetre",
            ],
            "base_symbols": ["mm"],
            "prefixed_symbols": ["dm", "nm", "mm", "cm", "km", "m", "dam"],
        },
        "Coil Resistance": {
            "base_units": ["o"],
            "prefixed_units": [
                "microo",
                "megao",
                "millio",
                "decao",
                "decio",
                "o",
                "nanoo",
                "gigao",
                "centio",
                "kiloo",
            ],
            "base_symbols": ["o"],
            "prefixed_symbols": ["go", "o", "co", "do", "no", "dao", "mo"],
        },
    }

    return generator


def dummy_choose_key():
    return ["Air Gap Thickness"], True


def dummy_choose_false_key():
    return ["Air Resistance"], False


def dummy_choose_unit():
    return "mm", True


def dummy_remove_word():
    return "burst npa"


DUMMY_MANIPULATOR: List[Callable[[str], str]] = [dummy_remove_word]
