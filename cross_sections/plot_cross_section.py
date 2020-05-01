"""Quick script to plot cross section values from sigma_gamma_integ file"""

import matplotlib.pyplot as plt

# list of sigma_gamma_integ files (maybe there is only one)
sigma_gamma_integ_list = [
    #"/Users/navratil/Projects/rgm_ncsm/NCSMC/Li8_n/nLi8_NNn3lo3Nlnl-srg2.0_20_Nmax9_2p1p_m8p6_pheno_upto1.4MeV_3m/sigma_gamma_integ_nLi8_NNn3lo3Nlnl-srg2.0_20_Nmax9_2p1p_m8p6_pheno_upto1.4MeV_3m_NCSMC_E1M1E2_Li9_3_3_r1.agr",
    #"/Users/navratil/Projects/rgm_ncsm/NCSMC/Li8_n/nLi8_NNn3lo3Nlnl-srg2.0_20_Nmax9_2p1p_m8p6_pheno_upto1.4MeV_1m/sigma_gamma_integ_nLi8_NNn3lo3Nlnl-srg2.0_20_Nmax9_2p1p_m8p6_pheno_upto1.4MeV_1m_NCSMC_E1M1E2_Li9_1_3.agr"
    "sigma_gamma_integ_nLi8_NNn3lo3Nlnl-srg2.0_20_Nmax9_2p1p_m8p6_pheno_upto1.4MeV_1m_NCSMC_E1M1E2_Li9_1_3.agr",
]

# name to use as output filename
# don't include an extension here, we'll save as a bunch of formats at the end
fig_name = "sigma_gamma_integ_nLi8_NNn3lo3Nlnl-srg2.0_20_Nmax9_2p1p_m8p6_pheno_upto1.4MeV_NCSMC_E1M1E2_Li9_tot"


# make cross_sections a dictionary, of the form 
# cross_sections[energy] = value
cross_sections = {}

for sigma_gamma_integ_file in sigma_gamma_integ_list:
    with open(sigma_gamma_integ_file, "r+") as sig_file:
        lines = sig_file.readlines()

    # ignore the first and last lines
    lines = lines[1:-1]

    for line in lines:
        words = line.split()
        # energy
        e = float(words[0])
        # cross-section
        c = float(words[2]) * 10000
        # if energy not in dict, add it
        if e not in cross_sections.keys():
            cross_sections[e] = c
        # otherwise, add e to the value already there
        else:
            cross_sections[e] += c

# then output the cross_section data to different formats:
ec_pairs = [[e, c] for e, c in sorted(cross_sections.items())]

# xmgrace
with open('summed_xsect.agr','w') as fileout:
    for pair in ec_pairs:
        e, c = pair
        line = f"{e} {c} \n"
        fileout.write(line)

# matplotlib, e = x axis, c = y axis
e, c = list(zip(*ec_pairs))
plt.plot(e, c)
plt.title("Cross-Section for The $^8Li(n, \\gamma) ^9Li$ Reaction, $8\\hbar \\Omega$")
plt.xlabel("Energy ($MeV$)")
plt.ylabel("Cross-Section ($\\mu b$)")
plt.yscale("log")
plt.xlim(0,1.1)
plt.xticks(ticks=[0.0,0.2,0.4,0.6,0.8,1.0])
for extension in [".pdf", ".svg", ".png"]:
    plt.savefig(fig_name+extension)
