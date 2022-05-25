Developer guide
===============

This page is dedicated to helping maintainers get an understanding about the internals of this program. It is also inteded to cover common additions maintainers might want to make. 

Module interaction
------------------

Make sure you read the :ref:`API reference` for an overview of available modules and classes.


Adding transformers
-------------------

As there are 3 kinds of transformers at the moment, adding new ones is done in different places.

All transformers are configurable through the config and need validators, which reside in :py:mod:`arttabgen.config_validator`.


* *Style transformers*
    reside in :py:mod:`arttabgen.style_transformer` and need to be added to :py:mod:`arttabgen.style_transformer.STYLE_TRANSFORMERS`. 

    They are configurable under the :ref:`style_parameters`` key in the config.

    Their validators need to be added to :py:mod:`arttabgen.config_validator.PARAMETER_VALIDATORS`.

* *Structure transformers*
    reside in :py:mod:`arttabgen.structure_transformer` and need to be added to :py:mod:`arttabgen.structure_transformer.STRUCTURE_TRANSFORMERS`. 

    They are configurable under the ``structure_parameters`` key in the config.

    Their validators need to be added to :py:mod:`arttabgen.config_validator.STRUCTURE_PARAMETER_VALIDATORS`.

* *Effect transformers*
    reside in :py:mod:`arttabgen.transformers.image_manipulators.IMAGE_MANIPULATORS` and need to be added to :py:mod:`arttabgen.transformers.image_manipulators.IMAGE_MANIPULATORS.EFFECT_PROCESSORS`. 

    They are configurable under the ``image_effects`` key in the config.

    Their validators need to be added to :py:mod:`arttabgen.config_validator.IMAGE_EFFECTS_VALIDATORS`.

.. seealso::
   | :ref:`Config`
   | :ref:`Transformers`
   | Module :py:mod:`arttabgen.style_transformer`
   | Module :py:mod:`arttabgen.structure_transformer`
   | Module :py:mod:`arttabgen.transformers.image_manipulators.IMAGE_MANIPULATORS`
   | Module :py:mod:`arttabgen.config_handler`
   | Module :py:mod:`arttabgen.config_validator`

Adding config keys
------------------

To support new config keys, you simply need to add a validator for it and use it wherever you need it.

.. note:: 
   The config is loaded in :py:mod:`arttabgen.main` and will be available in the :py:mod:`arttabgen.config_handler.ConfigHandler` instance's ``config`` member at :py:mod:`arttabgen.config_handler.config_handler`.

.. seealso::
   | :ref:`Config`
   | Module :py:mod:`arttabgen.config_handler`
   | Module :py:mod:`arttabgen.config_validator`

Adding export formats
---------------------

To support new table export formats, you simply need to add a the function to :py:mod:`arttabgen.table_exporter.TableExporter`, assign it a folder in :py:mod:`arttabgen.table_exporter.TableExporter.subdirs_per_output_format` and assign the exporter function to :py:mod:`arttabgen.table_exporter.TableExporter.exporters_per_output_format`.

.. seealso::
   | :ref:`Command line interface`
   | Module :py:mod:`arttabgen.table_exporter`
   | Module :py:mod:`arttabgen.main`

Adding text manipulators
------------------------

To support new text manipulators, you simply need to add a the function to :py:mod:`arttabgen.text_manipulator.TEXT_MANIPULATORS`.

.. seealso::
   | :ref:`Table modes`
   | Module :py:mod:`arttabgen.text_manipulator`
