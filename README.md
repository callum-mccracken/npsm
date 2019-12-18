[See the Detailed Docs](https://callum-mccracken.github.io/npsm/build/html)

# Why Does NPSM Exist?

There are many codes to run when doing No Core Shell Model
work, and historically it's been a bit of a pain to figure out
how each one works. This is an attempt to simplify that process.

# Getting Started

First clone the
[github repository](https://github.com/callum-mccracken/npsm.git).

You'll want to use the ``--recurse-submodules``
flag so all submodules are created properly, i.e. do this:

``git clone --recurse-submodules https://github.com/callum-mccracken/npsm``

Then, make sure you have some kind of way to download python packages,
e.g. Anaconda. We won't need much, but we will need numpy and matplotlib
for sure.

The first page of the Walkthrough,
called "[The Basics](https://callum-mccracken.github.io/npsm/build/html)",
walks you through how to get set up in more detail.

Read the rest of the Walkthrough to see how to run each script.

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
