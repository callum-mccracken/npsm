==============================
NCSD
==============================

The ncsd_python module has 2 main uses. I'll walk you through each.

Run ncsd
--------

1. Open the ``ncsd_python`` directory, and the ``ncsd_multi.py`` file within.

2. You'll see a bunch of parameters to adjust::

    ncsd_path = realpath("ncsd-it.exe")
    working_dir = realpath("")
    int_dir = realpath("../interactions/")
    machine = "cedar"
    run = True
    man_params = ManParams(
        Z=3,  # number of protons
        N=5,  # number of neutrons
        ...
    )

Edit them for your specific case. If you want to have multiple runs, you
can use lists for the ``ManParams`` parameters, e.g.::

    man_params = ManParams(
        Z=3,  # number of protons
        N=[3,4,5,6],  # number of neutrons
        ...
    )

That would run ncsd 4 times, for lithium 6, 7, 8, and 9.

3. Once you have finished with all that, just run the file::

    python ncsd_multi.py

This will create a directory for each run, and put all the necessary files
inside. Then depending on the value of ``run``, it will run the batch file
in the directory. If ``run=False``, you'll have to do that yourself.

The batch script was created such that the output from ncsd gets plotted
automatically, i.e. the next section should already be done, but you may
want to edit those plots so still read the next section.

Plot NCSD Output
----------------

So now you have ncsd output, but it's not in a directly plottable format.

The filename will look something like ``Li8_n3lo-NN3Nlnl-srg2.0_Nmax0-10.20``.

The script ``output_plotter.py`` will plot the energies of various states
for your nucleus of interest.

For example, the file listed above produced the following plot
(using filler data for experimental values, our calculation wasn't THAT good):

.. raw:: html

    <a href="https://i.imgur.com/JcXMeMW.jpg" >
        <img src="https://i.imgur.com/JcXMeMW.jpg"/>
    </a>

This is just the auto-generated matplotlib plot, which could use some work
in terms of beauty, but it illustrates what gets plotted.
The xmgrace version plots channel titles too.

.. admonition:: Future Work

    The matplotlib graph could be better, with channel titles etc.

If you want your plot to exclude certain Nmax values or something,
there are parameters in the ``output_plotter.py`` file that you can edit,
and then re-run, same kind of idea as with ``ncsd_multi.py``.



