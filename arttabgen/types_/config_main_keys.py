"""Holds an enum defining the main keys of the config file.

See also:
    :ref:`Config`
"""
from enum import Enum


class ConfigMainKeys(str, Enum):
    """Defines the main keys of the config file.

    See also:
        :ref:`Config`
    """

    SEED = "seed"
    TABLE_VALUE_LIMIT = "table_value_limit"
    ROW_MANIPULATION_ODDS = "row_manipulation_odds"
    MIN_TABLE_LENGTH = "min_table_length"
    MAX_TABLE_LENGTH = "max_table_length"
    JPG_QUALITY = "jpg_quality"
    IMAGE_WIDTH = "image_width"
    IMAGE_HEIGHT = "image_height"
    NUMBER_OF_TABLES = "number_of_tables"
    KEY_CHANCE = "keyword_chance"
    IMAGE_MANIPULATION_PROBABILITY = "image_manipulation_probability"
    SEMANTIC_WORD_REPLACEMENT_MIN_SIMILARITY = (
        "semantic_word_replacement_min_similarity"
    )
    SEMANTIC_WORD_REPLACEMENT_MAX_SIMILARITY = (
        "semantic_word_replacement_max_similarity"
    )
    MAX_NUMBER_SPACES = "max_number_spaces"
    GEN_MODES_ODDS = "generation_modes_odds"
    GT_ODDS_PER_MODE = "gt_odds_per_mode"
    NUMBER_OF_COLUMNS_ODDS = "number_of_columns_odds"
    STYLE_PARAMETERS = "parameters"
    STRUCTURE_PARAMETERS = "structure_parameters"
    IMAGE_PARAMETERS = "image_manipulators"
