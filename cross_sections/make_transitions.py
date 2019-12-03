import process_observ
import utils
import shutil
import os
import re
# note that gs = ground state in a bunch of places

target = "Li8"
projectile = "n"

run_name = "nLi8_n3lo-NN3Nlnl-srg2.0_20_Nmax6"
state_name = "3m"
naming = "NCSMC_E1M1E2_Li9_2J_3"
Nhw = 20.0
r_matching = 18.0
r_zero = 50.0
n_points = 10000

# in your ncsmc run, what were the min/max energy values and step size?
Emin = 0.02
Emax = 10.0
Estep = 0.02
Eexpt = 0.0  # TODO: experimental energy? What is this?

# info about target and projectile
n_targets = 1  # TODO: what do I do if these are not both one?
target_A = 8
target_Z = 3
target_gs_J2 = 4
target_gs_parity = 1
target_gs_T2 = 2

n_projectiles = 1
proj_A = 1
proj_Z = 0
proj_gs_J2 = 1
proj_gs_parity = 1
proj_gs_T2 = 1

# info about bound states, so we can find them in the observ.out file.
# TODO: could we get these automatically?
target_bound_states = [
    # Format: 2J, parity, 2T, binding energy. First entry = ground state.
    [target_gs_J2, target_gs_parity, target_gs_T2, -34.8845],
    [2, 1, 2, -33.7694]
]
n_bound_target = len(target_bound_states)

# is it safe to assume that the projectile only has 1 bound state?
n_bound_proj = 1


# the observ.out file for the target
observ_file = "/Users/callum/Desktop/npsm/_Nmax6_ncsmc_output/Li8_observ_Nmax6_Jz1"
transitions = ["E2", "M1"]
simp = process_observ.simplify("4 1 2", transitions, observ_file)
with open(simp, "r+") as simp_file:
    text = simp_file.read()

def parameter_list(transition):
    """
    Returns the parameters we should take from the observ.out file,
    for each type of transition.
    """
    param_dict = {
        "E2": ["E2p", "E2n"],
        "M1": ["pl", "nl", "ps", "ns"]
    }
    return param_dict[transition]

def get_e_m_transitions():
    e_transitions = []
    m_transitions = []
    for i, state in enumerate(target_bound_states):
        J2, parity, T2, energy = state
        pattern = re.compile(f".* {J2} {parity} {T2} # [0-9]* {energy}.*\n.*\n.*")
        matches = re.findall(pattern, text)
        for match in matches:
            lines = match.split("\n")
            states_line, transition, data_line = lines
            multipolarity = int(transition[1:])
            e_or_m = transition[0]
            # find state #s, i.e. their indices in target_bound_states
            # the states look like this: 9 -- 6 1 2 # 2 -26.2739
            state_f, state_i = states_line.split("   ")
            f_words = state_f.split()
            J2_f, pi_f, T2_f, E_f = f_words[2], f_words[3], f_words[4], f_words[7]
            J2_f, pi_f, T2_f = int(J2_f), int(pi_f), int(T2_f)
            E_f = float(E_f)
            state_f = [J2_f, pi_f, T2_f, E_f]
            if state_f in target_bound_states:
                num_f = target_bound_states.index(state_f) + 1
            else:
                continue
            i_words = state_i.split()
            J2_i, pi_i, T2_i, E_i = i_words[2], i_words[3], i_words[4], i_words[7]
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
                t = [multipolarity, num_i, num_f, data["E2p"], data["E2n"]]
                if t not in e_transitions:
                    e_transitions.append(t)
            else:
                t = [num_i, num_f, data["pl"], data["nl"], data["ps"], data["ns"]]
                if t not in m_transitions:
                    m_transitions.append(t)
    return e_transitions, m_transitions
e_transitions, m_transitions = get_e_m_transitions()

def get_bound_state_str(target_bound_states):
    bound_state_fmt = "{E}   {J2}  {parity}  {T2}     ! E, J, pi, T"
    targ_bound_str = ""
    for i, state in enumerate(target_bound_states):
        J2, p, T2, E = state
        targ_bound_str += bound_state_fmt.format(E=E, J2=J2, parity=p, T2=T2)
        if i+1 != len(target_bound_states):
            targ_bound_str += "\n"
    return targ_bound_str
targ_bound_str = get_bound_state_str(target_bound_states)

def get_transition_lines(e_transitions, m_transitions):
    e_fmt = "{multipolarity} {i} {f} {Mp} {Mn} ! targ E mul i f  Mp Mn\n"
    e_lines = ""
    for m, i, f, Mp, Mn in e_transitions:
        e_lines += e_fmt.format(multipolarity=m, i=i, f=f, Mp=Mp, Mn=Mn)
    m_fmt = "  {i} {f} {Mlp} {Mln} {Msp} {Msn} ! targ M1 i f Mlp Mln Msp Msn\n"
    m_lines = ""
    for i, f, Mlp, Mln, Msp, Msn in m_transitions:
        m_lines += m_fmt.format(i=i, f=f, Mlp=Mlp, Mln=Mln, Msp=Msp, Msn=Msn)
    return e_lines, m_lines
e_lines, m_lines = get_transition_lines(e_transitions, m_transitions)


file_str = f"""{run_name} ! Naming convention used in input files
{state_name} ! State of reaction product
{naming} ! Something to use to rename your output
{n_targets} ! Number of target nuclei
{n_projectiles} ! Number of projectiles
{target_A} {target_Z} {target_gs_J2} {target_gs_parity} {target_gs_T2} {n_bound_target} ! Target info
{targ_bound_str}
{proj_A} {proj_Z} {proj_gs_J2} {proj_gs_parity} {proj_gs_T2} {n_bound_proj} ! Projectile info
{target_A} {target_Z} {target_gs_J2} {target_gs_parity} {target_gs_T2} {n_bound_target} ! Target info
{targ_bound_str}
{proj_A} {proj_Z} {proj_gs_J2} {proj_gs_parity} {proj_gs_T2} {n_bound_proj} ! Projectile info
{Nhw} ! Frequency used in NCSM calculation
{r_matching} ! Matching radius
{r_zero} ! Cutoff radius, after which wavefunction ~0
{n_points} ! Number of points to use for integration
0 1 1 2 ! nsig_min,nsig_max,lamb_min,lamb_max

2.1961 2.3077 2.2605 ! targ Rp, Rn, Rm

{e_lines}
{m_lines}
{Emin} {Emax} {Estep} ! Emin, Emax, dE
{Eexpt} ! Eexpt
"""

with open("transitions_NCSMC_"+state_name+".in", "w+") as out_file:
    out_file.write(file_str)
