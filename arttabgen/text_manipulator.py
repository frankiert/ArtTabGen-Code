"""Holds functions to manipulate text.

TEXT_MANIPULATORS: A list of all text manipulators.
"""
import random
import string
from functools import partial
from typing import Callable, List, Optional, Tuple

import editdistance
import nltk
from nltk.corpus import wordnet
from nltk.corpus.reader.wordnet import WordNetError

import arttabgen.types_.config_main_keys
from arttabgen import config_handler, helper
from arttabgen.helper import PAIRS_OF_SIMILAR_LOOKING_LETTERS, QWERTY_KEYS, WORDS

try:
    nltk.data.find("wordnet")
except LookupError:
    nltk.download("wordnet", quiet=True)
try:
    nltk.data.find("omw-1.4")
except LookupError:
    nltk.download("omw-1.4", quiet=True)

wordnet_synsets: List = list(wordnet.all_synsets("n"))
ALPHABET: List[str] = list(string.ascii_lowercase)


def remove_random_word(text: str) -> str:
    """Remove a random word from the input text.

    Args:
        text: a text to manipulate.

    Returns:
        The manipulated text.

    """
    words: list[str] = text.split(" ")
    if len(words) > 1:
        rand_index: int = random.randrange(0, max(0, len(words)))
        words.pop(rand_index)
        text = " ".join(words)

    return text


def switch_two_chars_in_random_word(text: str) -> str:
    """Swap two random characters in a random word from the input text.

    Args:
        text: a text to manipulate.

    Returns:
        The manipulated text.

    """
    words: list[str] = text.split(" ")
    rand_index: int = random.randrange(0, max(0, len(words)))
    word: str = words[rand_index]

    if len(word) > 3:
        random_char_index = random.randrange(1, len(word) - 1)
        words[rand_index] = (
                word[:random_char_index]
                + word[random_char_index + 1]
                + word[random_char_index]
                + word[random_char_index + 2:]
        )

    return " ".join(words)


def duplicate_random_char_in_random_word(text: str) -> str:
    """Duplicate a random character in a random word from the input text.

    Args:
        text: a text to manipulate.

    Returns:
        The manipulated text.

    """
    words: list[str] = text.split(" ")
    rand_index: int = random.randrange(0, max(0, len(words)))
    word: str = words[rand_index]

    if len(word) > 1:
        random_char_index: int = random.randrange(1, len(word))
        words[rand_index] = (
                word[:random_char_index]
                + word[:random_char_index][-1]
                + word[random_char_index:]
        )

    return " ".join(words)


def insert_random_char_in_random_word(text: str) -> str:
    """Insert a random character into a random word from the input text.

    Args:
        text: a text to manipulate.

    Returns:
        The manipulated text.

    """
    words: list[str] = text.split(" ")

    if len(words) > 0:
        rand_index: int = random.randrange(0, max(0, len(words)))
        word: str = words[rand_index]

        if len(word) > 1:
            rnd_posix: int = random.randrange(1, max(0, len(word)))
            word = word[:rnd_posix] + random.choice(helper.ALPHABET) + word[rnd_posix:]
            words[rand_index] = word

    return " ".join(words)


def add_spaces_at_random_pos(text: str) -> str:
    """Insert a space into a random position in the input text.

    Args:
        text: a text to manipulate.

    Returns:
        The manipulated text.

    """
    max_number_spaces = 5
    if (
            arttabgen.types_.config_main_keys.ConfigMainKeys.MAX_NUMBER_SPACES
            in config_handler.config_handler.config
    ):
        max_number_spaces = config_handler.config_handler.config[
            arttabgen.types_.config_main_keys.ConfigMainKeys.MAX_NUMBER_SPACES
        ]
    words: list[str] = text.split(" ")
    rand_index: int = random.randrange(0, max(0, len(words)))
    words[rand_index] = words[rand_index] + (" " * random.randint(1, max_number_spaces))

    return " ".join(words)


def replace_random_char_with_adjacency_typo(text: str) -> str:
    """Switch a random letter (not just any char) with one adjacent on a QWERTY keyboard.

    Args:
        text: a text to manipulate.

    Returns:
        The manipulated text.

    """

    # I am not sure though, if this is the best way to handle these edge cases.
    # At least they are consistent with the rest of the module.

    if not any(char.isalpha() for char in text) or not any(
            helper.find_letter_in_qwerty_keys(char) for char in text
    ):
        return text

    rand_char_index: int = random.randrange(0, max(0, len(text)))

    original_char_position_in_qwerty: Optional[
        Tuple[int, int]
    ] = helper.find_letter_in_qwerty_keys(text[rand_char_index])

    while not text[rand_char_index].isalpha() or not original_char_position_in_qwerty:
        rand_char_index = random.randrange(0, max(0, len(text)))
        original_char_position_in_qwerty = helper.find_letter_in_qwerty_keys(
            text[rand_char_index]
        )

    new_char: str = helper.get_random_adjacent_element(
        QWERTY_KEYS,
        original_char_position_in_qwerty[0],
        original_char_position_in_qwerty[1],
    )

    return text[:rand_char_index] + new_char + text[rand_char_index + 1:]


def replace_random_letter_with_similar_looking_one(text: str) -> str:
    """Replace a random letter (not just any char) with a similar looking one (e.g. p -> q).

    Args:
        text: a text to manipulate.

    Returns:
        The manipulated text.

    """

    if not any(char.isalpha() for char in text) or not any(
            helper.find_letter_in_similar_looking_ones(char) for char in text
    ):
        return text

    rand_char_index: int = random.randrange(0, max(0, len(text)))

    original_char_position_in_similar_chars: Optional[
        Tuple[int, int]
    ] = helper.find_letter_in_similar_looking_ones(text[rand_char_index])

    while (
            not text[rand_char_index].isalpha()
            or not original_char_position_in_similar_chars
    ):
        rand_char_index = random.randrange(0, max(0, len(text)))
        original_char_position_in_similar_chars = (
            helper.find_letter_in_similar_looking_ones(text[rand_char_index])
        )

    new_char: str = PAIRS_OF_SIMILAR_LOOKING_LETTERS[
        original_char_position_in_similar_chars[0]
    ][1 - original_char_position_in_similar_chars[1]]

    return text[:rand_char_index] + new_char + text[rand_char_index + 1:]


def replace_random_word_with_similar_one(text: str) -> str:
    """Replace a random word with a similarly spelled one (e.g. mouse -> house, moose).

    Args:
        text: a text to manipulate.

    Returns:
        The manipulated text.

    """

    input_words: List[str] = text.split(" ")

    if not any(word.isalpha() for word in input_words):
        return text

    rand_word_index: int = random.randrange(0, len(input_words))

    while not input_words[rand_word_index].isalpha():
        rand_word_index = random.randrange(0, max(0, len(input_words)))

    rand_word: str = input_words[rand_word_index]

    reference_words_sorted_by_similarity: List[str] = sorted(
        WORDS, key=partial(editdistance.eval, b=rand_word)
    )

    new_word_pool: List[str] = reference_words_sorted_by_similarity[:5]

    # Prevent picking original word

    if rand_word in new_word_pool:
        new_word_pool.remove(rand_word)
        new_word_pool += reference_words_sorted_by_similarity[5]

    new_word: str = random.choice(new_word_pool)

    input_words[rand_word_index] = new_word

    return " ".join(input_words)


def replace_word_with_semantically_similar_one(text: str) -> str:
    """Replace a random word with a semantically similar one (e.g. plane -> boat).

    Args:
        text: a text to manipulate.

    Returns:
        The manipulated text.

    """

    input_words: List[str] = text.split(" ")

    if not any(word.isalpha() for word in input_words):
        return text

    rand_word_index: int = random.randrange(0, len(input_words))

    while not input_words[rand_word_index].isalpha():
        rand_word_index = random.randrange(0, max(0, len(input_words)))

    rand_word: str = input_words[rand_word_index]

    try:
        synset_orig = wordnet.synset(f"{rand_word}.n.01")
    # Chosen word is not part of wordnet
    except WordNetError:
        return text

    random.shuffle(wordnet_synsets)

    for synset_candidate in wordnet_synsets:

        # https://stackoverflow.com/questions/21902411/how-to-get-domain-of-words-using-wordnet-in-py

        if (
                config_handler.config_handler.config[
                    arttabgen.types_.config_main_keys.ConfigMainKeys.SEMANTIC_WORD_REPLACEMENT_MIN_SIMILARITY
                ]
                < synset_orig.path_similarity(synset_candidate)
                < config_handler.config_handler.config[
            arttabgen.types_.config_main_keys.ConfigMainKeys.SEMANTIC_WORD_REPLACEMENT_MAX_SIMILARITY
        ]
        ):
            input_words[rand_word_index] = synset_candidate.lemmas()[0].name()

            return " ".join(input_words)

    return text


TEXT_MANIPULATORS: List[Callable[[str], str]] = [
    remove_random_word,
    switch_two_chars_in_random_word,
    duplicate_random_char_in_random_word,
    insert_random_char_in_random_word,
    add_spaces_at_random_pos,
    replace_random_letter_with_similar_looking_one,
    replace_random_word_with_similar_one,
    replace_word_with_semantically_similar_one,
]
"""Holds all defined *text manipulators*."""
