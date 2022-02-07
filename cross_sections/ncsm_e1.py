"""
A script to take files from the observ.out format of NCSMC output,
and make the NCSM_E1_Afi files needed for cross-section calculations.
"""
import file_tools
import dot_in
import os
import re

desired_states = ["1 -1 3", "3 -1 3"]
"""resultant nucleus states we care about, 2J, pi, 2T"""

pn_mode = True
"""ignore isospin quantum numbers"""
#(the transitions code will use proton and neutron components individually)

transitions = ["E1", "E2", "M1"]
"""transitions we care about"""

run_name = "nLi8_n3lo-NN3Nlnl-srg2.0_20_Nmax6"
"""this variable is for naming of output files"""


observ_files = [
    "/Users/callum/Desktop/npsm/_Nmax6_ncsmc_output/Li9_observ_Nmax6_Jz1",
    "/Users/callum/Desktop/npsm/_Nmax6_ncsmc_output/Li9_observ_Nmax7_Nmax6_Jz1"
]
"""paths to observ.out files for resultant nucleus"""

ncsd_file = "/home/callum/ncsd/Li9_n3lo-NN3Nlnl-srg2.0_Nmax8.20"
"""path to ncsd output file for resultant nucleus"""

nmax = 8

def transition_parameter(trans_str):
    """
    Which parameter should we take from lines of data?

    e.g. in the line ``L= 1 E1p= -0.0102   E1n=  0.0102     B(E1)=  0.0001``,
    we want E1p.

    trans_str:
        string, "E1" or something of that sort
    """

    kind = trans_str[0]

    if kind == "E":
        return trans_str+"p"
    elif kind == "M":
        return trans_str
    else:
        raise ValueError("What? Transition = " + trans_str)

def get_radii(ncsd_file, nmax, state):
    """
    Given an ncsd output file, get the values of Rp, Rn, Rm in all
    the required ways. Very similar to dot_out.get_Rs()

    ncsd_file:
        string, path to the ncsd output file for the resultant nucleus
    nmax:
        int, the value of Nmax for which we want to get values
    state:
        (J2, p, T2) tuple, descibes the state for which we want to get radii
    """
    state_J2, _, state_T2 = state
    # these should be integers already but this is so you can use strings too
    state_T2 = int(state_T2)
    state_J2 = int(state_J2)

    # we'll produce an n by n "matrix" with (Rp Rn Rm) entries.
    # some entries may be zero
    r_data = {}

    # split the files into sections using the word "Nmax"
    with open(ncsd_file, "r") as ncsd:
        text = ncsd.read()
    nmax_sections = text.split("Nmax=")

    # select the section we want
    section = None
    for sec in nmax_sections[1:]:  # ignore first section, before any Nmax
        words = sec.split()
        if int(words[0]) == nmax:  # if we find the section with desired nmax
            section = sec
            break
    if section is None:
        raise ValueError("this file doesn't seem to contain the right Nmax!")

    # now find all instances of our state and get radii
    found_state = False
    state_counter = 1
    for line in section.split("\n"):
        if "State #" in line:
            # see if it's a state we care about. Template line:
            #  State # 9   Energy =  -28.4504     J =  2.0230      T =  1.5000
            line = line.replace("State #", "")
            #   9   Energy =  -28.4504     J =  2.0230      T =  1.5000
            num, _, _, E, _, _, J, _, _, T = line.split()
            num = int(num)
            # note that these J and T may not be exact matches
            J2 = float(J) * 2
            T2 = float(T) * 2
            # we'll only take very close matches
            if abs(state_J2 - J2) < 1e-3 and abs(state_T2 - T2) < 1e-3:
                # we found a state with matching J and T!
                found_state = True
        # find the first time after "State #" that "Radius" comes up
        if found_state and "Radius" in line:
            # line looks something like this:
            # Radius: proton=   2.0671  neutron=   2.3067 mass =   2.2199

            # get the data
            _, _, Rp, _, Rn, _, _, Rm = line.split()
            Rp, Rn, Rm = float(Rp), float(Rn), float(Rm)

            # store it in the dict
            r_data[(state_counter, state_counter)] = (Rp, Rn, Rm)

            # then look for the next state
            state_counter += 1
            found_state = False

    # now format it a bit and return
    for state_i in range(1, state_counter):  # loop over every matching state
        for state_f in range(1, state_counter):
            if (state_i, state_f) not in r_data.keys():
                r_data[(state_i, state_f)] = (0.0, 0.0, 0.0)  # filler data
    return r_data



def make_ncsm_e1(desired_states, transitions, run_name,
                 observ_files, ncsd_file, nmax, out_dir=None, verbose=False):
    """
    Makes NCSM_E1_Afi.dat files for the given parameters.

    desired_states:
        list, initial resultant nucleus states we want to consider,
        transitions go from resultant to target states
        e.g. ["1 -1 3", "3 -1 3"]

    transitions:
        list, types of transitions to consider,
        e.g. ["E1", "E2", "M1"]

    run_name:
        string, to use for output naming,
        e.g. "nLi8_n3lo-NN3Nlnl-srg2.0_20_Nmax6_2p1p"

    observ_files:
        list of strings, paths to observ.out files for resultant nucleus,
        e.g. ["/path/to/observ1.out", "/path/to/observ2.out"]

    ncsd_file:
        string, path to ncsd output file for resultant nucleus
        e.g. "/your_dir_here/Li9_n3lo-NN3Nlnl-srg2.0_Nmax8.20"

    nmax:
        int, max number of excitations above the lowest Pauli-allowed state
        e.g. 8
    """

    # store all transitions that will be put in the file, to avoid duplicates
    # if there are two copies of the same transition in multiple files.
    # also note that duplicates might not have EXACTLY the same parameters,
    # down to some rounding error tolerance.
    # I assume the first time we see a transition, that'll be the only one
    # that matters, and others will be duplicates.
    # tolerance is controled by tol here:
    tol = 1e-3
    transition_bank = {}

    # make one ncsm_e1 file for each state
    for desired_state in desired_states:
        # have we got the radii yet?
        added_radii = False

        J2, p, T2 = desired_state.split()
        assert p in ["-1", "1"]
        # get the "2Jparity" name of the state
        # e.g. if 2J=3, parity=1, then name="3p" (for "3 plus")
        j2_parity = J2 + ("m" if p == "-1" else "p")
        # data stores info from observ files, to be written out after the loop
        data = []
        for file_index, filename in enumerate(observ_files):
            # simplify observ file
            simp, num = file_tools.simplify_observ(
                desired_state, transitions, filename, function="make_ncsm_e1", pn_mode=pn_mode)
            num_desired_state = max(num,num_desired_state)
            if simp is None:
                continue
            # get the useful info out of the data lines, e.g. E2p number
            # e.g. E1p in the line L= 1 E1p= -0.0102 E1n= 0.0102 B(E1)= 0.0001
            with open(simp, "r+") as simp_file:
                text = simp_file.read()
            lines = text.splitlines()
            M1_components = [None]*len(lines)
            for t in transitions:
                var = transition_parameter(t)
                for i, line in enumerate(lines):
                    if var in line and line != var:
                        # get the word after var=, i.e. the value
                        words = line.split()
                        try:
                            index = words.index(var+"=")
                        except ValueError:
                            print(line)
                            raise ValueError("Could not find variable "+var)
                        lines[i] = words[index+1]
                    if line=="M1":
                        if lines[i+1][0:2] == "pl":
                            M1_components[i+1] = (lines[i+1].split()[1:8:2])
                     
            text = "\n".join(lines)

            # get transitions from simplified observ.out file
            lines = text.splitlines()
            for i, line in enumerate(lines):
                # get all transitions from the state of interest to others
                if " ++ " + desired_state in line:
                    
                    state_f, state_i = line.split("   ")  # 3 spaces
                    # ignore the bit at the start, and write state as a tuple
                    # which contains (2J, pi, 2T). Record state # too
                    state_f_jpt = tuple(state_f.split()[2:5])  # indices 2 3 4
                    #if pn_mode: state_f_jpt = tuple(state_f.split()[2:4])
                    # we'll only want transitions to final states of interest
                    f_num = state_f.split()[6]
                    # state_i_jpt = state_i.split()[2:5]
                    i_num = state_i.split()[6]
                    transition = lines[i+1]
                    trans_type = transition[1]
                    param = lines[i+2]
                    if state_f_jpt not in transition_bank.keys():
                        transition_bank[state_f_jpt] = {}
                    if trans_type not in transition_bank[state_f_jpt].keys():
                        transition_bank[state_f_jpt][trans_type] = []
                    already_exists = False
                    for inum, fnum, paramval, _ in transition_bank[state_f_jpt][trans_type]:
                        params_are_same = abs(float(paramval) - float(param)) < tol
                        if inum == i_num and fnum == f_num and params_are_same:
                            already_exists = True
                    if not already_exists:
                        if pn_mode:
                           fnum_max = 0
                           for inum, fnum, _, _ in transition_bank[state_f_jpt][trans_type]:
                              if inum == i_num:
                                 if int(fnum) > fnum_max:
                                    fnum_max = int(fnum)
                           f_num = str(fnum_max+1)
                        transition_bank[state_f_jpt][trans_type].append(
                                (i_num, f_num, param, M1_components[i+2]))

            # get E0 transitions from a state to another state with same Q#s
            # careful to just do this once!
            if not added_radii:
                added_radii = True
                radii = get_radii(ncsd_file, nmax, (J2, p, T2))

                if (J2, p, T2) not in transition_bank.keys():
                    transition_bank[(J2, p, T2)] = {}
                if "0" not in transition_bank[(J2, p, T2)].keys():
                    transition_bank[(J2, p, T2)]["0"] = []

                for i in range(1, min(len(radii)+1, num_desired_state+1)):
                    for j in range(1, min(len(radii)+1, num_desired_state+1)):
                        Rp, Rn, Rm = radii[(i, j)]
                        transition_bank[(J2, p, T2)]["0"].append(
                            (str(i), str(j), f"{Rp} {Rn} {Rm}", None))


        # now turn the data in transition_bank into writable lines
        # in the input file format
        lines = []
        # first 2 lines of the file should be initial state description
        lines.append(desired_state)
        lines.append(str(num_desired_state))
        # then go through and write all final states, in the format we need
        for state_f in sorted(transition_bank.keys()):
            for trans_type in sorted(transition_bank[state_f].keys()):
                # how many blocks will we need for this transition?
                blocks = {}
                for transition in transition_bank[state_f][trans_type]:
                    i, f, param, comps = transition
                    if i not in blocks.keys():
                        blocks[i] = 1
                    else:
                        blocks[i] += 1
                # then go through and make each block
                for i_val, n_blocks in blocks.items():
                    # line for the final state quantum numbers
                    lines.append(" ".join(state_f))
                    # line for multipolarity of transition
                    lines.append(str(trans_type))
                    # line for how many lines are in this block
                    line_counter = 0
                    block_lines = []
                    for transition in transition_bank[state_f][trans_type]:
                        i, f, param, comps = transition
                        if i == i_val:
                            line_counter += 1
                            block_lines.append(" ".join([i, f, param]))
                            if not comps is None:
                                block_lines[-1] = " ".join([block_lines[-1]," ".join(comps)])
                    lines.append(str(line_counter))
                    lines += block_lines
        # once we've looped over all files, write data to a file for this state
        if out_dir is None:
            out_dir = os.path.dirname(filename)
        out_name = f'NCSM_E1_Afi_{run_name}_{j2_parity}.dat'
        out_path = os.path.join(out_dir, out_name)
        with open(out_path, "w+") as done_file:
            done_file.write("\n".join(lines)+"\n")
        if verbose:
            print('wrote', out_path)


if __name__ == "__main__":
    make_ncsm_e1(
        desired_states, transitions, run_name, observ_files, ncsd_file, nmax,
        out_dir="")
