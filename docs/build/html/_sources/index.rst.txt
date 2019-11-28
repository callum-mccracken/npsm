======================
The OptCov Docs
======================

.. mdinclude:: ../../../README.md

All Modules
-----------

.. toctree::
   :maxdepth: 1

   constants
   earth_data
   genetics
   geometry
   optimization
   plot_funcs
   sampling
   tests
   timer

To Edit these Docs
------------------

These docs were created by sphinx, which pulls docstrings from Python modules.

To generate new HTML files:

- ``cd`` into ``docs`` then run a sphinx command like ``make html``

To add a new Python module:

- create the Python file, and make sure it has good ReST docstrings
- create  ``docs/source/your_filename.rst``, just copy & edit one that's there
- edit ``docs/source/index.rst`` so it includes your new file
- then generate new HTML files
