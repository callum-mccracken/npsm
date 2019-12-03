"""
A script to take files from the ``observ.out`` format of NCSMC output,
to the ``NCSM_E1_Afi`` format needed for cross-section calculations.
"""

import re
import os

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

def make(desired_states, transitions, run_name, files):
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
            # get all text from file
            with open(filename, "r+") as open_file:
                text = open_file.read()

            # remove blank spaces in front of lines, e.g. \n Line1\n Line2
            if text[0] == " ":
                text = text[1:]
            text = text.replace("\n ","\n")

            # remove blank lines
            text = text.replace("\n\n", "\n")

            # remove lines with *** in them
            text = re.sub(r'\*\*\*.*\n', '', text)

            # remove "Occupation ..." lines
            text = re.sub(r'Occupation.*\n', '', text)

            # make a list to store states of initial and final nuclei
            nuclei = []
            while "Nucleus" in text:
                # The top of the file looks something like this:
                """
                Nucleus:
                A=  9   Z=  3   N=  6
                2*MJ=  1   2*MT= -3  parity= -
                hbar Omega= 20.0000   Nhw= 11  dimension= 2945589 nhme=  0
                k1max=  8   mxnwd=  4   mxsps=     256   major= 2   iparity= 1
                J= 1.5000    T= 1.5000     Energy=    -37.0052     Ex=   0.0000
                J= 0.5000    T= 1.5000     Energy=    -35.1180     Ex=   1.8872
                J= 2.5000    T= 1.5000     Energy=    -31.9848     Ex=   5.0204
                J= 1.5000    T= 1.5000     Energy=    -30.9345     Ex=   6.0707
                J= 3.5000    T= 1.5000     Energy=    -29.9713     Ex=   7.0339
                J= 1.5000    T= 1.5000     Energy=    -29.5476     Ex=   7.4576
                J= 2.5000    T= 1.5000     Energy=    -28.4432     Ex=   8.5620
                J= 0.5000    T= 1.5000     Energy=    -27.6044     Ex=   9.4008
                J= 2.5000    T= 1.5000     Energy=    -25.2446     Ex=  11.7606
                J= 1.5000    T= 1.5001     Energy=    -25.1139     Ex=  11.8913
                N1_max=   7   N12_max=   8   Nasps= 237
                wave functions of the states #  1- # 10 used
                """
                lines = text.splitlines()
                # scroll through until you find Nucleus
                if "Nucleus" in lines[0]:
                    lines = lines[1:]
                else:
                    try:
                        continue
                    except IndexError:
                        raise ValueError("Nucleus not found!")
                # grab nucleus info
                nucleus_info, lines = lines[:4], lines[4:]
                plus_or_minus = nucleus_info[1].split()[-1]
                parity = int(plus_or_minus + "1")
                states = []
                state_nums = {}
                state_counter = 1
                while "J=" == lines[0][:2]:
                    # something like this (with different #s of spaces, maybe):
                    # J= 2.5000    T= 1.5000  Energy=    -28.4099  Ex=   0.0000
                    words = lines[0].split()
                    J, T, E, Ex = words[1], words[3], words[5], words[7]
                    J, T, E, Ex = list(map(float, [J, T, E, Ex]))
                    J2 = round(J * 2)
                    T2 = round(T * 2)
                    if (J2, T2) not in state_nums.keys():
                        state_nums[(J2, T2)] = 1
                    else:
                        state_nums[(J2, T2)] += 1
                    num = state_nums[(J2, T2)]
                    state = [state_counter, J2, parity, T2, num, Ex, E]
                    state_counter += 1
                    states.append(state)
                    lines = lines[1:]
                # then when you reach the end take the next couple lines
                extra_lines, lines = lines[:2], lines[2:]
                # the second of those should tell you how many states were used
                states_line = extra_lines[1]
                # e.g. wave functions of the states #  1- # 10 used
                n_states = int(states_line.split()[-2])
                states = states[:n_states]
                nuclei.append(states)
                text = "\n".join(lines)

            assert len(nuclei) < 3  # let us pray this never fails
            # assuming all went well, now we have
            # nuclei[0] = initial, nuclei[1] = final
            # if we only have one nucleus, set initial == final
            if len(nuclei) == 1:
                nuclei = nuclei + nuclei
            # nuclei entries are states
            # nuclei[i][j] = [state_counter, J2, parity, T2, num, Ex, E]
            i_parity = nuclei[0][0][2]
            f_parity = nuclei[1][0][2]

            # find out how many of the desired type of state there are
            num_list = []
            for state in nuclei[0]:
                _, J2, parity, T2, num, _, _ = state
                if "{} {} {}".format(J2, parity, T2) == desired_state:
                    num_list.append(num)
            num_desired_state = max(num_list)

            # Now note that the Ex numbers in nuclei
            # are not exactly what's printed in the observ.out files.
            # For the final nucleus, their energy is relative to the
            # ground state of the initial nucleus
            i_ground_state = None
            for state in nuclei[0]:
                _, _, _, _, _, Ex, E = state
                if Ex == 0:
                    if i_ground_state is None:
                        i_ground_state = E
                    else:
                        raise ValueError("can't find initial ground state!")
            assert i_ground_state is not None

            # take only data that is relevant to us
            # e.g. if we only have transitions = ["E3"] up top,
            # keep lines with E3 transitions and discard others
            lines = text.splitlines()
            interesting_lines = []
            state_line = ""
            for m in mtx_elements:
                line_to_find = m + " matrix elements:"
                for i, line in enumerate(lines):
                    if line[0] == "#":
                        state_line = line
                    elif line == line_to_find:
                        interesting_lines += [state_line, m[1:], lines[i+1]]
            text = "\n".join(interesting_lines)

            # now we have something that looks mostly like this:
            """
            #  1 [2*(J,T),Ex]_f=  5 3  8.5953   #  1 [2*(J,T),Ex]_i= 3 3 0.0000
            E1
            L= 1 E1p= -0.0189   E1n=  0.0189     B(E1)=  0.0004
            #  2 [2*(J,T),Ex]_f=  3 3  9.2805   #  1 [2*(J,T),Ex]_i= 3 3 0.0000
            ...
            """

            # replace the channel titles with new titles, for easier processing
            title_lines = re.findall(r"# .*   # .*\n", text)
            title_lines = [t.replace("\n", "") for t in title_lines]
            i_to_replace = []
            f_to_replace = []
            for t in title_lines:
                f_title, i_title = t.split("   ")
                if i_title not in i_to_replace:
                    i_to_replace.append(i_title)
                if f_title not in f_to_replace:
                    f_to_replace.append(f_title)
            # replace initial state titles
            for title in i_to_replace:
                _, num, _, J2, T2, Ex = title.split()
                num, J2, T2, Ex = list(map(float, [num, J2, T2, Ex]))
                num, J2, T2 = int(num), int(J2), int(T2)
                # find a matching state in nuclei[0]
                for state in nuclei[0]:
                    i_num, i_J2, i_parity, i_T2, state_num, i_Ex, _ = state
                    if num == i_num and J2 == i_J2 and T2 == i_T2 and Ex == i_Ex:
                        new_name = "{} ++ {} {} {} # {}".format(
                            num, J2, i_parity, T2, state_num)
                        text = text.replace(title, new_name)
                        break
            # replace final state titles
            for title in f_to_replace:
                _, num, _, J2, T2, Ex = title.split()
                num, J2, T2, Ex = list(map(float, [num, J2, T2, Ex]))
                num, J2, T2 = int(num), int(J2), int(T2)
                # find a matching state in nuclei[1]
                for state in nuclei[1]:
                    f_num, f_J2, f_parity, f_T2, state_num, f_Ex, f_E = state
                    # replace f_Ex with the actual printed value
                    f_Ex = f_E - i_ground_state
                    diff = abs(Ex - f_Ex)
                    if num == f_num and J2 == f_J2 and T2 == f_T2 and diff < 1e-5:
                        new_name = "{} -- {} {} {} # {}".format(
                            num, J2, f_parity, T2, state_num)
                        text = text.replace(title, new_name)
                        break

            # now get the useful info out of the data lines, e.g. E2p number
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
        out_dir = os.path.dirname(filename)
        out_name = f'NCSM_E1_Afi_{run_name}_{j2_parity}.dat'
        out_path = os.path.join(out_dir, out_name)
        with open(out_path, "w+") as done_file:
            done_file.write("\n".join(data)+"\n")

if __name__ == "__main__":
    make(desired_states, transitions, run_name, files)
