==============================
NCSD
==============================

The ncsd_python module makes it easy to run NCSD multiple times
and to plot output from those NCSD runs.

Important Variables
--------------------

ncsd_path:
    Path to NCSD executable

working_dir:
    Path to directory where you want to put all the ncsd files and run them

int_dir:
    Path to directory where your interaction files are stored

machine:
    One of "cedar", "summit", "local". The machine you're using to run ncsd.

run:
    Do you want to run the batch files this code creates? If so, set run=True

ZN:
    Pairs of Z, N values, e.g. (3, 5) or [(3, 5), (3, 6)].

hbar_omega:
    Harmonic oscillator frequency

N_1max:
    highest number of harmonic oscillator quanta for 1 nucleon

N_12max:
    highest number of harmonic oscillator quanta for 2 nucleons

Nmax:
    This isn't a parameter you'll have to enter here, but you should know what
    ``Nmax`` is. In contrast to ``N_1max`` and ``N_12max``,
    ``Nmax`` is the maximum number of oscillator quanta allowed above the
    lowest Pauli-allowed state for the nucleus of interest.
    E.g., ``Nmax = 0`` is the ground state of a nucleus.

Nmax_min, Nmax_max:
    ``Nmax_min`` and ``Nmax_max`` are lower/upper bounds for ``Nmax``.
    For example, ``Nmax_min = 0`` and ``Nmax_max = 8`` gives eigenvectors for
    ``Nmax = 0, 2, 4, 6, 8``.

Nmax_IT:
    ``Nmax`` value at which importance truncation starts

n_states:
    number of final states of the nucleus that we want to calculate

iterations_required:
    At some point in the calculation, we have to diagonalize the hamiltonian,
    which is a huge matrix, so we have to approximate using the Lanczos
    algorithm. ``iterations_required`` is the number of steps to use during
    this Lanczos step.

irest:
    If the calculation fails, should we restart?
    4 = yes, 0 = no, and there are a couple more options too.

nhw_restart:
    Either -1 or 1, whether to restart the calculation using partially finished
    data from a previous run

kappa:
    Kappa is a value that's used for TODO: what?

kappa_points:
    The number of kappa values to use.
    Note that they are entered here such that 1 means 1x10-4.

kappa_vals:
    The values for kappa in increasing order, written as a string so as not
    to confuse the program by giving it a list and looping over the values.

kappa_restart:
    Whether or not to restart the calculation with a certain value of kappa.
    -1 for false, or else some value between 1 and 4.

saved_pivot:
    "T" or "F", whether or not to use a pivot saved during the Lanczos step
    of a previous run.

time:
    A string of the form "days hours minutes", that tells how much processor
    time to reserve. This string will be formatted properly later by the
    program, depending on which machine you're using.

mem:
    How much memory will you need? Integer, denotes memory in GB.

n_nodes:
    number of nodes (integer)

potential_name:
    The name of the potential you used for your interaction,
    for example, "n3lo-NN3Nlnl-srg2.0".
    This is used as an identifier for output files.

two_body_interaction:
    The name of a 2-body interaction file, e.g.
    "TBMEA2srg-n3lo2.0_14.20_910".
    Note that this file must be stored inside int_dir!

interaction_type:
    Integer that designates which type of interaction.
    2 means 2-body, 3 means 3-body, -3 means 3-body but only 2-body
    when doing the importance truncated steps.

N_123max:
    ighest number of harmonic oscillator quanta for 3 nucleons

three_body_interaction:
    The name of a 3-body interaction file, e.g.
    "v3trans_J3T3.int_3NFlocnonloc-srg2.0_from24_220_11109.20_comp".
    Note that this file must be stored inside int_dir!


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
