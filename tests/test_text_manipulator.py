from pathlib import Path

from pytest_mock import MockerFixture

from arttabgen import text_manipulator
from arttabgen.config_handler import ConfigHandler


class TestRemoveRandomWord:
    def test_remove_third_word(self, mocker: MockerFixture):
        mocker.patch("random.randrange", return_value=2)

        text = "Lorem ipsum dolor sit amet"
        expected = "Lorem ipsum sit amet"

        returned = text_manipulator.remove_random_word(text)

        assert returned == expected


class TestSwitchTwoChars:
    def test_switch_two_chars_in_third_word(self, mocker: MockerFixture):
        mocker.patch("random.randrange", return_value=2)

        text = "Lorem ipsum dolor sit amet"
        expected = "Lorem ipsum doolr sit amet"

        returned = text_manipulator.switch_two_chars_in_random_word(text)

        assert returned == expected

    def test_no_switch_because_too_short(self, mocker: MockerFixture):
        mocker.patch("random.randrange", return_value=2)

        text = "Lorem ipsum i sit amet"
        expected = "Lorem ipsum i sit amet"

        returned = text_manipulator.switch_two_chars_in_random_word(text)

        assert returned == expected


class TestDuplicateChar:
    def test_duplicate_two_chars_in_second_word(self, mocker: MockerFixture):
        mocker.patch("random.randrange", return_value=2)

        text = "Lorem ipsum dolor sit amet"
        expected = "Lorem ipsum doolor sit amet"

        returned = text_manipulator.duplicate_random_char_in_random_word(text)

        assert returned == expected

    def test_no_change_because_too_short(self, mocker: MockerFixture):
        mocker.patch("random.randrange", return_value=2)

        text = "Lorem ipsum i sit amet"
        expected = "Lorem ipsum i sit amet"

        returned = text_manipulator.duplicate_random_char_in_random_word(text)

        assert returned == expected


class TestInsertChar:
    def test_insert_char_in_third_word(self, mocker: MockerFixture):
        mocker.patch("random.randrange", return_value=2)
        mocker.patch("random.choice", return_value="m")

        text = "Lorem ipsum dolor sit amet"
        expected = "Lorem ipsum domlor sit amet"

        returned = text_manipulator.insert_random_char_in_random_word(text)

        assert returned == expected


class TestAddSpaces:
    def test_add_two_spaces(self, mocker: MockerFixture):
        mocker.patch("random.randrange", return_value=2)
        mocker.patch("random.randint", return_value=3)

        text = "Lorem ipsum dolor sit amet"
        expected = "Lorem ipsum dolor    sit amet"
        mocker.patch("json.loads")
        mocker.patch("pathlib.Path.read_text")
        mocker.patch(
            "arttabgen.config_handler.config_handler",
            ConfigHandler(Path(""), None),
        )
        mocker.patch(
            "arttabgen.config_handler.config_handler.config", {"max_number_spaces": 5}
        )

        returned = text_manipulator.add_spaces_at_random_pos(text)

        assert returned == expected


class TestApplyAdjacencyTypoToRandomLetter:
    def test_first_iteration_no_letter(self, mocker: MockerFixture):
        mocker.patch("random.randrange", side_effect=[3, 2])
        mocker.patch("random.randint", side_effect=[0, 1])

        returned: str = text_manipulator.replace_random_char_with_adjacency_typo(
            "foo bar"
        )

        assert returned == "fop bar"

    def test_letter(self, mocker: MockerFixture):
        mocker.patch("random.randrange", return_value=4)
        mocker.patch("random.randint", side_effect=[-1, 0])

        returned: str = text_manipulator.replace_random_char_with_adjacency_typo(
            "foo bar"
        )

        assert returned == "foo gar"


class TestReplaceRandomLetterWithSimilarLookingOne:
    def test_first_iteration_no_letter(self, mocker: MockerFixture):
        mocker.patch("random.randrange", side_effect=[3, 2])
        mocker.patch("random.randint", side_effect=[0, 1])

        returned: str = text_manipulator.replace_random_letter_with_similar_looking_one(
            "FOO BAR"
        )

        assert returned == "FOQ BAR"

    def test_letter_to_second_in_pair(self, mocker: MockerFixture):
        mocker.patch("random.randrange", return_value=4)
        mocker.patch("random.randint", side_effect=[-1, 0])

        returned: str = text_manipulator.replace_random_letter_with_similar_looking_one(
            "foo bar"
        )

        assert returned == "foo dar"

    def test_letter_to_first_in_pair(self, mocker: MockerFixture):
        mocker.patch("random.randrange", return_value=4)
        mocker.patch("random.randint", side_effect=[-1, 0])

        returned: str = text_manipulator.replace_random_letter_with_similar_looking_one(
            "foo dar"
        )

        assert returned == "foo bar"


class TestReplaceRandomWordWithSimilarOne:
    def test_replace_first_word(self, mocker: MockerFixture):
        mocker.patch("random.randrange", return_value=0)
        mocker.patch("random.choice", return_value="bar")
        mocker.patch(
            "arttabgen.text_manipulator.WORDS", ["car", "ar", "bar", "ca", "cab", "cat"]
        )

        returned: str = text_manipulator.replace_random_word_with_similar_one(
            "car tree mouse"
        )

        assert returned == "bar tree mouse"

    def test_first_iteration_no_word(self, mocker: MockerFixture):
        mocker.patch("random.randrange", side_effect=[1, 0])
        mocker.patch("random.choice", return_value="bar")
        mocker.patch(
            "arttabgen.text_manipulator.WORDS", ["car", "ar", "bar", "ca", "cab", "cat"]
        )

        returned: str = text_manipulator.replace_random_word_with_similar_one(
            "car 1234 mouse"
        )

        assert returned == "bar 1234 mouse"
