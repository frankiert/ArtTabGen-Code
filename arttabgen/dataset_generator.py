"""Holds the DatasetGenerator class, which offers a complete dataset generation routine."""
import csv
import itertools
import json
import operator
from functools import reduce
from pathlib import Path
from typing import Callable, Dict, Iterator, List, Optional, Tuple, Union

from arttabgen import config_handler
from arttabgen.helper import Table, dict_merge
from arttabgen.progress_printer import ProgressPrinter
from arttabgen.table_exporter import TableExporter
from arttabgen.table_generator import TableGenerator
from arttabgen.types_.transformer_application_strategy import (
    TransformerApplicationStrategy,
)
from arttabgen.types_.transformer_value_combination import TransformerValueCombination


class DatasetGenerator:
    def __init__(
            self,
            table_generator: TableGenerator,
            table_exporter: TableExporter,
            export_used_keywords_and_units: bool,
            number_of_tables: int,
            transformer_application_strategy: TransformerApplicationStrategy,
    ) -> None:
        """Offers a complete dataset generation routine.

        Args:
            table_generator: A TableGenerator instance used to generate tables for the dataset.
            table_exporter: A TableExporter instance used to export generated tables.
            export_used_keywords_and_units: A flag enabling/disabling the export of
                                            keywords and units used to generate a dataset.
            number_of_tables: The number of tables to generate per dataset.
                                This can be overriden if transformer_application_strategy is COMBINATORICAL.
            transformer_application_strategy: An enum controlling how transformers are applied during table generators.

        """
        self.table_generator: TableGenerator = table_generator
        self.table_exporter: TableExporter = table_exporter
        self.export_used_keywords_and_units = export_used_keywords_and_units
        self.number_of_tables: int = number_of_tables
        self.number_of_generated_tables: int = 0
        self.transformer_application_strategy = transformer_application_strategy
        self.config = config_handler.config_handler.config
        self.transformers, number_of_tables = self.build_transformer_combinations()

        number_of_tables = (
                number_of_tables or config_handler.config_handler.config["number_of_tables"]
        )
        # Per table, export the specified formats and generated and gt csv.
        # The remaining value (1) of the constant term (3) is an implementation detail of the export functionality.
        progress_total = number_of_tables * (
                len(self.table_exporter.output_formats) + 2
        )

        progress_printer = ProgressPrinter(
            progress_total,
            number_of_tables,
            20,  # noqa: WPS432
        )

        progress_printer.print_progress()

        self.table_exporter.progress_printer = progress_printer

    def build_transformer_combinations(
            self,
    ) -> Tuple[Iterator[TransformerValueCombination], Optional[int]]:
        """Build a generator yielding transformer parameter combinations.

        This method simply delegates to other methods through :data:`VARIATION_BUILDERS`
        depending on :attr:`transformer_application_strategy`.

        Warning:
            If :attr:`transformer_application_strategy` has the value
            :attr:`arttabgen.types_.transformer_application_strategy.TransformerApplicationStrategy.SELECTIVE`,
            the returned generator will be infinite.

        Returns:
            A generator yielding transformer parameter combinations.

        See also:
            | :ref:`Transformer application strategies`
            | :mod:`arttabgen.types_.transformer_application_strategy`
            | :mod:`arttabgen.types_.transformer_value_combination`
            | :data:`VARIATION_BUILDERS`

        """

        return VARIATION_BUILDERS[self.transformer_application_strategy](self.config)

    def generate_dataset(self) -> None:
        """Generate and export a complete dataset."""

        generate_tables_with_gt: Iterator[
            Tuple[Table, Table, int]
        ] = self.table_generator.generate_tables_with_gt()

        for table, gt, mode in generate_tables_with_gt:
            # No more tables to generate!

            if (
                    self.transformer_application_strategy
                    == TransformerApplicationStrategy.SELECTIVE
                    and self.number_of_generated_tables == self.number_of_tables
            ):
                break

            try:
                transformer_value_combination = next(self.transformers)
                self.number_of_generated_tables += 1
                self.table_exporter.export_table(
                    gt,
                    table,
                    transformer_value_combination,
                    mode,
                )
            # No more tables to generate!
            except StopIteration:
                break

        Path(self.table_exporter.dataset_path, "seed.txt").write_text(
            str(self.table_generator.seed),
            encoding="utf-8",
        )

        if self.export_used_keywords_and_units:
            keywords = Path(self.table_exporter.dataset_path, "keywords_motor.txt")
            with keywords.open("w", encoding="utf-8") as file:
                csv.writer(file).writerows(self.table_generator.keywords)

            Path(self.table_exporter.dataset_path, "units_motor.json").write_text(
                json.dumps(self.table_generator.units),
            )

        self.table_exporter.thread_pool.shutdown(wait=True)

        # Make sure errors in concurrent calls are communicated back to the main thread

        for future in self.table_exporter.futures:
            future.result()


def _build_transformer_combinations_selective(
        config: Dict,
) -> Tuple[Iterator[TransformerValueCombination], Optional[int]]:
    """Build a generator of transformer parameter combinations based on a ``SELECTIVE`` transformer
    application strategy.

    Args:
        config: A deserialized config containing transformer configurations.

    Warning:
        The returned generator is infinite.

    Returns:
        An infinite generator yielding transformer parameter combinations.

    See also:
        | :ref:`Transformers`
        | :ref:`Transformer application strategies`
        | :mod:`arttabgen.types_.transformer_application_strategy`
        | :mod:`arttabgen.types_.transformer_value_combination`
    """

    def _inner() -> Iterator[TransformerValueCombination]:
        while True:
            style_transformers: List[
                Union[str, int, float]
            ] = config_handler.build_style_transformers(
                config,
                TransformerApplicationStrategy.SELECTIVE,
            )
            structure_transformers: Dict[
                str, Union[str, bool]
            ] = config_handler.build_structure_transformers(
                config,
                TransformerApplicationStrategy.SELECTIVE,
            )

            yield TransformerValueCombination(
                style_transformers,
                structure_transformers,
            )

    return _inner(), None


def _build_transformer_combinations_combinatorical(
        config: Dict,
) -> Tuple[Iterator[TransformerValueCombination], Optional[int]]:
    """
    Build a generator of transformer parameter combinations based on a ``COMBINATORICAL``
    transformer application strategy.

    Args:
        config: A deserialized config containing transformer configurations.


    Returns:
        A generator yielding transformer parameter combinations.

    See also:
        | :ref:`Transformers`
        | :ref:`Transformer application strategies`
        | :mod:`arttabgen.types_.transformer_application_strategy`
        | :mod:`arttabgen.types_.transformer_value_combination`
    """
    style_transformers: List[
        List[Union[str, int, float]]
    ] = config_handler.build_style_transformers(
        config, TransformerApplicationStrategy.COMBINATORICAL
    )
    structure_transformers: List[
        Dict[str, Union[str, bool]]
    ] = config_handler.build_structure_transformers(
        config,
        TransformerApplicationStrategy.COMBINATORICAL,
    )

    style_transformers.extend(structure_transformers)
    transformer_combinations = itertools.product(*style_transformers)
    number_of_tables = reduce(operator.mul, map(len, style_transformers), 1)

    return (
        (
            TransformerValueCombination(
                combination[:-2],
                reduce(dict_merge, combination[-2:]),
            )
            for combination in transformer_combinations
        ),
        number_of_tables,
    )


VARIATION_BUILDERS: Dict[
    TransformerApplicationStrategy,
    Callable[[Dict], Tuple[Iterator[TransformerValueCombination], Optional[int]]],
] = {
    TransformerApplicationStrategy.SELECTIVE: _build_transformer_combinations_selective,
    TransformerApplicationStrategy.COMBINATORICAL: _build_transformer_combinations_combinatorical,
}
"""Maps all possible strategies for applying transformers to functions building generators of transformer 
parameter combinations.


See also:
    | :ref:`Transformers`
    | :ref:`Transformer application strategies`
    | :mod:`arttabgen.types_.transformer_application_strategy`
    | :mod:`arttabgen.types_.transformer_value_combination`
"""
