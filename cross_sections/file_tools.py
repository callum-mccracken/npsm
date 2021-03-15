"""
A module for processing files from NCSMC output.
"""
import re
from os.path import basename, join
import cross_sections_utils

def simplify_observ(desired_state, transitions, filename, function=None, verbose=True):
    """
    Makes a "simplified" version of an ``observ.out`` file.

    desired_state:
        string, of the form 2J, pi, 2T, e.g. "3 -1 3"

    transitions:
        a list of transitions to keep in the file, e.g. ["E1"]

    filename:
        string, the path to the observ.out file.

    function:
        string, name of function calling this function

    Returns:
        simp_path:
            the path to the simplified file

        if function == "make_ncsm_e1", this also returns

        num_desired_state:
            the number of states with the same quantum
            numbers as the desired state
    """
    if verbose:
        print("simplifying", filename)
    # get all text from file
    with open(filename, "r+") as open_file:
        text = open_file.read()

    # remove blank spaces in front of lines, e.g. \n Line1\n Line2
    if text[0] == " ":
        text = text[1:]
    text = text.replace("\n ", "\n")

    # remove blank lines
    text = text.replace("\n\n", "\n")

    # remove lines with *** in them which do not contain =
    lines = text.splitlines()
    newlines = []
    for line in lines:
        if ("***" in line) and ("=" not in line):
            pass
        else:
            newlines.append(line)
    text = "\n".join(newlines)

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
            #print(lines[0])
            #print(lines[1])
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
        #print("getting state info: state, 2J, pi, 2T, num, Ex, E")
        while "J=" == lines[0][:2]:
            # something like this (with different #s of spaces, maybe):
            # J= 2.5000    T= 1.5000  Energy=    -28.4099  Ex=   0.0000
            # but note that we might have something like J=2.499
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
        nuclei.append(nuclei[0])
    # nuclei entries are states
    # nuclei[i][j] = [state_counter, J2, parity, T2, num, Ex, E]
    i_parity = nuclei[0][0][2]
    f_parity = nuclei[1][0][2]

    # find out how many of the desired state there are
    num_list = []
    for state in nuclei[0]:
        _, J2, parity, T2, num, _, _ = state
        if "{} {} {}".format(J2, parity, T2) == desired_state:
            num_list.append(num)
    if len(num_list) == 0:
        print("Desired state {}".format(desired_state),
              "not found in {}".format(filename))
        return None, 0
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
    
    # we have data lines of the form:

    # #  4 [2*(J,T),Ex]_f=  5 1  7.5177   #  3 [2*(J,T),Ex]_i=  7 1  4.8240
    #
    # BM1 matrix elements:
    # pl= -0.2839   nl=  0.0257   ps= -0.0163   ns=  0.2745 M1= -1.4256 B(M1)=  2.0322
    #
    # BE2 matrix elements:
    # L= 2 E2p=  1.1540   E2n=  0.2056     B(E2)=  1.3318
    #
    # BE4 matrix elements:
    # L= 4 E4p= -5.9098   E4n= -2.9355     B(E4)= 34.9253
    #
    # BE6 matrix elements:
    # L= 6 E6p= 22.9857   E6n= 11.2814     B(E6)=528.3428

    # we want to record what state we're on (top line)
    # then scroll through taking all relevant data until we hit the next state

    lines = text.splitlines()
    interesting_lines = []
    state_line = None  # this will hold the "top line"
    mtx_elements = ["B" + tr for tr in transitions]
    #print(mtx_elements)
    for m in mtx_elements:  # find each kind of transition we want
        # the line with the data will look like "BM1 matrix elements: ..."
        line_to_find = m + " matrix elements:"
        for i, line in enumerate(lines):
            if line[0] == "#":
                state_line = line
            #elif "#" in line:
            #    print('noop', line)
            elif line == line_to_find:
                interesting_lines += [state_line, m[1:], lines[i+1]]
            #print(interesting_lines)
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
    #print("replacing initial state titles")
    state_counter = {}
    for title in i_to_replace:
        _, num, _, J2, T2, Ex = title.split()
        num, J2, T2, Ex = list(map(float, [num, J2, T2, Ex]))
        num, J2, T2 = int(num), int(J2), int(T2)
        if (J2, T2) not in state_counter.keys():
            state_counter[(J2, T2)] = 1
        else:
            state_counter[(J2, T2)] += 1
        # find a matching state in nuclei[0]
        i_num, _, i_parity, _, state_num, _, E = nuclei[0][num-1]  # num is 1-based, not 0-based
        assert num == i_num
        new_name = "{} ++ {} {} {} # {} {}".format(
            num, J2, i_parity, T2, state_counter[(J2, T2)], E)
        #print("replacing", title, "with", new_name)
        text = text.replace(title, new_name)

    # replace final state titles
    #print("replacing final state titles")
    state_counter = {}
    for title in f_to_replace:
        _, num, _, J2, T2, Ex = title.split()
        num, J2, T2, Ex = list(map(float, [num, J2, T2, Ex]))
        num, J2, T2 = int(num), int(J2), int(T2)
        if (J2, T2) not in state_counter.keys():
            state_counter[(J2, T2)] = 1
        else:
            state_counter[(J2, T2)] += 1
        # find a matching state in nuclei[0]
        f_num, _, f_parity, _, state_num, _, E = nuclei[1][num-1]  # num is 1-based, not 0-based
        assert num == f_num
        new_name = "{} -- {} {} {} # {} {}".format(
            num, J2, f_parity, T2, state_counter[(J2, T2)], E)
        #print("replacing", title, "with", new_name)
        text = text.replace(title, new_name)

    simp_path = filename+"_simp"
    with open(simp_path, "w+") as simp_file:
        simp_file.write(text)
    #print('wrote output to', simp_path)

    if function == "make_ncsm_e1":
        return simp_path, num_desired_state
    elif function == "transitions":
        return simp_path
    else:
        return simp_path


def make_wf_file(wavefunction_NCSMC_file, res_state, run_dir):
    """
    Makes a wavefunction_NCSMC file for the resultant nucleus

    wavefunction_NCSMC_file:
        string, path to the original wavefunction_NCSMC file

    res_state:
        string, of the form "2J parity 2T", state of resultant nucleus

    run_dir:
        string, directory where we'll save the new file
    """
    with open(wavefunction_NCSMC_file, "r+") as wf_file:
        lines = wf_file.readlines()

    # look for the line that designates the res_state's segment of the file
    segments = []
    segment = []
    hashtag_counter = 0
    for line in lines:
        if "#" in line:
            # if it's one of the lines related to a section break, it should
            # have #words < 5 (I'm pretty sure this should always work, right?)
            if len(line.split()) < 5:
                hashtag_counter += 1
        if hashtag_counter == 5:
            # we've started a new segment
            hashtag_counter = 0
            segments.append(segment)
            segment = []
        segment.append(line)
    # then add the last segment
    segments.append(segment)

    # now pick which segment to save by comparing J, parity, T
    J2, parity, T2 = map(int, res_state.split())
    the_chosen_one = None
    for segment in segments:
        first_line = segment[0]
        seg_J2, seg_parity, seg_T2 = map(int, first_line.split()[1:])
        if J2 == seg_J2 and parity == seg_parity and T2 == seg_T2:
            the_chosen_one = segment
    assert the_chosen_one is not None

    # save that segment back out to a file
    state_name = cross_sections_utils.get_state_name(res_state)
    # I assume the filename ends with .agr
    filename = basename(wavefunction_NCSMC_file)[:-4]
    out_path = join(run_dir, filename + "_" + state_name + ".agr")
    with open(out_path, "w+") as out_file:
        out_file.writelines(the_chosen_one)
    return out_path
