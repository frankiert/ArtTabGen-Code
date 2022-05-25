Output
======

Directory Structure
-------------------

The dataset's name and where it is saved is configurable through the command line interface.

In the dataset directory, new directories are generated: one for each export format as well as generated and ground truth raw table data. 
Additionally, a textfile with the used seed will be exported in the dataset directory by default.

Example:

.. code-block::

    out/dataset_20211130113708795005
    ├── gt_csv
    │   ├── tables_1.csv
    │   ├── tables_2.csv
    │   └── tables_3.csv
    │   
    ├── seed.txt
    │   
    ├── tables_csv
    │   ├── tables_1.csv
    │   ├── tables_2.csv
    │   └── tables_3.csv
    │   
    ├── tables_html
    │   ├── tables_1.html
    │   ├── tables_2.html
    │   └── tables_3.html
    │   
    ├── tables_jpg
    │   ├── tables_1.jpg
    │   ├── tables_2.jpg
    │   └── tables_3.jpg
    │   
    ├── tables_pdfs
    │   ├── tables_1.pdf
    │   ├── tables_2.pdf
    │   └── tables_3.pdf
    │   
    └── tables_png

Optional Exports
----------------

Using the command interface, it is possible to enable the export of the used keywords and units.

.. seealso::
    | :py:mod:`arttabgen.table_exporter.TableExporter`
    | :ref:`Units`
    | :ref:`Keywords`
    | :ref:`Command line interface`
    | :ref:`Command line interface's dataset name option <dataset_name_target>`
    | :ref:`Command line interface's dataset name option <export_used_keywords_and_units_target>`
    | :ref:`Command line interface's output directory option <output_dir_target>`
