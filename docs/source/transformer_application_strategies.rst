Transformer application strategies
==================================

Transformer application strategies decide the logic of applying *transformers*.

Selective
---------

When using this method of transformer application, for each table a random value from each style
parameter and structure parameter defined in the config file is randomly selected and applied.
All parameters are used and for every parameter a single value is chosen.

Combinatorical
--------------

When using this method of transformer application, a list of transformer parameter combinations will be built and it's combinations removed after being used.
The list of transformer parameter combinations contains all possible combinations of all values of all transformer parameters.
All parameters are used and for every parameter all values are chosen.

Abstract example:

Style parameters: ``A``, ``B``, ``C``

Structure parameters: ``X``, ``Y``

Transformer parameter combinations: ``AX``, ``AY``, ``BX``, ``BY``, ``CX``, ``CY``

.. note::
    The combinatorical transformer parameter application overrides the number of tables to be generated.
    For every possible combination, a table will be generated.

.. seealso::
    | :ref:`Config`
    | :ref:`Transformers`
    | :py:mod:`arttabgen.types.transformer_application_strategy`
    | :ref:`Command line interface's transformer application strategy option <transformer_application_strategy_cli_target>`
