"""
A module for making transitions_NCSMC.in files
"""

import file_tools
import utils
import shutil
import os
import re

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
    # Format: 2J, parity, 2T, binding energy. First entry = ground state.
    [4, 1, 2, -34.8845],
    [2, 1, 2, -33.7694]
]
"""bound states of the target nucleus."""

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
Rp = 2.1961
Rn = 2.3077
Rm = 2.2605

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
        ``[[J2, parity, T2, energy], ...]``

    lamb_max:
        integer, lambda = multipolarity of a transition. If we have some block
        of e transitions that looks like this::

            2 1 1 1.4850 2.4430 ! targ E mul i f  Mp Mn
            2 1 2 -0.7626 -1.5856 ! targ E mul i f  Mp Mn
            2 2 1 0.9845 2.0470 ! targ E mul i f  Mp Mn
            2 2 2 1.0374 0.8974 ! targ E mul i f  Mp Mn

        we're going to have a problem, since the code needs to read lines with
        all possible values from 1 to lamb_max as the first number.

    """
    e_transitions = {}
    m_transitions = []
    for state in target_bound_states:
        J2, parity, T2, energy = state
        pattern = re.compile(
            f".* {J2} {parity} {T2} # [0-9]* {energy}.*\n.*\n.*")
        matches = re.findall(pattern, simp_file_text)
        for match in matches:
            lines = match.split("\n")
            states_line, transition, data_line = lines
            multipolarity = int(transition[1:])
            e_or_m = transition[0]
            # find state #s, i.e. their indices in target_bound_states
            # the states look like this: 9 -- 6 1 2 # 2 -26.2739
            state_f, state_i = states_line.split("   ")
            f_words = state_f.split()
            J2_f = f_words[2]
            pi_f = f_words[3]
            T2_f = f_words[4]
            E_f = f_words[7]
            J2_f, pi_f, T2_f = int(J2_f), int(pi_f), int(T2_f)
            E_f = float(E_f)
            state_f = [J2_f, pi_f, T2_f, E_f]
            if state_f in target_bound_states:
                num_f = target_bound_states.index(state_f) + 1
            else:
                continue
            i_words = state_i.split()
            J2_i = i_words[2]
            pi_i = i_words[3]
            T2_i = i_words[4]
            E_i = i_words[7]
            J2_i, pi_i, T2_i = int(J2_i), int(pi_i), int(T2_i)
            E_i = float(E_i)
            state_i = [J2_i, pi_i, T2_i, E_i]
            if state_i in target_bound_states:
                num_i = target_bound_states.index(state_i) + 1
            else:
                continue
            var_list = parameter_list(transition)
            data_line_hunks = data_line.split()
            data = {}
            for var in var_list:
                for j, hunk in enumerate(data_line_hunks):
                    if var+"=" == hunk:
                        value = data_line_hunks[j+1]
                        data[var] = value
            if e_or_m == "E":
                t = (multipolarity, num_i, num_f)
                d = (data["E2p"], data["E2n"])
                if t not in e_transitions:
                    e_transitions[t] = d
            else:
                t = [num_i, num_f, data["pl"],
                     data["nl"], data["ps"], data["ns"]]
                if t not in m_transitions:
                    m_transitions.append(t)

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

    return new_e_trans, m_transitions


def get_bound_state_str(target_bound_states):
    """
    The .in file has a few lines dedicated to describing target bound states,
    this file makes those.

    target_bound_states:
        list of bound states, formatted like
        ``[[J2, parity, T2, energy], ...]``
    """
    bound_state_fmt = "{E}   {J2}  {parity}  {T2}     ! E, J, pi, T"
    targ_bound_str = ""
    for i, state in enumerate(target_bound_states):
        J2, p, T2, E = state
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
    J2 = round(float(gs_words[1]))
    T2 = round(float(gs_words[3]))
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
        return [1, 1, 1, 1, 1]
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
        elif all([utils.is_float(word) for word in words]):
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


def make_dot_in(proj, target_bound_states, run_name,
                state_name, naming_str, observ_file, transitions,
                shift_file, out_dir=None):
    """
    Makes a transitions_NCSMC.in file.

    proj:
        string, the projectile, e.g. "n"

    target_bound_states:
        list, info about bound states of the target.
        Formatted like ``[[J2, parity, T2, energy], ...]``

    run_name:
        string, name of directory where we'll put files

    state_name:
        string, state of resultant nucleus, in "2Jparity" format, e.g. "1m"

    naming_str:
        string, for naming stuff after the run is complete

    observ_file:
        string, path to the observ.out file for the target nucleus

    transitions:
        list of strings, transitions we'll consider, e.g. ["E2", "M1"]

    shift_file:
        string, path to a phase_shift or eigenphase_shift file

    out_dir:
        string, directory where we'll save the file

    """
    multipolarities = [int(t[1]) for t in transitions]
    lamb_min = min(multipolarities)
    lamb_max = max(multipolarities)


    # get info abount reactants, t = target, p = projectile
    t_A, t_Z, t_gs_J2, t_gs_parity, t_gs_T2 = get_target_info(observ_file)
    p_A, p_Z, p_gs_J2, p_gs_parity, p_gs_T2 = get_proj_info(proj)

    n_bound_target = len(target_bound_states)

    # in your ncsmc run, what were the min/max energy values and step size?
    Emin, Emax, Estep = get_energy_info(shift_file)

    # simplify observ file, get text
    shutil.copyfile(observ_file, os.path.split(observ_file)[1])
    simp = file_tools.simplify_observ("4 1 2", transitions, observ_file)
    with open(simp, "r+") as simp_file:
        text = simp_file.read()

    # get frequency from observ file
    hw = get_freq(observ_file)

    e_transitions, m_transitions = get_e_m_transitions(
        text, target_bound_states, lamb_max)
    targ_bound_str = get_bound_state_str(target_bound_states)
    e_lines, m_lines = get_transition_lines(e_transitions, m_transitions)

    file_str = utils.dot_in_fmt.format(
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
                observ_file, transitions, out_dir="")
