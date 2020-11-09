"""
A module for making transitions_NCSMC.in files
"""

import file_tools
import cross_sections_utils
import shutil
import os
import re

# some manual input / default values

r_matching = 18.0
r_zero = 50.0
n_points = 10000
n_bound_resultant = 1
n_scattering_resultant = 1
n_bound_proj = 1
Eexpt = 0.0
nsig_min = 0
nsig_max = 1

# other parameters to adjust if you want to run this file on its own
# note these are not used when calling functions externally

ncsd_file = "/home/callum/exch/Li8Li9/ncsd/Li8_n3lo-NN3Nlnl-srg2.0_Nmax0-10.20"
"""the ncsd output file for the target"""

observ_file = "/Users/callum/Desktop/npsm/_Nmax6_ncsmc_output/Li8_observ_Nmax6_Jz1"
"""the observ.out file for the target"""

shift_file = "/Users/callum/Desktop/npsm/_Nmax6_ncsmc_output/phase_shift_nLi8_n3lo-NN3Nlnl-srg2.0_20_Nmax6.agr"
"""the eigenphase_shift or phase_shift file, for getting energy bounds"""

run_name = "nLi8_n3lo-NN3Nlnl-srg2.0_20_Nmax6"
"""a string that input files contain"""

state_name = "3m"
"""the state name of a bound state in the resultant nucleus"""

naming_str = "NCSMC_E1M1E2_Li9_2J_3"
"""a string for naming output files"""

transitions = ["E2", "M1"]
"""the transitions we want to keep track of"""

proj = "n"
"""the projectile we're using, curently only "n" and "p" are supported"""

target_bound_states = [
    # Format: 2J, parity, 2T, num, binding energy. First entry = ground state.
    [4, 1, 2, 1, -34.8845],
    [2, 1, 2, 1, -33.7694]
]
"""bound states of the target nucleus."""


def parameter_list(transition):
    """
    Returns the parameters we should take from the observ.out file,
    for each type of transition. E.g.::

        >> parameter_list("E2")
        ["E2p", "E2n"]
    """
    param_dict = {
        "E2": ["E2p", "E2n"],
        "M1": ["pl", "nl", "ps", "ns"]
    }
    return param_dict[transition]


def get_e_m_transitions(simp_file_text, target_bound_states, lamb_max):
    """
    Given a simplified observ.out file and the bound states of the target,
    get lists containg the values to be printed for E and M transitions
    between those bound states.

    simp_file_text:
        string, the text of a simplified observ.out file

    target_bound_states:
        list of bound states, formatted like
        ``[[J2, parity, T2, num, energy], ...]``

    lamb_max:
        integer, lambda = multipolarity of a transition. If we have some block
        of e transitions that looks like this::

            2 1 1 1.4850 2.4430 ! targ E mul i f  Mp Mn
            2 1 2 -0.7626 -1.5856 ! targ E mul i f  Mp Mn
            2 2 1 0.9845 2.0470 ! targ E mul i f  Mp Mn
            2 2 2 1.0374 0.8974 ! targ E mul i f  Mp Mn

        then we're going to have a problem, since the code needs to read lines with
        all possible values from 1 to lamb_max as the first number.
        Same deal with the second and third.

    """
    e_transitions = {}
    m_transitions = {}

    # simp_file_text comes in groups of 3 lines:
    # states, transition, data
    lines = simp_file_text.split("\n")
    while lines != []:
        # get first 3 lines
        states_line, transition, data_line = lines[0:3]
        # then cut off the  3 lines
        lines = lines[3:]

        # now get info about these 3 lines
        multipolarity = int(transition[1:])  # like 2 for M2
        e_or_m = transition[0]  # the letter E or M
        # find state #s, i.e. their indices in target_bound_states
        # the states look like this: 9 -- 6 1 2 # 2 -26.2739
        # [num in observ.out] [i/f] [J2, pi, T2] # [num state with J2 pi T2] [Energy]
        state_f, state_i = states_line.split("   ")
        _, _, J2_f, pi_f, T2_f, _, num_f, E_f = state_f.split()
        _, _, J2_i, pi_i, T2_i, _, num_i, E_i = state_i.split()

        J2_f, pi_f, T2_f, num_f = int(J2_f), int(pi_f), int(T2_f), int(num_f)
        J2_i, pi_i, T2_i, num_i = int(J2_i), int(pi_i), int(T2_i), int(num_i)

        E_f = float(E_f)
        E_i = float(E_i)

        state_f = [J2_f, pi_f, T2_f, num_f, E_f]
        state_i = [J2_i, pi_i, T2_i, num_i, E_i]
        
        #print("looking at transition:", state_i, state_f)
        # there was a bit of an issue earlier with having states from
        # target_bound_states not quite matching with states from the
        # observ.out files...
        # I solved this by having it be possible for there to be a little
        # possible discrepancy in energies from the rgm.out and observ.out files

        def one_match(state, bound_states):
            """
            returns false if there is no match to state in bound_states.
            If there is one match, returns the index of that match + 1.
            If more than one match, raises ValueError.
            """
            found_match = False
            index = None
            J2_s, pi_s, T2_s, num_s, _ = state
            for i, bs in enumerate(bound_states):
                J2_bs, pi_bs, T2_bs, num_bs, _ = bs
                if J2_s == J2_bs and pi_s == pi_bs and T2_s == T2_bs and num_s == num_bs:
                    if not found_match:
                        found_match = True
                        index = i + 1
                    else:
                        # more than one match!
                        raise ValueError("More than one match!")
            if found_match:
                return index
            else:
                return False

        # consider only transitions to a bound state from another bound state
        match_f = one_match(state_f, target_bound_states)
        match_i = one_match(state_i, target_bound_states)
        if match_f and match_i:
            #print("both states are bound!")
            index_f = match_f
            index_i = match_i
        else:
            #print("this transition is not bound-state to bound-state")
            #print("ignoring...")
            continue
        #print("getting transition info:", state_i, "to", state_f)
        #print("transition type:", transition)
        var_list = parameter_list(transition)
        data_line_hunks = data_line.split()
        data = {}
        for var in var_list:
            for j, hunk in enumerate(data_line_hunks):
                if var+"=" == hunk:
                    value = data_line_hunks[j+1]
                    data[var] = value
        if e_or_m == "E":
            t = (multipolarity, index_i, index_f)
            d = (data["E2p"], data["E2n"])
            if t not in e_transitions.keys():
                e_transitions[t] = d
            #print(t, d)
        else:
            t = (index_i, index_f)
            d = (data["pl"],data["nl"], data["ps"], data["ns"])
            if t not in m_transitions.keys():
                m_transitions[t] = d
            #print(t, d)

    for k in m_transitions.keys():
        print(k, m_transitions[k])
    

    # ensure that e_transitions has the correct form
    new_e_trans = []
    for l in range(1, lamb_max+1):
        for i in range(1, len(target_bound_states) + 1):
            for j in range(1, len(target_bound_states) + 1):
                if (l, i, j) not in e_transitions.keys():
                    E2p, E2n = "0.d0", "0.d0"
                else:
                    E2p, E2n = e_transitions[(l, i, j)]
                new_e_trans.append([l, i, j, E2p, E2n])
    # and m too
    new_m_trans = []
    for l in range(1, len(target_bound_states) + 1):
        for i in range(1, len(target_bound_states) + 1):
            if (l, i) not in m_transitions.keys():
                Mpl, Mnl, Mls, Mns = "0.0000", "0.0000", "0.0000", "0.0000"
            else:
                Mpl, Mnl, Mls, Mns = m_transitions[(l, i)]
            new_m_trans.append([l, i, Mpl, Mnl, Mls, Mns])


    return new_e_trans, new_m_trans


def get_bound_state_str(target_bound_states):
    """
    The .in file has a few lines dedicated to describing target bound states,
    this file makes those.

    target_bound_states:
        list of bound states, formatted like
        ``[[J2, parity, T2, num, energy], ...]``
    """
    bound_state_fmt = "{E}d0   {J2}  {parity}  {T2}     ! E, 2J, pi, 2T"
    targ_bound_str = ""
    for i, state in enumerate(target_bound_states):
        J2, p, T2, num, E = state
        targ_bound_str += bound_state_fmt.format(E=E, J2=J2, parity=p, T2=T2)
        if i+1 != len(target_bound_states):
            targ_bound_str += "\n"
    return targ_bound_str


def get_transition_lines(e_transitions, m_transitions):
    """
    The .in file has lines which describe E/M transitions between bound states
    of the target.

    Givem e_transitions, m_transitions, make those lines.

    e_transitions:
        list of lists of floats, format: [[m, i, f, Mp, Mn], ...]

    m_transitions:
        list of lists of floats, format: [[i, f, Mlp, Mln, Msp, Msn], ...]

    """
    e_fmt = "{multipolarity} {i} {f} {Mp} {Mn} ! targ E mul i f  Mp Mn\n"
    e_lines = ""
    for m, i, f, Mp, Mn in e_transitions:
        e_lines += e_fmt.format(multipolarity=m, i=i, f=f, Mp=Mp, Mn=Mn)
    m_fmt = "  {i} {f} {Mlp} {Mln} {Msp} {Msn} ! targ M1 i f Mlp Mln Msp Msn\n"
    m_lines = ""
    for i, f, Mlp, Mln, Msp, Msn in m_transitions:
        m_lines += m_fmt.format(i=i, f=f, Mlp=Mlp, Mln=Mln, Msp=Msp, Msn=Msn)
    return e_lines, m_lines


def get_freq(observ_file):
    """
    Get the frequency (Nhw) used for the calculation

    observ_file:
        path to observ.out file
    """
    with open(observ_file, "r+") as observ:
        lines = observ.readlines()
    freq_line = lines[3]
    freq_word = freq_line.split()[2]
    return float(freq_word)


def get_target_info(observ_file):
    """
    Gets A, Z, J2, parity, T2 for the target.

    observ_file:
        path to observ.out file
    """

    with open(observ_file, "r+") as observ:
        lines = observ.readlines()
    # get parity
    parity_line = lines[2]
    parity_str = parity_line.split()[-1]
    parity = 1 if parity_str == "+" else -1
    # get 2J, 2T
    state_lines = [l for l in lines if " J=" in l]
    ground_state_line = state_lines[0]
    """ J= 2.0000    T= 1.0001     Energy=    -34.8845     Ex=      0.0000"""
    gs_words = ground_state_line.split()
    J2 = 2 * round(float(gs_words[1]))
    T2 = 2 * round(float(gs_words[3]))
    # get A, Z
    A_Z_line = lines[1]
    A_Z_words = A_Z_line.split()
    A = int(A_Z_words[1])
    Z = int(A_Z_words[3])
    target_info = A, Z, J2, parity, T2
    return target_info


def get_proj_info(projectile):
    """
    get A, Z, 2J, parity, 2T for a projectile

    projectile:
        string, e.g. "n" or "p"

    Warning:
        currently "n" and "p" are supported, I haven't got around to a
        more general implementation
    """

    if projectile == "n":
        return [1, 0, 1, 1, 1]
    elif projectile == "p":
        return [1, 1, 1, 1, 1]  # TODO: that's right, right?
    #elif ... add your own special case here
    else:
        raise ValueError("I'm not sure how to process this projectile!")


def get_energy_info(shift_file):
    """
    The shift_file is a path to a file that looks something like this::

        @ s0 legend "1\\S-\\N3"
        0.02000      -0.05754   0.00000   0.00001
        0.04000      -0.15804   0.00000   0.00005
        ...
        10.00000     -0.73485   0.00000   0.00066
        &

    Let's get the minimum energy, maximum energy, and energy step

    """
    with open(shift_file, "r+") as f:
        lines = f.readlines()
    counter = 0
    for line in lines:
        words = line.split()
        if line == "&":  # end case
            break
        elif all([cross_sections_utils.is_float(word) for word in words]):
            # the line contains only numbers --> first number is energy
            energy = float(words[0])
            if counter == 0:
                Emin = energy
            elif counter == 1:
                Emax = energy
                Estep = energy - Emin
            else:
                Emax = energy
            counter += 1
        else:
            # could be a title, maybe a blank line?
            continue
    return Emin, Emax, Estep

def get_Rs(ncsd_file, nmax):
    """
    Given an ncsd output file, get the values of Rp, Rn, Rm

    ncsd_file:
        string, path to the ncsd output file for the target nucleus
    nmax:
        int, the value of Nmax for which we want to get values
    
    """
    Rp, Rn, Rm = None, None, None

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

    # now find the ground state, identified by "State # 1"
    # TODO: are the R values always the ones from the ground state?
    found_state = False
    for line in section.split("\n"):
        if "State # 1" in line:
            found_state = True

        # find the first time after "State #1" that "Radius" comes up
        if found_state and "Radius" in line:
            # line looks something like this:
            # Radius: proton=   2.0671  neutron=   2.3067 mass =   2.2199
            _, _, Rp, _, Rn, _, _, Rm = line.split()
            Rp, Rn, Rm = float(Rp), float(Rn), float(Rm)
            break

    if any([Rp is None, Rn is None, Rm is None]):
        raise ValueError("Rp, Rn, or Rm not found!")

    return Rp, Rn, Rm


def make_dot_in(proj, target_bound_states, run_name,
                state_name, naming_str, ncsd_file, nmax,
                observ_file, transitions, shift_file,
                out_dir=None):
    """
    Makes a transitions_NCSMC.in file.

    proj:
        string, the projectile, e.g. "n", or list of [A, Z, 2J, pi, 2T]

    target_bound_states:
        list, info about bound states of the target.
        Formatted like ``[[J2, parity, T2, num, energy], ...]``

    run_name:
        string, name of directory where we'll put files

    state_name:
        string, state of resultant nucleus, in "2Jparity" format, e.g. "1m"

    naming_str:
        string, for naming stuff after the run is complete

    ncsd_file:
        string, path to the ncsd output file for the target nucleus

    nmax:
        int, value of Nmax (excitations above lowest Pauli state)

    observ_file:
        string, path to the observ.out file for the target nucleus

    transitions:
        list of strings, transitions we'll consider, e.g. ["E2", "M1"]

    shift_file:
        string, path to a phase_shift or eigenphase_shift file

    out_dir:
        string, directory where we'll save the file

    """

    # get Rp, Rn, Rm
    Rp, Rn, Rm = get_Rs(ncsd_file, nmax)

    multipolarities = [int(t[1]) for t in transitions]
    lamb_min = min(multipolarities)
    lamb_max = max(multipolarities)


    # get info abount reactants, t = target, p = projectile
    t_A, t_Z, t_gs_J2, t_gs_parity, t_gs_T2 = get_target_info(observ_file)
    proj_info = proj if type(proj) == list else get_proj_info(proj)
    p_A, p_Z, p_gs_J2, p_gs_parity, p_gs_T2 = proj_info

    n_bound_target = len(target_bound_states)

    # in your ncsmc run, what were the min/max energy values and step size?
    Emin, Emax, Estep = get_energy_info(shift_file)

    # simplify observ file, get text
    shutil.copyfile(observ_file, os.path.split(observ_file)[1])
    ground_state = " ".join(map(str, target_bound_states[0][:3]))
    simp = file_tools.simplify_observ(ground_state, transitions, observ_file)
    with open(simp, "r+") as simp_file:
        text = simp_file.read()

    # get frequency from observ file
    hw = get_freq(observ_file)

    e_transitions, m_transitions = get_e_m_transitions(
        text, target_bound_states, lamb_max)
    targ_bound_str = get_bound_state_str(target_bound_states)
    e_lines, m_lines = get_transition_lines(e_transitions, m_transitions)

    file_str = cross_sections_utils.dot_in_fmt.format(
        run_name=run_name,
        state_name=state_name,
        naming_str=naming_str,
        n_bound_resultant=n_bound_resultant,
        n_scattering_resultant=n_scattering_resultant,
        target_A=t_A,
        target_Z=t_Z,
        target_gs_J2=t_gs_J2,
        target_gs_parity=t_gs_parity,
        target_gs_T2=t_gs_T2,
        n_bound_target=n_bound_target,
        targ_bound_str=targ_bound_str,
        proj_A=p_A,
        proj_Z=p_Z,
        proj_gs_J2=p_gs_J2,
        proj_gs_parity=p_gs_parity,
        proj_gs_T2=p_gs_T2,
        n_bound_proj=n_bound_proj,
        hw=hw,
        r_matching=r_matching,
        r_zero=r_zero,
        n_points=n_points,
        nsig_min=nsig_min,
        nsig_max=nsig_max,
        lamb_min=lamb_min,
        lamb_max=lamb_max,
        Rp=Rp,
        Rn=Rn,
        Rm=Rm,
        e_lines=e_lines,
        m_lines=m_lines,
        Emin=Emin,
        Emax=Emax,
        Estep=Estep,
        Eexpt=Eexpt
    )
    if out_dir is None:
        out_dir = os.path.dirname(observ_file)
    filename = os.path.join(out_dir, "transitions_NCSMC.in")
    with open(filename, "w+") as out_file:
        out_file.write(file_str)


if __name__ == "__main__":
    make_dot_in(proj, target_bound_states, run_name, state_name, naming_str,
                observ_file, transitions, shift_file, out_dir="")
