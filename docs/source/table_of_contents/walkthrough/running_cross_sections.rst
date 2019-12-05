==============================
Cross-Sections
==============================

Now that you've run NCSMC and you've looked at the output with
:ref:`ncsmc_python`, it's time to calculate the cross-section of the reaction.

This one is pretty simple.

1. Edit run_transitions.py
-------------------------------

If you head to the cross_sections directory and open run_transitions.py,
you'll see some variables at the top that look like this, but with comments::

    exe_path = realpath("transitions_NCSMC.exe")
    ncsmc_out_dir = "/Users/callum/Desktop/npsm/_Nmax6_ncsmc_output"
    resultant_files = [
        join(ncsmc_out_dir, "Li9_observ_Nmax6_Jz1"),
        join(ncsmc_out_dir, "Li9_observ_Nmax7_Nmax6_Jz1")
    ]
    target_file = join(ncsmc_out_dir, "Li8_observ_Nmax6_Jz1")
    norm_sqrt = join(ncsmc_out_dir, "norm_sqrt_r_rp_RGM_nLi8_n3lo-NN3Nlnl-srg2.0_20_Nmax6.dat")
    form_factors = join(ncsmc_out_dir, "NCSMC_form_factors_g_h_nLi8_n3lo-NN3Nlnl-srg2.0_20_Nmax6.dat")
    scattering_wf_NCSMC = join(ncsmc_out_dir, "scattering_wf_NCSMC_nLi8_n3lo-NN3Nlnl-srg2.0_20_Nmax6.agr")
    wavefunction_NCSMC = join(ncsmc_out_dir, "wavefunction_NCSMC_nLi8_n3lo-NN3Nlnl-srg2.0_20_Nmax6.agr")
    target_bound_states = [
        # Format: 2J, parity, 2T, binding energy. First entry = ground state.
        [4, 1, 2, -34.8845],
        [2, 1, 2, -33.7694]
    ]
    resultant_states = ["1 -1 3", "3 -1 3"]
    transitions_we_want = ["E1", "E2", "M1"]
    run_name = "nLi8_n3lo-NN3Nlnl-srg2.0_20_Nmax6"
    naming_str = "NCSMC_E1M1E2_Li9_2J_3"
    proj = "n"

Edit the variables to suit your needs.

2. Run run_transitions.py
-------------------------------

Like so::

    python run_transitions.py

3. That's it
-------------------------------

For each bound state of the resultant nucleus desribed in resultant_states,
the code will do the following things:

- make a transitions_NCSMC.in file
- make a NCSMC_E1_Afi file
- make a wavefunction_NCSMC file
- link the other required NCSMC output files
- link the executable

Then at the end all the executables will be run in parallel
and write output to ``output.txt`` in their respective directories
while you sip champagne and think about how convenient this code is.

