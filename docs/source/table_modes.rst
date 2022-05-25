Table modes
===========
The *table modes* decide how table data is generated.

Generated Rows can be considered *ground truth* or *false*.
False data was created by means like mixing parts of keywords, applying spelling mistakes, etc.

.. note:: If image manipulators are specified those will also be applied according to table mode


The table modes differ in the kind of manipulations they make as well as the configurable probability of making them.

Currently, there are 4 tables modes representing 4 different difficulty levels for the table data extraction.
Each mode adds new functionality in addition to the one present in lower difficulties.

1. Easy
   Picked Keywords can be random english words
2. Medium
3. Hard
   New wrong keywords are generated
4. Tough
   Table rows can be manipulated

.. seealso::
   | Module :py:mod:`arttabgen.text_manipulator`
   | Module :py:mod:`arttabgen.image_processing`
   | Function :py:mod:`arttabgen.table_generator.TableGenerator._generate_row_by_generation_mode`
   | :ref:`Config`
