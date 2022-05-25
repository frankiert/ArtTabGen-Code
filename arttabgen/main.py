"""The CLI entry point for arttabgen."""

import argparse
import datetime
import os
import random
import sys
import warnings
from typing import Callable, List

warnings.filterwarnings("ignore")

sys.path.append(os.path.curdir)
sys.path.append(os.path.abspath(os.path.join(".", "libs", "firefoxdriver")))
sys.path.append(os.path.abspath(os.path.join(".", "libs", "wkhtmltox", "bin")))

import shutil
from pathlib import Path

from arttabgen import config_handler
from arttabgen.dataset_generator import DatasetGenerator
from arttabgen.helper import validate_file_path
from arttabgen.table_exporter import TableExporter
from arttabgen.table_generator import TableGenerator
from arttabgen.types_.transformer_application_strategy import (
    TransformerApplicationStrategy,
)

parser = argparse.ArgumentParser(
    description="Commandline tool to generate artificial tables (ArtTabGen)",
    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
)

parser.add_argument(
    "--keyword_path",
    default=os.path.join(".", "data", "keywords_motor.txt"),
    help="input path to the keyword list",
)
parser.add_argument(
    "--unit_path",
    default=os.path.join(".", "data", "units_motor.json"),
    help="input path to the keyword list",
)
parser.add_argument(
    "--output_dir",
    default=os.path.join(".", "out"),
    help="output dir in which to save the tables",
)
parser.add_argument(
    "--output_formats",
    nargs="+",
    default=("pdf", "jpg", "html"),
    choices=("jpg", "png", "pdf", "html"),
    help="formats to export tables in.",
)

parser.add_argument(
    "--seed",
    type=int,
    help="seed for random generators (takes precedence over config parameter)",
)
parser.add_argument(
    "--dataset_name",
    help="name to store the dataset under",
    default=f"dataset_{datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')}",  # noqa: WPS237
)
parser.add_argument(
    "--config_path",
    default=os.path.join(".", "data", "default_config.json"),
    help="path to read dataset generation configuration from",
)
parser.add_argument(
    "--wkhtmltopdf_path",
    default=shutil.which("wkhtmltopdf") or os.path.abspath(
        os.path.join(".", "libs", "wkhtmltox", "bin", "wkhtmltopdf.exe")),
    type=validate_file_path,
    help="The path to the wkhtmltopdf.exe to use. Use this if the executable is not on the "
         "PATH or in the libs/ directory",
)

parser.add_argument(
    "--geckodriver_path",
    default=shutil.which("geckodriver") or os.path.abspath(
        os.path.join(".", "libs", "firefoxdriver", "geckodriver.exe")),
    type=validate_file_path,
    help="The path to the firefoxdriver executable (geckodriver.exe) to use. Use this if the executable is "
         "not on the PATH or in the libs/ directory",
)

parser.add_argument(
    "--transformer_application_strategy",
    default=TransformerApplicationStrategy.SELECTIVE.name,
    choices=tuple(strategy.name for strategy in TransformerApplicationStrategy),
    help="The strategy to use for selecting transformer parameters to apply",
)

parser.add_argument(
    "--export_used_keywords_and_units",
    action=argparse.BooleanOptionalAction,
    default=False,
    help="Optional export of used keyword and unit files",
)
parser.add_argument(
    "--use_concurrent_export",
    action=argparse.BooleanOptionalAction,
    default=True,
    help="Run exports concurrently or sequentially",
)


def main() -> None:  # noqa: WPS210
    """The entry point for arttabgen."""  # noqa: D401
    args = parser.parse_args()

    transformer_application_strategy = TransformerApplicationStrategy[
        args.transformer_application_strategy
    ]

    config_handler.config_handler = config_handler.ConfigHandler(
        Path(args.config_path), transformer_application_strategy
    )
    config_handler.config_handler.validate_config()

    try:
        seed = args.seed or config_handler.config_handler.config["seed"]
    except KeyError:
        seed = random.randrange(sys.maxsize)

    random.seed(int(seed))

    image_manipulators: List[
        Callable[[str], None]
    ] = config_handler.config_handler.build_image_manipulators()

    table_exporter = TableExporter(
        args.output_formats,
        args.output_dir,
        args.dataset_name,
        None,
        config_handler.config_handler.config["jpg_quality"],
        Path(args.wkhtmltopdf_path),
        Path(args.geckodriver_path),
        args.use_concurrent_export,
        config_handler.config_handler.config["image_manipulation_probability"],
        image_manipulators,
    )

    table_generator = TableGenerator(
        config_handler.config_handler.config["keyword_chance"],
        seed,
        config_handler.config_handler.config["min_table_length"],
        config_handler.config_handler.config["max_table_length"],
        config_handler.config_handler.config["table_value_limit"],
        config_handler.config_handler.config["do_complex_values"],
        config_handler.config_handler.config["complex_values_chance"],
        config_handler.config_handler.config["generation_modes_odds"],
        config_handler.config_handler.config["number_of_columns_odds"],
        config_handler.config_handler.config["row_manipulation_odds"],
    )
    table_generator.load_keywords(args.keyword_path)
    table_generator.load_units(args.unit_path)
    table_generator.build_gt_word_list()

    dataset_generator = DatasetGenerator(
        table_generator,
        table_exporter,
        args.export_used_keywords_and_units,
        config_handler.config_handler.config["number_of_tables"],
        config_handler.config_handler.transformer_application_strategy,
    )

    dataset_generator.generate_dataset()


if __name__ == "__main__":
    main()
