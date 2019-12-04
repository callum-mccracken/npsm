[See the Detailed Docs](https://callum-mccracken.github.io/npsm/build/html)

# What Is npsm?

We have a lot of codes to run when doing No Core Shell Model
work, a lot of which require non-standard input files, etc.

This code attemps to take the pain out of running NCSM code.

# Getting Started

First clone the [github repository](https://github.com/callum-mccracken/npsm.git).

Make sure you have some kind of way to download python packages, e.g. pip.
We won't need much, but we will need numpy and matplotlib for sure.

Then for each step in your calculation, run the files in each submodule.

# Main Things That npsm Should Do
(should != does, this is just the outline of what I'd like it to eventually do)
1. Run ncsd code, using the ncsd_python module
  - And once the code has been run, make some plots of the output
2. Raise/lower J for your ncsd eigenvectors with the raising_lowering module
3. Help you run trdens with some scripts in trdens_python
  - This will give RGM Kernels, Coupling Kernels and B/E matrix elements
4. Run ncsmc with the ncsmc_python module, and process the output
  - This gives observ.out files, resonance plots, and level scheme plots
5. Calculate nuclear cross-sections using the cross_sections module
  - Automatically deal with creating weird input files
  - Plot some output
  - Do phenomenological adjustments
