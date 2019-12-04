==============
1. ncsd_python
==============

NCSD is short for No Core Slater Determinant.

ncsd is the code that, given details about a nucleus, finds its wavefunction
by solving the many-body Schrödinger equation using an expansion in
harmonic oscillator basis states.

It uses Slater determinants to ensure that the end result is antisymmetric
with respect to particle exchange as required by symmetry properties of QCD.

There are two top-level modules here, and each has some sub-modules
full of helper functions.

.. automodule:: ncsd_python.ncsd_multi
   :members:

.. automodule:: ncsd_python.output_plotter
   :members:

multi_modules
=============

Helper modules for ncsd_multi.py

.. toctree::
   :maxdepth: 1

   multi_modules/data_checker
   multi_modules/data_structures
   multi_modules/file_manager
   multi_modules/formats_multi
   multi_modules/ncsd_multi_run
   multi_modules/parameter_calculations

plot_modules
=============

Helper modules for output_plotter.py

.. toctree::
   :maxdepth: 1

   plot_modules/formats_plot
   plot_modules/ncsd_output_reader
   plot_modules/plotter
   plot_modules/scraper
