==============================
NCSD
==============================

The ncsd_python module makes it easy to run NCSD multiple times
and to plot output from those NCSD runs.

Running NCSD
--------------

1. Open the ``ncsd_python`` directory, and the ``ncsd_multi.py`` file within.

2. Adjust all the parameters near the top as needed::

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

   - Enter the necessary paths
   - ``machine`` should be either ``cedar``, ``summit``, or ``local``
     (or some other machine if you add a way to make batch files for it)
   - ``run`` controls whether or not to run all batch files automatically
     at the end of this script
   - The ``ManParams`` instance is where you put nucleus info, etc.
   - Inside ``ncsd_multi.py``, each parameter is further explained in a comment

   For example, to do an NCSD run for lithium 6, 7, 8, and 9, enter this::

    man_params = ManParams(
        Z=3,  # number of protons
        N=[3,4,5,6],  # number of neutrons
        ...
    )

3. Run the file, like so::

    python ncsd_multi.py

   The script will...

   - create a directory for each run
   - put all the necessary files (e.g. mfdp.dat) inside
   - depending on the value of ``run``, it will submit the jobs
   - once ncsd's done running all output will be plotted

Plotting NCSD Output
---------------------

Now you have ncsd output files, and you want to make a plot
of energies vs Nmax. Something like this:

.. raw:: html

    <a href="https://i.imgur.com/nw1HBUW.png" >
        <img src="https://i.imgur.com/nw1HBUW.png"/>
    </a>

The file containing the relevant output will have a name like this::

    Li8_n3lo-NN3Nlnl-srg2.0_Nmax0-10.20

The script ``output_plotter.py`` will read that file, then plot the energies
of the states it finds. It produces .grdt, .csv, .png, and .svg output files.

The image I showed above is just the auto-generated matplotlib plot,
which could use some work in terms of beauty. If you want to edit the plots
afterwards, e.g. to rearrange titles, either use the xmgrace files or
edit the .svg file with Inkscape or a similar program.

If you want your plot to exclude certain ``Nmax`` values or something,
there are parameters in the ``output_plotter.py`` file that you can edit,
and then re-run. Those parameters are better explained inside the actual file.
