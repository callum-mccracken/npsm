"""
Main module of cross_sections

- you input some variables, like paths to files
- then for each bound state of the resultant nucleus, we make a directory with
  - transitions_NCSMC.in
  - wavefunction_NCSMC file
  - link to executable transitions code
  - norm_sqrt file
  - form_factors file
  - scattering_wf_NCSMC file
"""

import ncsm_e1
import dot_in
import file_tools
import utils
import os
from os.path import join, dirname, lexists, exists, basename, realpath
from multiprocessing import Process

# path to executable file
exe_path = realpath("transitions_NCSMC.exe")

# where are your output files stored?
ncsmc_out_dir = "/Users/callum/Desktop/npsm/_Nmax6_ncsmc_output"

# observ.out files for the resultant nucleus
resultant_files = [
    join(ncsmc_out_dir, "Li9_observ_Nmax6_Jz1"),
    join(ncsmc_out_dir, "Li9_observ_Nmax7_Nmax6_Jz1")
]

# observ.out file for the target nucleus
target_file = join(ncsmc_out_dir, "Li8_observ_Nmax6_Jz1")

#the eigenphase_shift or phase_shift file, for getting energy bounds
shift_file = join(ncsmc_out_dir, "phase_shift_nLi8_n3lo-NN3Nlnl-srg2.0_20_Nmax6.agr")

# you also need these files, which are produced by ncsmc:
norm_sqrt = join(ncsmc_out_dir, "norm_sqrt_r_rp_RGM_nLi8_n3lo-NN3Nlnl-srg2.0_20_Nmax6.dat")
form_factors = join(ncsmc_out_dir, "NCSMC_form_factors_g_h_nLi8_n3lo-NN3Nlnl-srg2.0_20_Nmax6.dat")
scattering_wf_NCSMC = join(ncsmc_out_dir, "scattering_wf_NCSMC_nLi8_n3lo-NN3Nlnl-srg2.0_20_Nmax6.agr")
wavefunction_NCSMC = join(ncsmc_out_dir, "wavefunction_NCSMC_nLi8_n3lo-NN3Nlnl-srg2.0_20_Nmax6.agr")

# bound states of the target nucleus. TODO: can we get these automatically?
target_bound_states = [
    # Format: 2J, parity, 2T, binding energy. First entry = ground state.
    [4, 1, 2, -34.8845],
    [2, 1, 2, -33.7694]
]

# resultant nucleus states we care about, in "2J pi 2T" format
resultant_states = ["1 -1 3", "3 -1 3"]

# transitions we care about
transitions_we_want = ["E1", "E2", "M1"]

# this string is contained in input files
run_name = "nLi8_n3lo-NN3Nlnl-srg2.0_20_Nmax6"

# another string for parts of naming of output files,
# we'll append "_2J" at the end, e.g. "_1", based on resultant_states
naming_str = "NCSMC_E1M1E2_Li9_2J"


# the projectile we're using, curently only "n" and "p" are supported
proj = "n"


def make_dir(res_state):
    """
    Makes a directory for the given state of the resultant nucleus.

    res_state:
        string, of the form "1 -1 3"
    """
    # the 3m version of a state with 2J = 3, parity = -1
    res_state_name = utils.get_state_name(res_state)
    run_dir = run_name+"_"+res_state_name
    if not exists(run_dir):
        os.mkdir(run_dir)

    J2, _, _ = res_state.split()

    # make NCSM_E1 file
    ncsm_e1.make_ncsm_e1(
        [res_state], transitions_we_want, run_name, resultant_files,
        out_dir=run_dir)
    # make transitions_NCSMC.in file
    dot_in.make_dot_in(
        proj, target_bound_states, run_name, res_state_name, naming_str+"_"+J2,
        target_file, transitions_we_want, shift_file, out_dir=run_dir)

    # link the executable
    if not lexists(join(run_dir, basename(exe_path))):
        os.symlink(exe_path, join(run_dir, basename(exe_path)))

    # copy / link the other files, as needed
    if not exists(join(run_dir, basename(norm_sqrt))):
        os.symlink(norm_sqrt, join(run_dir, basename(norm_sqrt)))
    if not exists(join(run_dir, basename(form_factors))):
        os.symlink(form_factors, join(run_dir, basename(form_factors)))
    if not exists(join(run_dir, basename(scattering_wf_NCSMC))):
        os.symlink(
            scattering_wf_NCSMC, join(run_dir, basename(scattering_wf_NCSMC)))

    # and finally split up the wavefunction_NCSMC file
    file_tools.make_wf_file(wavefunction_NCSMC, res_state, run_dir)

    # then return the executable to be run
    return join(run_dir, basename(exe_path))


def run_exe(exe):
    """
    Runs an executable file, writes output to output.txt in the same
    directory as the executable.

    exe:
        the path to an executable file
    """
    os.system(". " + exe + " > " + join(dirname(exe), "output.txt"))


if __name__ == "__main__":
    # make run directories
    executables = []
    for res_state in resultant_states:
        executables.append(make_dir(res_state))

    print("Running executables in parallel")
    for exe in executables:
        print(realpath(exe))
        os.system("chmod 777 "+exe)
        Process(target=run_exe(exe)).start()
