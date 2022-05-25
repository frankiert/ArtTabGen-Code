"""Holds the TableGenerator class, which offers functionality related to generating tables."""
import json
import random
from itertools import chain
from pathlib import Path
from typing import Callable, Dict, List, Set, Tuple, Union

import nltk

import arttabgen.types_.config_main_keys
from arttabgen import config_handler, helper, row_builder, text_manipulator
from arttabgen.helper import InfiniteIterator, Keyword, Row, Table

try:
    nltk.data.find("words")
except LookupError:
    nltk.download("words", quiet=True)

PREFIXED_SYMBOLS = "prefixed_symbols"
BASE_SYMBOLS = "base_symbols"


def _overlap_in_units(original_units, new_units):
    return any([unit in original_units for unit in new_units])


class TableGenerator:  # noqa: D101
    def __init__(
            self,
            keyword_chance: float,
            seed: int,
            min_table_length: int,
            max_table_length: int,
            table_value_limit: int,
            do_complex_value: bool,
            complex_value_chance: float,
            generation_modes_odds: Dict[int, float],
            number_of_columns_odds: Dict[int, float],
            row_manipulation_odds: float,
    ) -> None:
        """Offers functionality to generate tables.

        Args:
            keyword_chance: the chance a specific keyword is used in the tables.
            seed: The seed used for generation of tables.
            min_table_length: The minimum number of rows to generate tables with.
            max_table_length: The maximum number of rows to generate tables with.
            table_value_limit: The maximum value to generate in key, value, unit pairs.
            generation_modes_odds: The generation modes to use for generating tables.
            number_of_columns_odds: A mapping of number of table columns to
                                    probabilities of generating tables with that number of columns.
            row_manipulation_odds: The probability of manipulating a table row.

        """
        self.keywords: List[Keyword] = []
        self.units: Dict[str, Dict[str, List[str]]] = {}
        self.gt_word_list: Set[str] = set()

        self.generation_modes_odds: Dict[int, float] = generation_modes_odds
        self.number_of_columns_odds: Dict[int, float] = number_of_columns_odds

        self.keyword_chance: float = keyword_chance
        self.table_value_limit: int = table_value_limit
        self.do_complex_value: bool = do_complex_value
        self.complex_value_chance: float = complex_value_chance
        self.seed: int = seed

        self.table_min_length: int = min_table_length
        self.table_max_length: int = max_table_length

        self.row_builders: List[
            Callable[[str, str, str], Row]
        ] = row_builder.ROW_BUILDERS

        self.text_manipulators: List[
            Callable[[str], str]
        ] = text_manipulator.TEXT_MANIPULATORS

        self.row_manipulation_odds: float = row_manipulation_odds

    def generate_tables_with_gt(
            self,
    ) -> InfiniteIterator[Tuple[Table, Table, int]]:
        """Generate random tables and corresponding ground truths and html representation with a set gen_mode.

        The mode can be:

        - 1: easy: false examples are random words
        - 2: medium: false examples are keywords with incorrect unit
        - 3: hard: false examples are mixed up keywords, can have correct unit, true examples have missing words
        - 4: tough: false and true examples have permutations, spelling mistakes possible, line breaks etc.

        The tables contain keywords with random values (ranging from 1 to table_value_limit) and corresponding
        measurement units. The keywords and units have to be provided as described in main.py. Can be used for any list
        of words with units.

        The ground truths contain the row, if it is a true example, or an empty row (len(gt_table) = len(table)).

        Yields:
            The next generated table and its ground truth.

        """

        while True:  # noqa: WPS457
            yield self._generate_table_and_gt()

    def load_keywords(self, keywords_file_path: Union[str, Path]) -> None:
        """Load the keywords from a txt file.

        Args:
            keywords_file_path: The path to the file defining the available keywords.

        Note:
            1 row in the txt equals one keyword with all its synonyms separated by a comma.

        """
        with open(keywords_file_path, "r", encoding="utf-8") as f:
            lines: List[str] = f.read().splitlines()

        self.keywords = [synonym.split(",") for synonym in lines]

    def load_units(self, units_file_path: Union[str, Path]) -> None:
        """Load the units for the keywords from a json file.

        Args:
            units_file_path: The path to the file defining the available units.

        Note:
            It needs to have the following format::

                {
                Keyword_1: {
                    "base_units": ["<base unit>"],
                    "prefixed_units": ["<prefixed units separated by a comma>"],
                    "base_symbols": ["<base symbol>"],
                    "prefixed_symbols": ["<prefixed symbols separated by a comma>"]
                },
                Keyword_2: {...},
                ...
                }

            units are the unit name (centimeter) symbol the abbreviation (cm).

        """
        with open(units_file_path, "r", encoding="utf-8") as f:
            self.units = json.load(f)

    def build_gt_word_list(self) -> None:
        """Build a list of known, *ground truth*, words to avoid text manipulations resulting in 'correct' words."""
        self.gt_word_list.update(chain(*self.keywords))

        # Add top level keys
        self.gt_word_list.update(self.units.keys())
        # Add second level keys

        self.gt_word_list.update(*(unit.keys() for unit in self.units.values()))
        # Add second level values

        self.gt_word_list.update(
            list(
                chain.from_iterable(
                    list(chain.from_iterable(unit.values()))
                    for unit in self.units.values()
                )
            )
        )

    def _generate_table_and_gt(self) -> Tuple[Table, Table, int]:
        """Generate one random table and its GT.

        Returns:
            A table and its ground truth.

        """
        table: Table = []

        gt_table: Table = []

        mode: int = random.choices(
            list(self.generation_modes_odds.keys()),
            weights=list(self.generation_modes_odds.values()),
            k=1,
        )[0]

        col_no: int = random.choices(
            list(self.number_of_columns_odds.keys()),
            weights=list(self.number_of_columns_odds.values()),
            k=1,
        )[0]
        for _ in range(random.randint(self.table_min_length, self.table_max_length)):
            row, gt_row = self._generate_row_by_generation_mode(mode, col_no)
            table.append(row)
            gt_table.append(gt_row)

        return table, gt_table, mode

    def _manipulate_row(self, row: Row, odds: float) -> Row:
        """With a given chance, manipulate a row with a random *text manipulator*.

        Note:
            Manipulation is not guaranteed.

        Args:
            row: A row to manipulate.
            odds: The odds of manipulating the provided row.

        Returns:
            Row: The row after potential manipulation.

        """

        for _ in row:
            if random.uniform(0, 1) > odds:
                continue

            # choose cell to be manipulated
            chosen_cell_index: int = random.randrange(0, len(row))
            chosen_cell: str = row[chosen_cell_index]

            # If a cell contains a digit, it is a value (instead of a keyword or unit) and can not be manipulated.

            if not chosen_cell.strip() or any(char.isdigit() for char in chosen_cell):
                continue

            manipulator = random.choice(self.text_manipulators)
            new_cell: str = manipulator(chosen_cell)

            if new_cell not in self.gt_word_list and any(
                    char.isalpha() for char in new_cell
            ):
                row[chosen_cell_index] = new_cell

        return row

    def _generate_row_by_generation_mode(
            self, mode: int, col_no: int
    ) -> Tuple[Row, Row]:
        """Generate a row using a random row generator for the provided number of columns.

        Will generate a row of a table in accordance with the set generation mode and the defined column number.
        Based on the chosen mode different random manipulations are performed on the row.
        Correct rows are saved as the ground truth.

        Args:
            mode: The generation mode to use.
            col_no: The number of columns to generate the row with.

        Returns:
            A generated row and its optional ground truth.

        """
        keyword, is_true_keyword = self._choose_random_keyword()
        value: str = self._generate_random_value(mode)  # noqa: WPS110
        symbol, is_true_unit = self._choose_random_unit(keyword, mode)

        if is_true_keyword:
            synonym: str = random.choice(keyword)
            gt_row = [keyword[0], synonym, value, symbol] if is_true_unit else []

        else:
            if mode in {3, 4}:
                synonym = self._generate_random_wrong_keyword(symbol)
            else:
                synonym = " ".join(keyword)
            gt_row = []

        row: Row = row_builder.build_random_row(col_no, synonym, value, symbol)

        if mode == 4:
            row = self._manipulate_row(
                row,
                self.row_manipulation_odds,
            )  # add spelling error or new lines etc.

        return row, gt_row

    def _generate_random_value(self, mode) -> str:
        complex_value: str = ""
        if mode == 1 or not self.do_complex_value or random.uniform(0, 1) < self.complex_value_chance:
            complex_value = str(random.randint(0, self.table_value_limit))
        else:
            num_random_value = random.randint(1, 3)
            if num_random_value == 1:
                variations_one_val = ["{:.2f}", "<{:.2f}", "<={:.2f}", ">{:.2f}", ">={:.2f}", "~{:.2f}"]
                random_float = random.uniform(0, self.table_value_limit)
                complex_value = random.choice(variations_one_val).format(random_float)
            elif num_random_value == 2:
                variations_two_vals = ["{:.2f}-{:.2f}", "{:.2f}...{:.2f}", "{:.2f} to {:.2f}"]
                random_float_min = random.uniform(0, self.table_value_limit)
                random_float_max = random.uniform(0, self.table_value_limit)
                complex_value = random.choice(variations_two_vals).format(random_float_min, random_float_max)
            else:
                random_float_1 = random.randint(0, self.table_value_limit)
                random_float_2 = random.randint(0, self.table_value_limit)
                random_float_3 = random.randint(0, self.table_value_limit)
                complex_value = "{}x{}x{}".format(random_float_1, random_float_2, random_float_3)
        return complex_value

    def _choose_random_keyword(self) -> Tuple[Keyword, bool]:
        """Return a random keyword or two random English words (negatives).

        Returns:
            A random keyword and its synonyms, or two random words,
            and whether ground truth data(the keyword) was chosen.

        """
        is_gt: bool = False

        if random.uniform(0, 1) < self.keyword_chance:
            is_gt = True
            keyword: Keyword = random.choice(self.keywords)
        else:
            keyword = random.sample(helper.WORDS, 2)

        return keyword, is_gt

    def _generate_random_wrong_keyword(self, symbol: str) -> str:
        """Generate a random wrong keyword.

        The generation is done by mixing a random keyword with parts of a different random keyword.

        Args:
            symbol: A unit symbol, e.g. cm.

        Returns:
            The generated keyword.

        """
        keyword: Keyword = random.choice(self.keywords)
        random_synonym: str = random.choice(keyword)
        new_synonym: str = random_synonym
        new_units: List[str] = self.units[keyword[0]][PREFIXED_SYMBOLS] + self.units[keyword[0]][BASE_SYMBOLS]

        while self.__keyword_exists(new_synonym) or symbol in new_units:
            keyword = random.choice(self.keywords)

            mix_arr: List[str] = random.choice(keyword).split(" ")

            new_syn_arr: List[str] = random_synonym.split(" ")
            new_syn_arr[-1] = mix_arr[-1]
            new_synonym = " ".join(new_syn_arr)

            new_units = self.units[keyword[0]][PREFIXED_SYMBOLS] + self.units[keyword[0]][BASE_SYMBOLS]

        return new_synonym

    def _choose_random_unit(self, keyword: Keyword, mode: int) -> Tuple[str, bool]:
        """Return a random unit symbol from all units.

        Args:
            keyword: The keyword to choose the unit for.
            mode: The table generation mode used.

        Note:
            The chosen unit is distinct from the original unit (that would be considered
            the ground truth). If a random or wrong keyword was passed, a random original unit is chosen.

        Returns:
            A random unit and whether it is ground truth data.

        """
        is_gt: bool = True

        if keyword[0] in self.units:
            random_keyword: str = keyword[0]
        else:
            random_keyword = random.choice(self.keywords)[0]

        random_units: List[str] = self.units[random_keyword][PREFIXED_SYMBOLS] + self.units[random_keyword][
            BASE_SYMBOLS]
        correct_units: Set[str] = set(
            self.units[random_keyword][PREFIXED_SYMBOLS] + self.units[random_keyword][BASE_SYMBOLS])

        # "": has no symbol (e.g. number of xy: 100 vs length of xy = 100cm)
        random_unit_symbol: str = random.choice(random_units) if random_units else ""

        if (
                random.uniform(0, 1)
                > config_handler.config_handler.config[
            arttabgen.types_.config_main_keys.ConfigMainKeys.GT_ODDS_PER_MODE
        ][mode]
        ):
            is_gt = False

            while _overlap_in_units(correct_units, random_units):
                # while random_unit_symbol in correct_units:
                random_keyword = random.choice(self.keywords)[0]

                random_units = self.units[random_keyword][PREFIXED_SYMBOLS] + self.units[random_keyword][BASE_SYMBOLS]

                # "": has no symbol (e.g. number of xy: 100 vs length of xy = 100cm)
                random_unit_symbol = random.choice(random_units) if random_units else ""

        return random_unit_symbol, is_gt

    def __keyword_exists(self, key: str) -> bool:
        keys = [x.lower() for x in list(set(chain.from_iterable(self.keywords)))]
        return key.lower() in keys
