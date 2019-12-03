import ncsm_e1
import make_transitions

import os

# Resultant nucleus details, for use when making NCSM_E1 files

# states we care about, 2J, pi, 2T
desired_states = ["1 -1 3", "3 -1 3"]
# transitions we care about
transitions = ["E1", "E2", "M1"]
# this variable is for naming of output files
run_name = "nLi8_n3lo-NN3Nlnl-srg2.0_20_Nmax6"
# names of observ.out files from which to read data
files = [
    "/Users/callum/Desktop/npsm/_Nmax6_ncsmc_output/Li9_observ_Nmax6_Jz1",
    "/Users/callum/Desktop/npsm/_Nmax6_ncsmc_output/Li9_observ_Nmax7_Nmax6_Jz1"
]

run_dir = run_name
os.mkdir(run_dir)


ncsm_e1.make_ncsm_e1(desired_states, transitions, run_name, files, out_dir=run_dir)

