================
ncsmc_python
================

Now that you have the coupling kernels, RGM kernels,
and E/M "kernels" from trdens, as well as eigenvector files from ncsd,
you're ready to run ncsmc.

The main concept here is to think about your problem in terms of scattering.

You have some target nucleus, a projectile,
and a resultant nucleus that is made when the target and projectile meet.

Think of scattering a neutron off of lithium 8.

The neutron has one wavefunction going in, and another wavefunction after
being scattered. By math, the only difference between the pre- and post-
scattered wavefunctions should be a phase shift.

`See here for the math <https://en.wikipedia.org/wiki/Partial_wave_analysis>`_.

But the idea of ncsmc is to take a look at what kind of phase shifts happen
for different interactions of states, and at different energies.

Missing Feature:
    We don't currently have a script to run ncsmc. Please make one if possible!

But once you've run it, transfer the output to a local machine
(if you're not already there) and run ``process_ncsmc_output.py``.
It'll walk you through the process of how to deal with the output.

.. toctree::
   :maxdepth: 1

   fitter
   flipper
   output_simplifier
   pheno
   process_ncsmc_output
   rename_post_ncsmc
   resonance_info
   resonance_plotter
   scheme_plot
   utils
