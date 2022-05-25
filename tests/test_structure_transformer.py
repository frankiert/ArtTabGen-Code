from pytest_mock import MockerFixture

from arttabgen.transformers import structure_transformer


class TestTransformerHasHeader:
    def test_discrete(self, mocker: MockerFixture):
        parameter: bool = True

        returned: bool = structure_transformer.transformer_has_header(parameter)

        assert returned


class TestTransformerTableOrientation:
    def test_discrete(self, mocker: MockerFixture):
        parameter: str = "horizontal"

        returned: str = structure_transformer.transformer_table_orientation(parameter)

        assert returned == "horizontal"
