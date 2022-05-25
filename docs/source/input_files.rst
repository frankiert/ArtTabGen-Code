Input files 
===========

Keywords
========

Keyword files declare keywords, which can appear in the generated tables.
Each line holds a single keyword alongside it's synonyms, which are separated by commas.

.. note:: Spaces after commas are not allowed.


In the below example, we have a keywords ``Rotor Speed`` with a single synonyms ``rotor speed`` and another keyword ``Coil Resistance`` with the synonyms ``electrical resistance`` and ``coil resistance``. ::


    Rotor Speed,rotor speed
    Coil Resistance,electrical resistance,coil resistance

Units 
=====

Unit files map measuring units to keywords.

.. note:: Units are mapped to the main synonym of a keyword.

In the below example, we have the keywords ``Rotor Speed`` and ``Coil Resistance`` again.

The ``Rotor Speed`` is measured in the unit ``rpm``, which has the symbol ``rpm``.

The ``Coil Resistance`` is measured in the *base unit* ``ohm``, which has additional *prefixed units*; ``megaohm`` and ``kiloohm``.
It's *base symbol* is ``ohm``, but it has additional *prefixed symbols*; ``mohm``, ``kohm`` and ``ohm``.

.. code-block:: json

    {
        "Rotor Speed": {
            "base_units": [
                "rpm"
            ],
            "prefixed_units": [
                "rpm"
            ],
            "base_symbols": [
                "rpm"
            ],
            "prefixed_symbols": [
                "rpm"
            ]
        },
        "Coil Resistance": {
            "base_units": [
                "ohm"
            ],
            "prefixed_units": [
                "megaohm",
                "kiloohm",
                "ohm"
            ],
            "base_symbols": [
                "ohm"
            ],
            "prefixed_symbols": [
                "mohm",
                "kohm",
                "ohm"
            ]
        }
    }

Config
======
.. _config:

The config file is the interface for the user to change settings related to how tables and datasets are generated.

Structural Types Of Parameters
-------------------------------

The parameters can be devided into three types of parameters:

Simple
    The simple parameter consists of a keyword and a name.

    .. _simple_type:

    Example

    .. code-block:: json

        "seed": 847482374824728801

Continuous
    The continuous parameter consists of a name, type=continuous and a range of values defined by start, stop and a optional step value

    .. _continuous_type:

    Example

    .. code-block:: json

        {
        "name": "padding",
        "type": "continuous",
        "unit": "px",
        "value": {
            "start": 0,
            "stop": 100,
            "step": 5
            }
        }

Discrete
    The discrete parameter consists of a name, type=continuous and a set of values defined by selection of values

    .. _discrete_type:

    Example

    .. code-block:: json

        {
        "name": "text-decoration-line",
        "type": "discrete",
        "unit": "",
        "value": [
            "none",
            "underline",
            "overline"
            ]
        },


General parameters
------------------

* ``seed``
    A seed to use for initiating the internally used random number generator. If this key is not defined, the ``--seed`` option of the command line interface is used. If that does not exist either, a random one will be generated.

    Example:

    .. code-block:: json

        "seed": 847482374824728801

    .. seealso::
        
        :ref:`Command line interface's seed option <seed_cli_target>`


* ``table_value_limit``
    Sets the max. value for the numbers appearing in the generated table's cells.


    Example:

    .. code-block:: json

        "table_value_limit": 500

* ``row_manipulation_odds``
    Holds the probability that a row will be manipulated.


    Example:

    .. code-block:: json

        "row_manipulation_odds": 0.5

* ``min_table_length``
    Sets the minimal table length (min. rows or columns depending on orientation).


    Example:

    .. code-block:: json

        "min_table_length": 10

* ``max_table_length``
    Sets the maximum table length (max. rows or columns depending on orientation).


    Example:

    .. code-block:: json

        "max_table_length": 20

* ``jpg_quality``
    Sets the quality level of exported ``jpg`` images. Range 0-100, lower values worsen quality.


    Example:

    .. code-block:: json

        "jpg_quality": 80

* ``image_width``
    Sets the width of the exported images in pixels.


    Example:

    .. code-block:: json

        "image_width": 1080

* ``image_height``
    Sets the height of the exported images in pixels.


    Example:

    .. code-block:: json

        "image_height": 1920

* ``gen_modes_odds``
    Maps difficulty levels to the probability at which a table of that difficulty will be generated. In the example below each
    difficulty has the same chance to be generated.

    .. note:: There only exist the difficulty levels ``1``, ``2``, ``3`` and ``4``.

    .. seealso::
        
        :ref:`Table modes`


    Example:

    .. code-block:: json

        "gen_modes_odds": {
            "1": 0.25,
            "2": 0.25,
            "3": 0.25,
            "4": 0.25
        }

* ``number_of_tables``
    Sets the number of generated tables per dataset.


    Example:

    .. code-block:: json

        "number_of_tables": 3

    .. note:: This option is only effective, if the used *transformer application strategy* is ``SELECTIVE``

    .. seealso::
        
        | :ref:`Command line interface's transformer_application_strategy option <transformer_application_strategy_cli_target>`
        | :ref:`Transformer application strategies`
        | Module :py:mod:`arttabgen.types.transformer_application_strategy`

* ``keyword_chance``
    Sets the probability at which a key(word) is chosen to be included in a table's row.


    Example:

    .. code-block:: json

        "keyword_chance": 0.4

    .. seealso::
        
        | :ref:`Keywords`

* ``number_of_columns_odds``
    Maps numbers of columns to the probability at which a table is generated with the number of columns.


    Example:

    .. code-block:: json

        "number_of_columns_odds": {
            "1": 0.333,
            "2": 0.333,
            "3": 0.333
        }

    .. note:: Tables can have only ``1``, ``2`` or ``3`` columns.

Style parameters
----------------

.. note:: Most style parameters are legal CSS properties.


The following style-parameter are legal CSS parameters.

* ``background-color``
* ``border-collapse``
* ``border-color``
* ``border-spacing``
* ``border-style``
* ``border-width``
* ``color``
* ``font-family``
* ``font-size``
* ``font-style``
* ``font-weight``
* ``height``
* ``letter-spacing``
* ``margin-bottom``
* ``margin-left``
* ``margin-right``
* ``margin-top``
* ``padding``
* ``text-align``
* ``text-decoration-line``
* ``text-decoration-style``
* ``text-transform``
* ``vertical-align``
* ``width``

.. seealso::

   `<https://www.w3schools.com/cssref/>`_

The following style parameters are not legal CSS properties but are still implemented through CSS directives.

* ``background-color-alternating-row``: Defines two colors to be used for alternating background colors in rows
* ``background-color-alternating-column`` : Defines two colors to be used for alternating background colors in columns
* ``color-alternating-row``: Defines two colors to be used for alternating font colors in rows
* ``color-alternating-column``: Defines two colors to be used for alternating font colors in columns

A style parameter can either be *discrete* `discrete_type`_ or *continuous* `continuous_type`_.
Each style parameter can also be supplied with a unit.

Example:

.. code-block:: json

    {
        "name": "text-decoration-line",
        "type": "discrete",
        "unit": "",
        "value": [
            "none",
            "underline",
            "overline"
        ]
    },
    {
        "name": "padding",
        "type": "continuous",
        "unit": "px",
        "value": {
            "start": 0,
            "stop": 100,
            "step": 5
        }
    }

.. note:: The main key for in the config file for style parameters is `parameters`

.. seealso::

    | Module :py:mod:`arttabgen.style_transformer`

Structure parameters
--------------------

* ``has_header``
    Allows the values ``true`` and ``false``. It sets whether
    the generated table has a header. The default value is ``false``.

* ``table_orientation``
    Allows the values `"horizontal"` and `"vertical"`. It sets whether the table is
    vertical oriented or horizontal. The default value  is ``"horizontal"``.

All currently implemented structure parameters are *discrete* `discrete_type`_.

Example in config file:

.. code-block:: json

    "structure_parameters": [
        {
            "name": "has-header",
            "type": "discrete",
            "value": [
                true,
                false
            ]
        },
        {
            "name": "table-orientation",
            "type": "discrete",
            "value": [
                "vertical",
                "horizontal"
            ]
        }
    ]

.. seealso::

    | Module :py:mod:`arttabgen.structure_transformer`

Image effects
-------------

Optionally, it is possible to configure effect parameters, that manipulate exported images according to the difficulty of the generated table.

* ``blur``
    applies a blur effect
    Allowed values: [1, 3, 5, 7, 9, 11, ... , 299]

* ``contrast``
    adjusts the contrast
    Allowed values: [0 - 300]

* ``brightness``
    adjusts brightness
    Allowed values: [0-100]

* ``noise``
    applies a salt and pepper noise filter
    Allowed values: [0.0-1.0]

Example:

.. code-block:: json

    "image_effects": [
        {
            "name": "blur",
            "type": "continuous",
            "value": {
                "start": 5,
                "stop": 15,
                "step": 5
            }
        },
        {
            "name": "contrast",
            "type": "discrete",
            "value": [
                1.1,
                1.3,
                2.7
            ]
        },
        {
            "name": "brightness",
            "type": "continuous",
            "value": {
                "start": -50,
                "stop": 50,
                "step": 10
            }
        },
        {
            "name": "noise",
            "type": "discrete",
            "value": [
                0.05,
                0.1,
                0.07
            ]
        }
    ],

.. seealso::

    | Module :py:mod:`arttabgen.transformers.image_manipulators.IMAGE_MANIPULATORS`
