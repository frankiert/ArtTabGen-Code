"""Holds functionality related to the conversion of table data to an HTML representation.

Functions:
        table_to_html()
"""

import pandas as pd
from pandas import DataFrame

from arttabgen.helper import Table
from arttabgen.types_.transformer_value_combination import TransformerValueCombination

HTML_SKELETON: str = """
<!DOCTYPE html>
<html>
    <head>
        <meta charset="UTF-8">
        <title>ArtTabGen Table</title>
        <style>
            {styles}
        </style>
    </head>
    <body style="background: white">
        <br>
        <br>
        <br>
        {table}
        <br>
        <br>
        <br>
    </body>
</html>
"""


def table_to_html(
        table: Table,
        transformers: TransformerValueCombination,
) -> str:
    """Build an HTML representation of the passed table data.

    Args:
        table: The table data to use
        transformers: The *transformers* to apply.

    Returns:
        The HTML representation of the passed table data.

    """
    style_transformers = transformers.style_parameters
    structure_transformers = transformers.structure_parameters
    df_table: DataFrame = pd.DataFrame(table)

    table_orientation = "horizontal"
    has_header = False

    if "has-header" in structure_transformers:
        has_header = structure_transformers["has-header"]

    if "table-orientation" in structure_transformers:
        table_orientation = structure_transformers["table-orientation"]

    if table_orientation == "vertical":
        df_table = df_table.transpose()

    return HTML_SKELETON.format(
        table=df_table.to_html(header=has_header, index=False),
        styles="\n".join(style_transformers),
    )
