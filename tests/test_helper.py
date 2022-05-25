from typing import List

from pytest_mock.plugin import MockerFixture

from arttabgen import helper
from arttabgen.helper import randrange_float


class TestRandrangeFloat:
    def test_simple(self):
        assert randrange_float(1.5, 3.0, 0.5) in {1.5, 2.0, 2.5, 3.0}


class TestGetRandomAdjacentElement:
    def test_simple(self, mocker: MockerFixture):
        patcher = mocker.patch("random.randint", return_value=1)

        elements: List[List[str]] = [
            ["a", "b", "c"],
            ["d", "e", "f"],
            ["g", "h", "i"],
        ]

        returned = helper.get_random_adjacent_element(elements, 1, 1)

        assert patcher.call_count == 2
        assert returned == "i"
