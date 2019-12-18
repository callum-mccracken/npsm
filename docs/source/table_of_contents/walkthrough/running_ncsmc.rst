.. _ncsmc_python:

==============================
NCSMC
==============================

Buckle up for this one, this code is more interactive than the others.

.. admonition:: First, run NCSMC.

    We don't currently have code to automate that. If you could make some,
    that would be appreciated. Currently, we only deal with
    processing / plotting the output from NCSMC.

1. Get Set Up
--------------

Once you have your NCSMC output, copy it to a local machine, where you
have followed the setup instructions for Python. See :ref:`basics`.

Also, ensure the columns in the eigenphase_shift and phase_shift files are
rearranged as needed, this code does not adjust column order.

2. Edit process_ncsmc_output.py
---------------------------------

Head into ``ncsmc_python``, where you'll see a bunch of .py files. You only
need to worry about one of them for now, ``process_ncsmc_output.py``.

Open that one up and take a look!

You should see some parameters to edit::

    high_res_dpi = 900
    Nmax_list = [4, 6]
    file_dir = "../where_ncsmc_output_is_kept"
    phase_shift_list = [os.path.join(file_dir, f) for f in [
        "Nmax4/phase_shift_nLi8_n3lo-NN3Nlnl-srg2.0_20_Nmax4.agr",
        "Nmax6/phase_shift_nLi8_n3lo-NN3Nlnl-srg2.0_20_Nmax6.agr"]]
    eigenphase_shift_list = [os.path.join(file_dir, f) for f in [
        "Nmax4/eigenphase_shift_nLi8_n3lo-NN3Nlnl-srg2.0_20_Nmax4.agr",
        "Nmax6/eigenphase_shift_nLi8_n3lo-NN3Nlnl-srg2.0_20_Nmax6.agr"]]
    ncsmc_dot_out_list = [os.path.join(file_dir, f) for f in [
        "Nmax4/ncsm_rgm_Am2_1_1.out_nLi8_n3lo-NN3Nlnl-srg2.0_20_Nmax4",
        "Nmax6/ncsm_rgm_Am2_1_1.out_nLi8_n3lo-NN3Nlnl-srg2.0_20_Nmax6"]]
    experiment = os.path.join(file_dir, "experiment_Li9.txt")

If you're not familiar with the ``os.path.join`` function, it joins paths,
without making you worry about trailing slashes, i.e.::

    os.path.join("x", "y") --> "x/y"
    os.path.join("x/", "y") --> "x/y"

The parameters above are mostly to do with paths to ncsmc output.

The ``Nmax_list`` up top
says which Nmax values you used, and the order of this list must match the
order of the lists of paths down below.

The ``high_res_dpi`` is the resolution of your plots, 300 is poster quality.

``file_dir`` will be added to the front of every file in the lists of paths.

And finally, ``experiment`` references an ``experiment.txt`` file, which
is not a NCSMC output file. You have to make this!

It's something like this::

    I can put anything up here as long as it does not contain commas
    or the word thresh in all caps!

    Data is from the TUNL images and widths are eyeballed
    (http://www.tunl.duke.edu/nucldata/figures/09figs/09_03_2004.gif)

    States are given in the form
    "Energy Width J parity T" but with commas.
    Don't mess up the parsing by using commas elsewhere!

    Li9
    THRESH 4.0639
    0,0,1.5,-,1.5
    2.691,0,0.5,-,?
    4.296,0.2,2.5,-,?
    5.38,0.4,?,?,?
    6.43,0,?,?,?

Again, the part up top is whatever you want it to be, except ``THRESH``
or commas. The data at the bottom is from some experimental source,
usually `TUNL <http://www.tunl.duke.edu/nucldata/index.shtml>`_.

.. admonition:: Note:

    Energy values here are relative to the ground state of your nucleus.

3. Run the File
----------------

Once you've edited those parameters, run the file::

    python process_ncsmc_output.py

You should get some output that looks something like this::

    (base) callum@itheory10 ncsmc_python % python process_ncsmc_output.py
    working on Nmax = 4
    Analyzed all channels, saved CSV with info to /Users/callum/Desktop/npsm/ncsmc_python/resonances_Nmax_4/resonances_phase_Nmax_4.csv
    Working on resonance plotting
    Done plotting! Saved main plot(s) to:
    /Users/callum/Desktop/npsm/ncsmc_python/resonances_Nmax_4/PNGs_phase/phase_Nmax_4_auto.png
    /Users/callum/Desktop/npsm/ncsmc_python/resonances_Nmax_4/PNGs_phase/phase_Nmax_4_auto.svg
    /Users/callum/Desktop/npsm/ncsmc_python/resonances_Nmax_4/grace_files_phase/phase_plot_Nmax_4_auto.grdt
    Analyzed all channels, saved CSV with info to /Users/callum/Desktop/npsm/ncsmc_python/resonances_Nmax_4/resonances_eigenphase_Nmax_4.csv
    Working on resonance plotting
    Done plotting! Saved main plot(s) to:
    /Users/callum/Desktop/npsm/ncsmc_python/resonances_Nmax_4/PNGs_eigenphase/eigenphase_Nmax_4_auto.png
    /Users/callum/Desktop/npsm/ncsmc_python/resonances_Nmax_4/PNGs_eigenphase/eigenphase_Nmax_4_auto.svg
    /Users/callum/Desktop/npsm/ncsmc_python/resonances_Nmax_4/grace_files_eigenphase/eigenphase_plot_Nmax_4_auto.grdt
    Enter all interesting channels in resonances_Nmax_4/interesting.txt

    First, take a look at the PNGs_phase files, to figure out which
    channels are interesting

    (just look at the graph, if you see a swoop up, it's interesting)

    Then, figure out which columns in the eigenphase file those match with.
    (they should have the same J, pi, T, but may have a different column #)

    Then, open up resonances_eigenphase_Nmax_[#].csv and copy the lines
    associated with those channels.

    When you're done, the file should look
    something like this:

    3,+,3,1,strong
    3,+,3,3,strong
    3,-,3,3,strong
    5,-,3,4,none
    5,+,3,4,strong

    [lines copied from the eigenphase csv file, one blank line at the end]


    Hit enter once you've had enough time to enter the right lines. Don't forget to SAVE the file!

.. admonition:: Don't hit enter yet!

    If you do, I think things will break, but if you accidentally do,
    just delete the ``resonances_Nmax_X`` folder that got created,
    and start over.

4. Select Interesting Channels
-------------------------------

By this point in the code, here's what's been done:

- so far we're only considering the first Nmax value in Nmax_list
- we created plots of phase vs energy for all channels in the phase_shift
    and eigenphase_shift files.
- now the program is waiting for you to tell it which channels are
    interesting enough to make it to the final level scheme plot.

So now you have to look at all the different resonances, and do that.

A new directory has been created called ``resonances_Nmax_X``
where X is the first Nmax value.

Inside that directory, there are a bunch of plots (and other files).
Take a peek at the ``PNGs_phase`` directory.

At the same time, open a window with the file called
``resonances_eigenphase_Nmax_X.csv`` (in the resonances_Nmax directory).

Also open the file called ``interesting.txt`` (same directory).

Figure out which channels are interesting using the images made with
phase_shift data, then use the csv file made from eigenphase_shift data
to select channels.

For example, if you see a 2J=2, parity=1, 2T=3 state that looks interesting
in the phase_shift plots, try to find a corresponding channel in the
eigenphase_shift file. Copy that line into ``interesting.txt``

.. raw:: html

    <a href="https://imgur.com/Vm9m3Wi.jpg" >
        <img src="https://imgur.com/Vm9m3Wi.jpg"/>
    </a>

Once you've got all the interesting channels selected, double-check
that they're actually interesting by looking at the PNGs_eigenphase files.

Then save ``interesting.txt`` and hit enter in your terminal.


5. Fit Resonances
------------------

Soon after you hit enter, you should see something like this:

.. raw:: html

    <p>
    <a href="https://imgur.com/DEbKkEc.jpg" >
        <img src="https://imgur.com/DEbKkEc.jpg"/>
    </a>
    </p>

Welcome to the interactive resonance fitter!

Adjust the two sliders until you get a good fit, then hit ``Done``
and close the window. The sliders are adjustable by clicking/dragging,
by double-clicking, and by using arrow keys for fine adjustment.

Eventually, you should have something like this:

.. raw:: html

    <p>
    <a href="https://imgur.com/9T0Hjn4.jpg" >
        <img src="https://imgur.com/9T0Hjn4.jpg"/>
    </a>
    </p>

You'll get one of these windows for each resonance, and by the way,
the data you're seeing here is from the eigenphase_shift file.

After the last one (don't be alarmed if the window doesn't close this time),
it's on to the next Nmax value!

Repeat steps 5 and 6 for all following Nmax values.

6. Recap
---------------------

When you're done the last Nmax value, wait for a few seconds,
and then the code should be finished!

You should get some final output that looks like this::

    Working on resonance plotting
    Done plotting! Saved main plot(s) to:
    /Users/callum/Desktop/npsm/ncsmc_python/resonances_Nmax_6/PNGs_eigenphase/eigenphase_Nmax_6_custom.png
    /Users/callum/Desktop/npsm/ncsmc_python/resonances_Nmax_6/PNGs_eigenphase/eigenphase_Nmax_6_custom.svg
    /Users/callum/Desktop/npsm/ncsmc_python/resonances_Nmax_6/grace_files_eigenphase/eigenphase_plot_Nmax_6_custom.grdt
    got experimental data
    Saved level scheme plot as level_schemes/level_scheme.png

At this point, what has been done?

- For each Nmax:
  - made plots of phase vs energy for all channels
  - created high-res plots of the interesting resonances
  - made some spaghetti plots of multiple resonances
  - take a look in the resonances_Nmax_X directories to see everything
  - got the energies and widths of all interesting resonances
- then we made a plot of the level scheme of this nucleus
  - includes data from each Nmax we considered
  - resonances that were too large to fit on the graph are red

Now give youself a medal, you did it!

I'd love to make this less manual,
but I don't think we're able to detect / fit resonances automatically yet.

Note that if you run this code again, it won't make you select channels
and fit curves again, unless you delete the ``interesting.txt``
and ``eigenphase_info.csv`` files, respectively.

.. admonition:: Note about level scheme plots

    Level scheme plots are saved as .png image files as well as .svg
    (scalable vector graphics) files.

    In the event that there are misplaced titles or something in the image,
    you can edit .svg files with many programs, for example
    `Inkscape <https://inkscape.org/>`_.
