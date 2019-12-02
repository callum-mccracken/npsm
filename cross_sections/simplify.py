import re
import os

# name of file we want to simplify
filename = "/Users/callum/Desktop/npsm/cross_sections/Li8Li9/Li9_observ_Nmax6_Jz1"

# state we care about, 2J, pi, 2T
desired_state = "1 -1 3"

# transitions we care about
transitions = ["E2", "M1"]
multipolarity = [int(tr[1]) for tr in transitions]
mtx_elements = ["B" + tr for tr in transitions]

# get all text from file
with open(filename, "r+") as open_file:
    text = open_file.read()

# remove blank spaces in front
if text[0] == " ":
    text = text[1:]
text = text.replace("\n ","\n")

# remove blank lines
text = text.replace("\n\n", "\n")

# remove lines with *** in them
text = re.sub(r'\*\*\*.*\n', '', text)

# remove "Occupation ..." lines
text = re.sub(r'Occupation.*\n', '', text)

nuclei = []
while "Nucleus" in text:
    # The top of the file looks like this:
    """
    Nucleus:
    A=  9   Z=  3   N=  6
    2*MJ=  1   2*MT= -3  parity= -
    hbar Omega= 20.0000   Nhw= 11   dimension= 2945589   nhme=         0
    k1max=  8   mxnwd=  4   mxsps=     256   major= 2   iparity= 1
    J= 1.5000    T= 1.5000     Energy=    -37.0052     Ex=      0.0000
    J= 0.5000    T= 1.5000     Energy=    -35.1180     Ex=      1.8872
    J= 2.5000    T= 1.5000     Energy=    -31.9848     Ex=      5.0204
    J= 1.5000    T= 1.5000     Energy=    -30.9345     Ex=      6.0707
    J= 3.5000    T= 1.5000     Energy=    -29.9713     Ex=      7.0339
    J= 1.5000    T= 1.5000     Energy=    -29.5476     Ex=      7.4576
    J= 2.5000    T= 1.5000     Energy=    -28.4432     Ex=      8.5620
    J= 0.5000    T= 1.5000     Energy=    -27.6044     Ex=      9.4008
    J= 2.5000    T= 1.5000     Energy=    -25.2446     Ex=     11.7606
    J= 1.5000    T= 1.5001     Energy=    -25.1139     Ex=     11.8913
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
        # something like this:
        # J= 2.5000    T= 1.5000     Energy=    -28.4099     Ex=      0.0000
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

# nuclei[0] = initial, nuclei[1] = final
# if one nucleus, initial == final
if len(nuclei) == 1:
    nuclei = nuclei + nuclei
i_parity = nuclei[0][0][3]
f_parity = nuclei[1][0][3]
# find out how many of the desired type of state there are
num_list = []
for state in nuclei[0]:
    _, J2, parity, T2, num, _, _ = state
    if "{} {} {}".format(J2, parity, T2) == desired_state:
        num_list.append(num)
num_desired_state = max(num_list)

# now note that the Ex numbers in nuclei
# are not exactly what's printed.
# for the final nucleus, their energy is relative to the
# ground state of the initial nucleus
i_ground_state = None
for state in nuclei[0]:
    _, _, _, _, _, Ex, E = state
    if Ex == 0:
        if i_ground_state is None:
            i_ground_state = E
        else:
            raise ValueError("failed to find a unique ground state!")
assert i_ground_state is not None

# take only data that is irrelevant to us
# e.g. if we only have "E3" in transitions,
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

# now we have something that looks like
"""
#  1 [2*(J,T),Ex]_f=  5 3  8.5953   #  1 [2*(J,T),Ex]_i=  3 3  0.0000
E1
L= 1 E1p= -0.0189   E1n=  0.0189     B(E1)=  0.0004
#  2 [2*(J,T),Ex]_f=  3 3  9.2805   #  1 [2*(J,T),Ex]_i=  3 3  0.0000
...
"""

# replace the channel titles with new titles
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

def transition_parameter(trans_str):
    """
    Which parameter should we take from lines of data?
    trans_str = "E1" or something like that

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

# get useful info out of the data lines
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

with open(filename+"_simp", "w+") as write_file:
    write_file.write(text)

# now get all transitions from the state of interest to other states
transition_bank = {}
lines = text.splitlines()
for i, line in enumerate(lines):
    if " ++ " + desired_state in line:
        state_f, state_i = line.split("   ")  # 3 spaces
        # remove 1 -- or whatever from the start, and now write states as tuple
        # containg 2J, pi, 2T, number
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
        transition_bank[state_f][trans_type].append((i_num, f_num, param))

lines = []
lines.append(desired_state)
lines.append(str(num_desired_state))
for state_f in transition_bank.keys():
    lines.append(" ".join(state_f))
    for trans_type in transition_bank[state_f].keys():
        lines.append(str(trans_type))
        lines.append(str(len(transition_bank[state_f][trans_type])))
        for transition in transition_bank[state_f][trans_type]:
            i, f, param = transition
            lines.append(" ".join([i, f, param]))

out_name = filename + "_reformat_"+desired_state.replace(" ", "_")
with open(out_name, "w+") as done_file:
    done_file.write("\n".join(lines)+"\n")


