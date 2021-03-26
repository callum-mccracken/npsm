"""
Useful things that didn't really fit anywhere.
"""
import os
import sys
sys.path.append(os.path.realpath(".."))
from ncsmc_python.output_simplifier import simplify
import re

ptable = {
    "n": 0,
    "H": 1,
    "He": 2,
    "Li": 3,
    "Be": 4,
    "B": 5,
    "C": 6,
    "N": 7,
    "O": 8,
    "F": 9,
    "Ne": 10,
    "Na": 11,
    "Mg": 12,
    "Al": 13,
    "Si": 14,
    "P": 15,
    "S": 16,
    "Cl": 17,
    "Ar": 18,
    "K": 19,
    "Ca": 20,
    "Sc": 21,
    "Ti": 22,
    "V": 23,
    "Cr": 24,
    "Mn": 25,
    "Fe": 26,
    "Co": 27,
    "Ni": 28,
    "Cu": 29,
    "Zn": 30,
    "Ga": 31,
    "Ge": 32,
    "As": 33,
    "Se": 34,
    "Br": 35,
    "Kr": 36,
    "Rb": 37,
    "Sr": 38,
    "Y": 39,
    "Zr": 40,
    "Nb": 41,
    "Mo": 42,
    "Tc": 43,
    "Ru": 44,
    "Rh": 45,
    "Pd": 46,
    "Ag": 47,
    "Cd": 48,
    "In": 49,
    "Sn": 50,
    "Sb": 51,
    "Te": 52,
    "I": 53,
    "Xe": 54,
    "Cs": 55,
    "Ba": 56,
    "La": 57,
    "Ce": 58,
    "Pr": 59,
    "Nd": 60,
    "Pm": 61,
    "Sm": 62,
    "Eu": 63,
    "Gd": 64,
    "Tb": 65,
    "Dy": 66,
    "Ho": 67,
    "Er": 68,
    "Tm": 69,
    "Yb": 70,
    "Lu": 71,
    "Hf": 72,
    "Ta": 73,
    "W": 74,
    "Re": 75,
    "Os": 76,
    "Ir": 77,
    "Pt": 78,
    "Au": 79,
    "Hg": 80,
    "Tl": 81,
    "Pb": 82,
    "Bi": 83,
    "Po": 84,
    "At": 85,
    "Rn": 86,
    "Fr": 87,
    "Ra": 88,
    "Ac": 89,
    "Th": 90,
    "Pa": 91,
    "U": 92,
    "Np": 93,
    "Pu": 94,
    "Am": 95,
    "Cm": 96,
    "Bk": 97,
    "Cf": 98,
    "Es": 99,
    "Fm": 100,
    "Md": 101,
    "No": 102,
    "Lr": 103,
    "Rf": 104,
    "Db": 105,
    "Sg": 106,
    "Bh": 107,
    "Hs": 108,
    "Mt": 109,
    "Ds": 110,
    "Rg": 111,
    "Cn": 112,
    "Nh": 113,
    "Fl": 114,
    "Mc": 115,
    "Lv": 116,
    "Ts": 117,
    "Og": 118
}
"""The periodic table, well just the Z values"""


def is_float(string):
    """
    Check if a string can be cast to a float

    string:
        a string *shocking, I know*
    """
    try:
        _ = float(string)
        return True
    except ValueError:
        return False


def get_state_name(state):
    """
    if state = e.g., "3 -1 3"
    this will return the corresponding state_name,
    e.g., state_name = "3m"

    state:
        string, of the form "3 -1 3"
    """
    J2, pi, _ = map(int, state.split())
    pi_str = "p" if pi > 0 else "m"
    state_name = str(J2)+pi_str
    return state_name


def get_A_Z(name):
    """
    Get A and Z for a given atomic name

    name:
        string, of the form "Li8"
    """

    # first assume the name only has 1 letter like H2
    n_chars = 1
    while not is_float(name[n_chars:]):
        n_chars += 1
    A = float(name[n_chars:])
    Z = ptable[name[:n_chars]]
    return A, Z


def get_resultant_state_info(rgm_out_filename, verbose=False):
    _, state_titles = simplify(rgm_out_filename, verbose=verbose)
    for i, title in enumerate(state_titles):
        J, p, T = title.split("_")
        J2 = str(int(float(J) * 2))
        T2 = str(int(float(T) * 2))
        state_titles[i] = " ".join([J2, p, T2])
        print(J2,J,T2)
    return state_titles

##Chloe Modif
def get_proj_state_info(rgm_out_filename):
    with open(rgm_out_filename, "r+") as rgm_out_file:
        text = rgm_out_file.read()
    # I assume all hunks of relevant info look something like this:
    # chann,2*J,2*T,parity=

    regex = r'number of channels=[ ]*([0-9]*)'
    match = re.findall(regex, text)
    Nchan=match[0]
    regex = r'chann,2\SJ,2\ST,parity=[ ]*([0-9]*)[ ]*([0-9]*)[ ]*([0-9]*)[ ]*(-?[0-9]*)'    
    matches = re.findall(regex, text)
    regex=r'state \#[ ]([0-9])*[ ]*energy=[ ]*(-?[.0-9]*).*'
    matchstates = re.findall(regex, text)
    Nst=0
    ii=0
    for matchst in matchstates:
        ist=int(float(matchst[0]))
        if ist > Nst :
            Nst=int(float(matchst[0]))
        ii=ii+1
        
    states=[]
    iimin=0
    iimax=Nst    
    for match in matches:
        ichan=int(float(match[0]))
        J2 = int(float(match[1]))
        T2 = int(float(match[2]))
        parity = int(float(match[3]))
        for matchst in matchstates[iimin:iimax]: 
            ist=int(float(matchst[0]))
            energy=float(matchst[1])   
            states.append([ichan,ist,J2,parity,T2,energy])    
        iimin=iimin+Nst
        iimax=iimax+Nst
    return states

def get_target_state_info(rgm_out_filename):
    with open(rgm_out_filename, "r+") as rgm_out_file:
        text = rgm_out_file.read()
    # first get parity
    parity_matches = re.findall(r'parity= [+-]', text)
    # the first parity value in the file should be from the target info up top
    target_parity = parity_matches[0].split()[1]
    if target_parity == "+":
        parity = 1
    elif target_parity == "-":
        parity = -1
    else:
        raise ValueError("Parity value " + target_parity + " not understood")
    # I assume all hunks of relevant info look something like this:
    # J=  4    T=  2    Energy= -34.8845
    regex = r'J=[ ]*([.0-9]*)[ ]*T=[ ]*([.0-9]*)[ ]*Energy=[ ]*-?([.0-9]*).*'
    matches = re.findall(regex, text)
    states = []
    # keep a record of how many times a state with [J2, pi, T2] is entered
    nums = {}
    for match in matches:
        words = match
        J2 = int(2.*float(words[0]))
        T2 = int(2.*float(words[1]))
        energy = float(words[2])
        num_string = f"{J2} {parity} {T2}"
        if num_string not in nums.keys():
            nums[num_string] = 1
        else:
            nums[num_string] += 1
        states.append([J2, parity, T2, nums[num_string], energy])
    #for state in states:
    #    print(state)

    # Format: 2J, parity, 2T, num, binding energy. First entry = ground state.
    # I'm pretty sure that the first state will always be the ground state,
    # but if that's not the case, you should add some code here to rearrange
    # the list!
    return states


dot_in_fmt_1 = """{run_name}
{state_name}
{naming_str}
{n_bound_resultant} ! Number of bound states for composite nucleus
{n_scattering_resultant} ! Number of scattering states for composite nucleus
{target_A} {target_Z} {target_gs_J2} {target_gs_parity} {target_gs_T2} {n_bound_target} ! Target info: A, Z, ground state 2J, parity, 2T
{targ_bound_str}
{proj_A} {proj_Z} {proj_gs_J2} {proj_gs_parity} {proj_gs_T2} {n_bound_proj} ! Projectile info: A, Z, ground state 2J, parity, 2T
{target_A} {target_Z} {target_gs_J2} {target_gs_parity} {target_gs_T2} {n_bound_target} ! Target info: A, Z, ground state 2J, parity, 2T
{targ_bound_str}
{proj_A} {proj_Z} {proj_gs_J2} {proj_gs_parity} {proj_gs_T2} {n_bound_proj} ! Projectile info: A, Z, ground state 2J, parity, 2T
{hw} ! Frequency used in NCSM calculation
{r_matching} ! Matching radius
{r_zero} ! Cutoff radius, after which wavefunction ~0
{n_points} ! Number of points to use for integration
{nsig_min} {nsig_max} {lamb_min} {lamb_max} ! nsig_min,nsig_max,lamb_min,lamb_max

{Rp} {Rn} {Rm} ! targ Rp, Rn, Rm

{e_lines}
{m_lines}
{Emin} {Emax} {Estep} ! Emin, Emax, dE
{Eexpt} ! Eexpt
"""

dot_in_fmt_2 = """{run_name}
{state_name}
{naming_str}
{n_bound_resultant} ! Number of bound states for composite nucleus
{n_scattering_resultant} ! Number of scattering states for composite nucleus
{target_A} {target_Z} {target_gs_J2} {target_gs_parity} {target_gs_T2} {n_bound_target} ! Target info: A, Z, ground state 2J, parity, 2T
{proj_A} {proj_Z} {proj_gs_J2} {proj_gs_parity} {proj_gs_T2} {n_bound_proj} ! Projectile info: A, Z, ground state 2J, parity, 2T
{target_A} {target_Z} {target_gs_J2} {target_gs_parity} {target_gs_T2} {n_bound_target} ! Target info: A, Z, ground state 2J, parity, 2T
{proj_A} {proj_Z} {proj_gs_J2} {proj_gs_parity} {proj_gs_T2} {n_bound_proj} ! Projectile info: A, Z, ground state 2J, parity, 2T
{hw} ! Frequency used in NCSM calculation
{r_matching} ! Matching radius
{r_zero} ! Cutoff radius, after which wavefunction ~0
{n_points} ! Number of points to use for integration
{nsig_min} {nsig_max} {lamb_min} {lamb_max} ! nsig_min,nsig_max,lamb_min,lamb_max

{Rp} {Rn} {Rm} ! targ Rp, Rn, Rm

{e_lines}
{m_lines}
{Emin} {Emax} {Estep} ! Emin, Emax, dE
{Eexpt} ! Eexpt
"""

dot_in_fmt_3 = """{run_name}
{state_name}
{naming_str}
{n_bound_resultant} ! Number of bound states for composite nucleus
{n_scattering_resultant} ! Number of scattering states for composite nucleus
{target_A} {target_Z} {target_gs_J2} {target_gs_parity} {target_gs_T2} {n_bound_target} ! Target info: A, Z, ground state 2J, parity, 2T
{targ_bound_str}
{proj_A} {proj_Z} {proj_gs_J2} {proj_gs_parity} {proj_gs_T2} {n_bound_proj} ! Projectile info: A, Z, ground state 2J, parity, 2T
{proj_bound_str}
{target_A} {target_Z} {target_gs_J2} {target_gs_parity} {target_gs_T2} {n_bound_target} ! Target info: A, Z, ground state 2J, parity, 2T
{targ_bound_str}
{proj_A} {proj_Z} {proj_gs_J2} {proj_gs_parity} {proj_gs_T2} {n_bound_proj} ! Projectile info: A, Z, ground state 2J, parity, 2T
{proj_bound_str}
{hw} ! Frequency used in NCSM calculation
{r_matching} ! Matching radius
{r_zero} ! Cutoff radius, after which wavefunction ~0
{n_points} ! Number of points to use for integration
{nsig_min} {nsig_max} {lamb_min} {lamb_max} ! nsig_min,nsig_max,lamb_min,lamb_max

{Rptarg} {Rntarg} {Rmtarg} ! targ Rp, Rn, Rm

{e_lines_targ}
{m_lines_targ}
{Rpproj} {Rnproj} {Rmproj} ! proj Rp, Rn, Rm

{e_lines_proj}
{m_lines_proj}
{Emin} {Emax} {Estep} ! Emin, Emax, dE
{Eexpt} ! Eexpt
"""

dot_in_fmt_4 = """{run_name}
{state_name}
{naming_str}
{n_bound_resultant} ! Number of bound states for composite nucleus
{n_scattering_resultant} ! Number of scattering states for composite nucleus
{target_A} {target_Z} {target_gs_J2} {target_gs_parity} {target_gs_T2} {n_bound_target} ! Target info: A, Z, ground state 2J, parity, 2T
{proj_A} {proj_Z} {proj_gs_J2} {proj_gs_parity} {proj_gs_T2} {n_bound_proj} ! Projectile info: A, Z, ground state 2J, parity, 2T
{proj_bound_str}
{target_A} {target_Z} {target_gs_J2} {target_gs_parity} {target_gs_T2} {n_bound_target} ! Target info: A, Z, ground state 2J, parity, 2T
{proj_A} {proj_Z} {proj_gs_J2} {proj_gs_parity} {proj_gs_T2} {n_bound_proj} ! Projectile info: A, Z, ground state 2J, parity, 2T
{proj_bound_str}
{hw} ! Frequency used in NCSM calculation
{r_matching} ! Matching radius
{r_zero} ! Cutoff radius, after which wavefunction ~0
{n_points} ! Number of points to use for integration
{nsig_min} {nsig_max} {lamb_min} {lamb_max} ! nsig_min,nsig_max,lamb_min,lamb_max

{Rptarg} {Rntarg} {Rmtarg} ! targ Rp, Rn, Rm

{e_lines_targ}
{m_lines_targ}
{Rpproj} {Rnproj} {Rmproj} ! proj Rp, Rn, Rm

{e_lines_proj}
{m_lines_proj}
{Emin} {Emax} {Estep} ! Emin, Emax, dE
{Eexpt} ! Eexpt
"""


dot_in_fmt_5 = """{run_name}
{state_name}
{naming_str}
{n_bound_resultant} ! Number of bound states for composite nucleus
{n_scattering_resultant} ! Number of scattering states for composite nucleus
{target_A} {target_Z} {target_gs_J2} {target_gs_parity} {target_gs_T2} {n_bound_target} ! Target info: A, Z, ground state 2J, parity, 2T
{proj_A} {proj_Z} {proj_gs_J2} {proj_gs_parity} {proj_gs_T2} {n_bound_proj} ! Projectile info: A, Z, ground state 2J, parity, 2T
{target_A} {target_Z} {target_gs_J2} {target_gs_parity} {target_gs_T2} {n_bound_target} ! Target info: A, Z, ground state 2J, parity, 2T
{proj_A} {proj_Z} {proj_gs_J2} {proj_gs_parity} {proj_gs_T2} {n_bound_proj} ! Projectile info: A, Z, ground state 2J, parity, 2T
{hw} ! Frequency used in NCSM calculation
{r_matching} ! Matching radius
{r_zero} ! Cutoff radius, after which wavefunction ~0
{n_points} ! Number of points to use for integration
{nsig_min} {nsig_max} {lamb_min} {lamb_max} ! nsig_min,nsig_max,lamb_min,lamb_max

{Rptarg} {Rntarg} {Rmtarg} ! targ Rp, Rn, Rm

{e_lines_targ}
{m_lines_targ}
{Rpproj} {Rnproj} {Rmproj} ! proj Rp, Rn, Rm

{e_lines_proj}
{m_lines_proj}
{Emin} {Emax} {Estep} ! Emin, Emax, dE
{Eexpt} ! Eexpt
"""
"""The format of the transitions_NCSMC.in file"""
