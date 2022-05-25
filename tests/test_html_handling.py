from typing import Any, Dict

from pytest_mock import MockerFixture

from arttabgen import html_handling
from arttabgen.types_.transformer_value_combination import (
    TransformerValueCombination,
)


class TestHtmlHandling:
    def test_no_transformers(self, mocker: MockerFixture):
        def return_kwargs(**kwargs):
            return kwargs

        mocked_str = mocker.Mock(spec=str)
        mocker.patch("arttabgen.html_handling.HTML_SKELETON", mocked_str)
        mocked_str.format = return_kwargs

        table = [
            ["electric resistance to current", "th", "437"],
            ["Residual mmoment", "120  ", ""],
        ]

        returned: Dict[str, Any] = html_handling.table_to_html(
            table, TransformerValueCombination([], [])
        )

        wanted_table = """<table border="1" class="dataframe">
  <tbody>
    <tr>
      <td>electric resistance to current</td>
      <td>th</td>
      <td>437</td>
    </tr>
    <tr>
      <td>Residual mmoment</td>
      <td>120</td>
      <td></td>
    </tr>
  </tbody>
</table>"""

        assert returned["styles"] == ""
        assert returned["table"] == wanted_table

    def test_transpose(self, mocker: MockerFixture):
        def return_kwargs(**kwargs):
            return kwargs

        mocked_str = mocker.Mock(spec=str)
        mocker.patch("arttabgen.html_handling.HTML_SKELETON", mocked_str)
        mocked_str.format = return_kwargs

        table = [
            ["electric resistance to current", "th", "437"],
            ["Residual mmoment", "120  ", ""],
        ]

        returned: Dict[str, Any] = html_handling.table_to_html(
            table,
            TransformerValueCombination([], [False, "horizontal"]),
        )

        wanted_table = """<table border="1" class="dataframe">
  <tbody>
    <tr>
      <td>electric resistance to current</td>
      <td>th</td>
      <td>437</td>
    </tr>
    <tr>
      <td>Residual mmoment</td>
      <td>120</td>
      <td></td>
    </tr>
  </tbody>
</table>"""

        assert returned["table"] == wanted_table

    def test_has_header(self, mocker: MockerFixture):
        def return_kwargs(**kwargs):
            return kwargs

        mocked_str = mocker.Mock(spec=str)
        mocker.patch("arttabgen.html_handling.HTML_SKELETON", mocked_str)
        mocked_str.format = return_kwargs

        table = [
            ["electric resistance to current", "th", "437"],
            ["Residual mmoment", "120  ", ""],
        ]

        returned: Dict[str, Any] = html_handling.table_to_html(
            table,
            TransformerValueCombination([], [True, "vertical"]),
        )

        wanted_table = """<table border="1" class="dataframe">
  <tbody>
    <tr>
      <td>electric resistance to current</td>
      <td>th</td>
      <td>437</td>
    </tr>
    <tr>
      <td>Residual mmoment</td>
      <td>120</td>
      <td></td>
    </tr>
  </tbody>
</table>"""

        assert returned["table"] == wanted_table

    def test_style_transformers(self, mocker: MockerFixture):
        def return_kwargs(**kwargs):
            return kwargs

        mocked_str = mocker.Mock(spec=str)
        mocker.patch("arttabgen.html_handling.HTML_SKELETON", mocked_str)
        mocked_str.format = return_kwargs

        table = [
            ["electric resistance to current", "th", "437"],
            ["Residual mmoment", "120  ", ""],
        ]

        returned: Dict[str, Any] = html_handling.table_to_html(
            table,
            TransformerValueCombination(["foo", "bar"], []),
        )

        wanted_style = "foo\nbar"

        assert returned["styles"] == wanted_style
