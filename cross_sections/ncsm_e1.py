"""
A script to take files from the ``observ.out`` format of NCSMC output,
to the ``NCSM_E1_Afi`` format needed for cross-section calculations.
"""

import file_tools
import os
import re
# state we care about, 2J, pi, 2T
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


def transition_parameter(trans_str):
    """
    Which parameter should we take from lines of data?
    
    trans_str = "E1" or something of that sort

    e.g. in the line ``L= 1 E1p= -0.0102   E1n=  0.0102     B(E1)=  0.0001``,

    we want E1p.
    """
    kind, order = trans_str[0], trans_str[1]
    if kind == "E":
        return trans_str+"p"
    elif kind == "M":
        return trans_str
    else:
        raise ValueError("What? Transition = " + trans_str)


def make_ncsm_e1(desired_states, transitions, run_name, files, out_dir=None):
    """
    Makes NCSM_E1_Afi.dat files for the given parameters.

    Params:
        ``desired_states``: a list of initial states we want to consider,
            e.g. ``["1 -1 3", "3 -1 3"]``
        
        ``transitions``: a list of transitions to consider,
            e.g. ``["E1", "E2", "M1"]``
        
        ``run_name``: a string to use for output naming,
            e.g. ``"nLi8_n3lo-NN3Nlnl-srg2.0_20_Nmax6_2p1p"``
        
        ``files``: a list of strings with paths to observ.out files
            e.g. ``files = ["/path/to/observ1.out", "/path/to/observ2.out"]``
    """
    # multipolarity of each transition
    multipolarity = [int(tr[1]) for tr in transitions]
    # what kind of matrix elements should we save in the ncsm_e1 file?
    mtx_elements = ["B" + tr for tr in transitions]
    # make one file for each state
    for desired_state in desired_states:
        # get the "3m" name of the state
        # e.g. if 2J=3, parity = 1, name=3p for 3 plus
        J2, p, _ = desired_state.split()
        assert p in ["-1", "1"]
        j2_parity = J2 + "m" if p == "-1" else "p"
        # data stores info from both files, to be written out after the loop
        data = []
        for file_index, filename in enumerate(files):
            simp, num = file_tools.simplify_observ(
                desired_state, transitions, filename, function="make_ncsm_e1")
            num_desired_state = num
            # now get the useful info out of the data lines, e.g. E2p number
            with open(simp, "r+") as simp_file:
                text = simp_file.read()
            lines = text.splitlines()
            for t in transitions:
                var = transition_parameter(t)
                for i, line in enumerate(lines):
                    if var in line and line != var:
                        # remove stuff before it
                        lines[i] = re.sub(r'.*'+var, '', line)
                        # then the variable of interest is the second word
                        words = lines[i].split()
                        lines[i] = words[1]
            text = "\n".join(lines)
            # now get all transitions from the state of interest to other states
            transition_bank = {}
            lines = text.splitlines()
            for i, line in enumerate(lines):
                if " ++ " + desired_state in line:
                    state_f, state_i = line.split("   ")  # 3 spaces
                    # ignore the bit at the start, and write state as a tuple
                    # which contains (2J, pi, 2T). Record state # too
                    l = state_f.split()
                    state_f = (l[2], l[3], l[4])
                    f_num = l[6]
                    l = state_i.split()
                    state_i = (l[2], l[3], l[4])
                    i_num = l[6]
                    transition = lines[i+1]
                    trans_type = transition[1]
                    param = lines[i+2]
                    if state_f not in transition_bank.keys():
                        transition_bank[state_f] = {}
                    if trans_type not in transition_bank[state_f].keys():
                        transition_bank[state_f][trans_type] = []
                    transition_bank[state_f][trans_type].append(
                        (i_num, f_num, param))

            # now turn the data in transition_bank into writable lines
            # in the input file format
            lines = []
            # first 2 lines of the file should be initial state description
            if file_index == 0:
                lines.append(desired_state)
                lines.append(str(num_desired_state))
            # then go through and write all final states, in the format we need
            for state_f in sorted(transition_bank.keys()):
                for trans_type in sorted(transition_bank[state_f].keys()):
                    # how many blocks will we need for this transition?
                    total_trans = len(transition_bank[state_f][trans_type])
                    blocks = {}
                    for transition in transition_bank[state_f][trans_type]:
                        i, f, param = transition
                        if i not in blocks.keys():
                            blocks[i] = 1
                        else:
                            blocks[i] += 1
                    for i_val, n_blocks in blocks.items():
                        # line for the final state quantum numbers
                        lines.append(" ".join(state_f))
                        # line for multipolarity of transition
                        lines.append(str(trans_type))
                        # line for how many lines are in this block
                        line_counter = 0
                        block_lines = []
                        for transition in transition_bank[state_f][trans_type]:
                            i, f, param = transition
                            if i == i_val:
                                line_counter += 1
                                block_lines.append(" ".join([i, f, param]))
                        lines.append(str(line_counter))
                        lines += block_lines
            # add the lines from this file to overall set of lines / data
            data += lines
        # once we've looped over all files, write data to a file for this state
        if out_dir is None:
            out_dir = os.path.dirname(filename)
        out_name = f'NCSM_E1_Afi_{run_name}_{j2_parity}.dat'
        out_path = os.path.join(out_dir, out_name)
        with open(out_path, "w+") as done_file:
            done_file.write("\n".join(data)+"\n")

if __name__ == "__main__":
    make_ncsm_e1(desired_states, transitions, run_name, files, out_dir="")
