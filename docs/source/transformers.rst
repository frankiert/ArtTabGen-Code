Transformers
============

*Transformers* offer transformer on how generated tables/documents look.

.. note:: These transformers only act on the generated documents, not on the raw table data.

Currently there are 3 kinds of transformers: style transformers, structure transformers and image manipulators. 

**Style transformers** can make changes to properties like font sizes, border widths a table cell's background color, etc. and are implemented through CSS directives.


**Structure transformers** can make changes like transposing a table or adding a table header.

**Image manipulators** can make changes like applying a blur, noise or contrast change.



.. note:: Image manipulators only apply to image based export formats.

.. seealso::

   | Module :py:mod:`arttabgen.style_transformer`
   | Module :py:mod:`arttabgen.structure_transformer`
   | Module :py:mod:`arttabgen.transformers.image_manipulators.IMAGE_MANIPULATORS`
