Command line interface
======================

.. command-output:: cd ../../ && python arttabgen/main.py --help
   :shell:

All arguments to the Command line interface (CLI) are optional.
To see it's options like above, execute ``python arttabgen/main.py --help``.

Notice how most options specify their default value or define a set of values to choose from.
The ``--keyword_path`` option makes the program search for the ``data/keywords_cubesat.txt`` file by default.
The ``--table_mode`` option only allows a combination of values containing ``1`` , ``2``, ``3``, ``4``.

.. seealso::

    Module :py:mod:`arttabgen.main`

Options
-------

* ``--keyword_path``
     A file containing keywords to fill generated tables with

.. seealso::

    :ref:`Keywords`

* ``--unit_path``
      A file containing keywords-unit mappings to use for the table generation

.. seealso::

    :ref:`Units`

.. _output_dir_target:

* ``--output_dir``
     The directory in which to save the generated dataset

* ``--table_mode``
     The table modes with which individual tables can be generated

.. seealso::

    :ref:`Table modes`

* ``--format``
     Output formats to export generated tables for

.. note:: The raw data of a table and it's ground truth representation is exported in ``csv`` files, this is not configuable.

.. _seed_cli_target:

* ``--seed``
     A seed to use for initiating the internally used random number generator. If this option is not used, the ``seed`` key of the json config will be used. If that does not exist either, a random one will be generated

.. seealso::

    :ref:`Config`

.. _dataset_name_target:

* ``--dataset_name``
     The name to give the directory representing the generated dataset. If not specified, a unique name based on the current time will be created

* ``--config_path``
     A config file containing settings to use for the dataset generation

.. seealso::

    :ref:`Config`

* ``--wkhtmltopdf_path``
     A ``wkhtmltopdf`` binary to use for the ``PDF`` export. If not specified, it will be searched for on the ``PATH`` or in the ``libs`` directory.

* ``--geckodriver_path``
      A ``geckodriver`` binary to use for image based export. If not specified, it will be searched for on the ``PATH`` or in the ``libs`` directory.

.. _transformer_application_strategy_cli_target:

* ``--transformer_application_strategy``
     A strategy controlling how to apply transformers

.. seealso::

    | :ref:`Transformer application strategies`
    | :ref:`Transformers`

.. _export_used_keywords_and_units_target:

* ``--export_used_keywords_and_units``, ``--no-export_used_keywords_and_units``
      Decides if a copy of used keyword and unit files are to be included in the generated dataset. ``--export_used_keywords_and_units`` is used by default, ``--no-export_used_keywords_and_units`` disables this logic.

* ``--concurrent_export``, ``--no-concurrent_export``
     Decides if the export of generated tables is to be done concurrently or sequentially. ``--concurrent_export`` is used by default, ``--no-concurrent_export`` disables this logic.

.. note:: Concurrent exporting uses all available CPU cores.
