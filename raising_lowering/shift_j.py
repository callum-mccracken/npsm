"""
This script makes applying the J raising / lowering operator a little easier,
and it puts the J-shifted output in the same spot as the original file.

Note this must be run in an interactive session on Cedar.
"""
import os
from os.path import exists, lexists, dirname, realpath, join
os.chdir(realpath(dirname(__file__)))

# path to the eigenvector file you wish to shift. Can be .gz if desired
eig_path = "/scratch/callum/Li8Li9/ncsd/output/mfdp.egv"

# path to raising / lowering program
exe_path = "eigv_Jplus.exe"

# number of neutrons, number of protons
N = 6
Z = 3

# max_2J (>=0) controls how many times we raise / lower.
# if your initial 2J value is 1 and max_2J = 5,
# you'll get files for 2J = -5, -3, -1, 1, 3, 5
max_2J = 5

# stop editing things here!

# initial values of 2J and 2T
init_2J = 0 if (Z + N) % 2 == 0 else 1  # (usually)
init_2T = Z - N

def raise_lower(eig_path):
    """
    Apply the raising / lowering operator for the parameters defined near
    the top of this file.

    After running the exe file once, we obtain:

    - ``mfdp.egv_2J_2T`` for ``delta_J = -1, +1``
    - For example if we start with ``2J=0``, ``2T=-2``, we'll get
        ``mfdp.egv_2_-2`` and ``mfdp.egv_-2_-2``
    - we also get a file for ``delta_J = 0``, but ignore that one
    - ``eigv_Jplus.out`` file

    Then we just run the program a few more times, using those output files
    as input for subsequent runs.
    """
    # unzip if necessary
    if eig_path[-3:] == ".gz":
        if exists(eig_path):
            os.system("gunzip "+eig_path)
            print("unzipped eigenvector file")
        else:
            print("file is already unzipped")
        eig_path = eig_path[:-3]

    # make link to mfdp.egv
    mfdp_link_name = "mfdp.egv"
    if eig_path != mfdp_link_name:
        # assume it's fine to os.remove if it already exists
        if os.path.islink(mfdp_link_name):
            os.remove(mfdp_link_name)
        os.symlink(eig_path, mfdp_link_name)
        print("linked", eig_path, "to", mfdp_link_name)

    # make command to run executable
    run_command = "srun " + exe_path

    # actually run the executable
    print("running", exe_path, "with J =", init_2J/2)
    os.system(run_command.format(J=init_2J/2))
    print("generated new files with J =", str(init_2J/2-1)+",", init_2J/2+1)

    # os.rename output files
    plus_suffix = "_"+str(init_2J + 2)+"_"+str(init_2T)
    minus_suffix = "_"+str(init_2J - 2)+"_"+str(init_2T)
    os.rename("mfdp.egv"+plus_suffix, eig_path+plus_suffix)
    os.rename("mfdp.egv"+minus_suffix, eig_path+minus_suffix)
    os.rename("eigv_Jplus.out", "eigv_Jplus.out_J="+str(init_2J/2))
    print("renamed relevant output files")

    # do positive values of J, then negative ones
    for sign in [1, -1]:
        # loop over all necessary 2J values of this sign
        for two_J in range(init_2J+sign*2, sign*max_2J, sign*2):
            # get the name of the 2J eigenvector file
            new_eig_file = eig_path + "_" + str(two_J) + "_" + str(init_2T)

            # remake mfdp.egv link
            if lexists(mfdp_link_name):
                os.remove(mfdp_link_name)
            os.symlink(new_eig_file, mfdp_link_name)
            print("linked", new_eig_file, "to", mfdp_link_name)

            # run the file
            print("running", exe_path, "with J =", two_J/2)
            os.system(run_command.format(J=two_J/2))
            print("generated new files with J =",
                  str(two_J/2-1)+", ", two_J/2+1)

            # rename the output file, we'll only care about one of them
            new_suffix = "_" + str(two_J + sign*2) + "_" + str(init_2T)
            os.rename("mfdp.egv" + new_suffix, eig_path + new_suffix)
            os.rename("eigv_Jplus.out", "eigv_Jplus.out_J="+str(two_J/2))
            print("renamed relevant output file")

if __name__ == "__main__":
    raise_lower(eig_path)
