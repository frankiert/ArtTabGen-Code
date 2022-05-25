"""Holds the TableExporter class, which offers functionality related to exporting generated tables."""
import random
import threading
from concurrent.futures import Future, ThreadPoolExecutor
from pathlib import Path
from typing import Callable, Dict, List, Optional, Union

import pandas as pd
import pdfkit
from PIL import Image
from pdfkit.configuration import Configuration
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.webdriver import WebDriver

from arttabgen import html_handling
from arttabgen.helper import Table
from arttabgen.progress_printer import ProgressPrinter
from arttabgen.transformers import image_manipulator
from arttabgen.types_.transformer_value_combination import TransformerValueCombination


class TableExporter:  # noqa: D101
    def __init__(
            self,
            output_formats: List[str],
            output_dir: Union[str, Path],
            dataset_name: str,
            progress_printer: ProgressPrinter,
            jpg_quality: int,
            wkhtmltopdf_path: Path,
            gecko_driver_path: Path,
            use_concurrent_export: bool,
            image_manipulation_probability: float,
            image_manipulators: List[Callable[[str], None]],
    ) -> None:
        """Offers functionality to exporting tables.

        Args:
            output_formats: The output formats to export tables with.
            output_dir: The directory to export the dataset to.
            dataset_name: The name to give the exported dataset.
            progress_printer: A ProgressPrinter instance to use for printing export progress.
            jpg_quality: The quality (0-100) to use for jpg export.
            wkhtmltopdf_path: The wkhtmltopdf executable to use for the PDF export.
            gecko_driver_path: The firefoxdriver executable to use for the image export.
            use_concurrent_export: A flag enabling/disabling concurrent_exports.
            image_manipulation_probability: The probability of an exported image getting manipulated.
            image_manipulators: A list of image manipulators available for application.

        """
        self.use_concurrent_export = use_concurrent_export
        self.output_formats = output_formats

        self.num_exported_tables: int = 0
        self.jpg_quality: int = jpg_quality
        self.image_manipulation_probability: float = image_manipulation_probability

        self.image_manipulators = image_manipulators
        self.image_manipulators_by_mode: Dict[
            int, List[str]
        ] = image_manipulator.IMAGE_MANIPULATORS_BY_MODE

        # Make sure unused effect transformers are removed before we could falsely access them
        for key, values in self.image_manipulators_by_mode.items():
            self.image_manipulators_by_mode[key] = [
                value for value in values if value in image_manipulators.keys()
            ]

        self.dataset_path: Path = Path(
            output_dir,
            dataset_name,
        )

        self.subdirs_per_output_format: Dict[str, Path] = {
            "csv": Path(self.dataset_path, "tables_csv"),
            "pdf": Path(self.dataset_path, "tables_pdfs"),
            "html": Path(self.dataset_path, "tables_html"),
            "png": Path(self.dataset_path, "tables_png"),
            "jpg": Path(self.dataset_path, "tables_jpg"),
            "gt_csv": Path(self.dataset_path, "gt_csv"),
        }

        if self.use_concurrent_export:
            self.exporters_per_output_format: Dict[
                str,
                Callable[[str, int, int], Future[None]],
            ] = self._export_concurrent()
        else:
            self.exporters_per_output_format: Dict[
                str,
                Callable[[str, int, int], Future[None]],
            ] = self._export_sequential()

        self.wkhtmltopdf_path: Path = wkhtmltopdf_path
        self.gecko_driver_path: Path = gecko_driver_path

        firefox_options: Options = Options()
        # no firefox instance is opened
        firefox_options.add_argument("--headless")
        self.driver: WebDriver = self._init_webdriver(firefox_options)

        self._create_needed_directories()
        self.futures = []
        self.thread_pool = ThreadPoolExecutor()
        self.webdriver_lock = threading.Lock()
        self.progress_printer: ProgressPrinter = progress_printer

    def export_table(
            self,
            ground_truth_table_data: Table,
            generated_table_data: Table,
            transformer_value_combination: TransformerValueCombination,
            mode: int,
    ) -> None:
        """Export a table.

        Args:
            ground_truth_table_data: The generated table's ground truth.
            generated_table_data: The generated table's data.
            generated_table_html: The generated table's html representation.
            transformer_value_combination: A combination of *transformers* to apply to the generated table data.
            mode: The table generation mode used to generate the table.
                  This is needed to apply the correct image manipulators.

        """
        self.num_exported_tables += 1

        generated_table_html = html_handling.table_to_html(
            generated_table_data, transformer_value_combination
        )
        # This copy seems to be necessary to avoid race conditions when exporter
        # functions read this var after it was changed by other threads,
        # leading to files being skipped
        table_num = self.num_exported_tables
        do_transpose = False
        structure_transformers = transformer_value_combination.structure_parameters
        if "table-orientation" in structure_transformers:
            table_orientation = structure_transformers["table-orientation"]
            if table_orientation == "vertical":
                do_transpose = True

        if self.use_concurrent_export:
            self.futures.append(
                self.thread_pool.submit(
                    self.progress_printer.run_as_progressor,
                    self._export_csv,
                    generated_table_data,
                    table_num,
                    "tables",
                    do_transpose
                )
            )
            self.futures.append(
                self.thread_pool.submit(
                    self.progress_printer.run_as_progressor,
                    self._export_csv,
                    ground_truth_table_data,
                    table_num,
                    "gt",
                    False
                )
            )
        else:
            self.progress_printer.run_as_progressor(
                self._export_csv,
                generated_table_data,
                table_num,
                "tables",
                do_transpose
            )
            self.progress_printer.run_as_progressor(
                self._export_csv,
                ground_truth_table_data,
                table_num,
                "gt",
                False
            )
        self._export_table_by_output_formats(generated_table_html, table_num, mode)

    def _export_table_by_output_formats(
            self,
            generated_table_html: str,
            table_num: int,
            mode: int,
    ) -> None:
        """Export a table (internal helper function).

        Args:
            generated_table_html: The generated table's html representation.
            table_num: The number of generated tables this one is.
            mode: The table generation mode used to generate the table.
                  This is needed to apply the correct image manipulators.

        """

        for output_format in self.output_formats:
            if output_format:
                if self.use_concurrent_export:
                    self.futures.append(
                        self.exporters_per_output_format[output_format](
                            generated_table_html,
                            table_num,
                            mode,
                        )
                    )
                else:
                    self.exporters_per_output_format[output_format](
                        generated_table_html,
                        table_num,
                        mode,
                    )

    def _export_csv(self, table_data: Table, table_num: int, data_type: str, do_transpose: bool) -> None:
        """Export a table to CSV.

        Args:
            table_data: The data of the table to export.
            table_num: The number of generated tables this one is.
            data_type: The type (ground truth or not) the provided table is of.

        """
        export_dir = self.subdirs_per_output_format[
            "csv" if data_type == "tables" else "gt_csv"
        ]

        df = pd.DataFrame(table_data)

        if do_transpose:
            df = df.transpose()

        df.to_csv(
            Path(export_dir, f"tables_{table_num}.csv"),
            sep=";",
            index=False,
            header=False
        )

    def _export_pdf(self, generated_table_html: str, table_num: int) -> None:
        """Export a table to PDF.

        Args:
            generated_table_html: The generated table's html representation.
            table_num: The number of generated tables this one is.
            mode: The table generation mode used to generate the table.
                  This is needed to apply the correct image manipulators.

        """
        table_name: str = f"tables_{table_num}"
        pdf_file: Path = Path(
            self.subdirs_per_output_format["pdf"],
            f"{table_name}.pdf",
        )

        config: Configuration = pdfkit.configuration(
            wkhtmltopdf=self.wkhtmltopdf_path,
        )  # use local installed version

        # to set options, they need to appear in a dict, see https://pypi.org/project/pdfkit/
        # and https://wkhtmltopdf.org/usage/wkhtmltopdf.txt
        options: Dict[str, Optional[str]] = {
            "enable-local-file-access": None,
            "quiet": "",
        }

        pdfkit.from_string(
            generated_table_html,
            str(pdf_file.absolute()),
            configuration=config,
            options=options,
        )

    def _export_image(
            self,
            generated_table_html: str,
            table_num: int,
            file_format: str,
            mode: int,
    ) -> None:
        """Export a table as a image.

        Args:
            generated_table_html: The generated tables html representation.
            table_num: The number of generated table this one is.
            file_format: the output format of the image (png or jpeg)
            mode: The table generation mode used to generate the table.
                  This is needed to apply the correct image manipulators.

        """

        table_name: str = f"tables_{table_num}"
        image_file: Path = Path(
            self.subdirs_per_output_format[file_format],
            f"{table_name}.{file_format}",
        )

        with self.webdriver_lock:
            # Hacky workaround because data URIs are bugged
            self.driver.get("data:text/html,")
            root_element = self.driver.find_element_by_tag_name("html")
            generated_table_html = generated_table_html.replace("\n", "\\n")
            generated_table_html = generated_table_html.replace("'", "\\'")
            self.driver.execute_script(
                f"arguments[0].innerHTML = '{generated_table_html}';", root_element
            )

            # https://stackoverflow.com/questions/41721734/take-screenshot-of-full-page-with-selenium-python-with-chromedriver/52572919#52572919
            original_size = self.driver.get_window_size()
            required_width = self.driver.execute_script('return document.body.parentNode.scrollWidth')
            required_height = self.driver.execute_script('return document.body.parentNode.scrollHeight')
            self.driver.set_window_size(required_width, required_height + 74)
            self.driver.find_element_by_tag_name('body').screenshot(str(image_file))
            self.driver.set_window_size(original_size['width'], original_size['height'])

        with Image.open(image_file) as image:
            # Strip Alpha channel, because JPG can't contain it
            image = image.convert("RGB")

            if (
                    random.random() < self.image_manipulation_probability
                    and self.image_manipulators_by_mode[mode]
            ):
                manipulator = self.image_manipulators[
                    random.choice(self.image_manipulators_by_mode[mode])
                ]
                image = manipulator(image)

            if file_format == "jpg":
                image.save(image_file, quality=self.jpg_quality)
            else:
                image.save(image_file)

    def _export_jpg(self, generated_table_html: str, table_num: int, mode: int) -> None:
        """Export a table as a jpg image.

        Args:
            generated_table_html: The generated tables html representation.
            table_num: The number of generated table this one is.
            mode: The table generation mode used to generate the table.
                  This is needed to apply the correct image manipulators.

        """

        self._export_image(generated_table_html, table_num, "jpg", mode)

    def _export_png(self, generated_table_html: str, table_num: int, mode: int) -> None:
        """Export a table as a png image.

        Args:
            generated_table_html: The generated tables html representation.
            table_num: The number of generated table this one is.
            mode: The table generation mode used to generate the table.
                  This is needed to apply the correct image manipulators.

        """

        self._export_image(generated_table_html, table_num, "png", mode)

    def _export_html(
            self, generated_table_html: str, table_num: int
    ) -> None:
        """Export a table as html.

        Args:
            generated_table_html: The generated table's html representation.
            table_num: The number of generated table this one is.
            mode: The table generation mode used to generate the table.
                  This is needed to apply the correct image manipulators.

        """
        table_name: str = f"tables_{table_num}"
        html_file: Path = Path(
            self.subdirs_per_output_format["html"],
            f"{table_name}.html",
        )

        html_file.write_text(generated_table_html, encoding="utf-8")

    def _create_needed_directories(self) -> None:
        """Create the dataset's directory structure."""

        for subdir in self.subdirs_per_output_format.values():
            subdir.mkdir(exist_ok=True, parents=True)

    def _init_webdriver(self, firefox_options: Options) -> WebDriver:
        """Create and configure a webdriver to use for the image export."""
        return webdriver.Firefox(
            executable_path=str(self.gecko_driver_path),
            options=firefox_options,
        )

    def _export_concurrent(self):  # -> Dict[str, Callable[[str, int, int], Future[None]]]:
        """Return a mapping of export formats to concurrent exporter functions."""
        return {
            "pdf": lambda html, table_num, mode: self.thread_pool.submit(
                self.progress_printer.run_as_progressor,
                self._export_pdf,
                html,
                table_num
            ),
            "png": lambda html, table_num, mode: self.thread_pool.submit(
                self.progress_printer.run_as_progressor,
                self._export_png,
                html,
                table_num,
                mode,
            ),
            "jpg": lambda html, table_num, mode: self.thread_pool.submit(
                self.progress_printer.run_as_progressor,
                self._export_jpg,
                html,
                table_num,
                mode,
            ),
            "html": lambda html, table_num, mode: self.thread_pool.submit(
                self.progress_printer.run_as_progressor,
                self._export_html,
                html,
                table_num
            ),
        }

    def _export_sequential(self) -> Dict[str, Callable[[str, int, int], None]]:
        """Return a mapping of export formats to sequential export functions."""
        return {
            "pdf": lambda html, table_num, mode: self.progress_printer.run_as_progressor(
                self._export_pdf,
                html,
                table_num,
                mode,
            ),
            "png": lambda html, table_num, mode: self.progress_printer.run_as_progressor(
                self._export_png,
                html,
                table_num,
                mode,
            ),
            "jpg": lambda html, table_num, mode: self.progress_printer.run_as_progressor(
                self._export_jpg,
                html,
                table_num,
                mode,
            ),
            "html": lambda html, table_num, mode: self.progress_printer.run_as_progressor(
                self._export_html,
                html,
                table_num,
                mode,
            ),
        }
