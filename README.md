[See the Detailed Docs](https://callum-mccracken.github.io/npsm/build/html)

Welcome to ``npsm``!

# What Is npsm?

We have a whole bunch of different codes to run when doing No Core Shell Model
calculations, and a bunch of those tasks are easy to do with Python / Bash.

This code attemps to take the pain out of running NCSM code.

# Getting Started

First clone the [github repository](https://github.com/callum-mccracken/npsm.git)

Make sure you have some kind of way to download python packages, e.g. pip.
We won't need much, but we will need numpy, matplotlib, maybe a few others.

Then, run `tests.py`, to make sure everything worked!

# Main Things That npsm Should Do
(should != does, this is just the outline of what I'd like it to eventually do)
- Run ``ncsd`` code, using the ``ncsd_python`` module
  - And once the code has been run, make some plots of the output
- Raise/lower J for your ``ncsd`` eigenvectors with ``raising_lowering``
- Help you run ``trdens`` with some scripts in ``trdens_python``
  - This will give RGM Kernels, Coupling Kernels and B/E matrix elements
- Run ``ncsmc`` with ``ncsmc_python``, and process the output
  - This gives observ.out files, resonance plots, and level scheme plots
- Calculate nuclear cross-sections using ``cross_sections``
  - Automatically deal with creating weird input files
