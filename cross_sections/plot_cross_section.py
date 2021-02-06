"""Quick script to plot cross section values from sigma_gamma_integ file"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.font_manager
from matplotlib.ticker import MultipleLocator
mpl.rcParams['lines.linewidth'] = '2'
mpl.rcParams['axes.linewidth'] = '2'
mpl.rcParams['lines.dashed_pattern'] = (7, 2)
mpl.rcParams['lines.dotted_pattern'] = (1, 1.65)
plt.rcParams["font.family"] = "Times New Roman"
plt.rcParams["font.weight"] = "bold"
plt.rc('text', usetex=True)
plt.rc('font', size=16)


# list of sigma_gamma_integ files (maybe there is only one)
sigma_gamma_integ_file_list = [
    'total.agr',
    "/home/callum/Documents/Undergrad Work/npsm/input_files/sigma_gamma_integ_nLi8_n3lo-NN3Nlnl-srg2.0_20_Nmax8_pheno_3m_NCSMC_E1M1E2_Li9_3_3.agr",
    "/home/callum/Documents/Undergrad Work/npsm/input_files/sigma_gamma_integ_nLi8_n3lo-NN3Nlnl-srg2.0_20_Nmax8_pheno_1m_NCSMC_E1M1E2_Li9_1_3.agr"
]

# titles for each file
title_list = [
    "Total$,$ N$_{\\mathrm{max}}=8$",
    "$3/2^-,$ N$_{\\mathrm{max}}=8$",
    "$1/2^-,$ N$_{\\mathrm{max}}=8$",
]

styles = [
    "r-",
    "b--",
    "g--"
]


# name to use as output filename
# don't include an extension here, we'll save as a bunch of formats at the end
fig_name = "sigma_gamma_integ_nLi8_NNn3lo3Nlnl-srg2.0_20_Nmax9_2p1p_m8p6_pheno_upto2MeV_NCSMC_E1M1E2_Li9"

# make cross_sections a dictionary, of the form 
# cross_sections[title][energy] = value, for each file
cross_sections = {}

for sgi_file, title in zip(sigma_gamma_integ_file_list, title_list):
    cross_sections[title] = {}

    # read lines
    with open(sgi_file, "r+") as sig_file:
        lines = sig_file.readlines()

    # ignore the first and last lines
    lines = lines[1:-1]

    for line in lines:
        words = line.split()
        # energy
        e = float(words[0])
        # cross-section * 10000 to convert units
        c = float(words[2]) * 10000
        # if energy not in dict, add it
        if e not in cross_sections[title].keys():
            cross_sections[title][e] = c
        # otherwise, add e to the value already there
        else:
            cross_sections[title][e] += c

    # then output the cross_section data to different formats:
    ec_pairs = [[e, c] for e, c in sorted(cross_sections[title].items())]

# use matplotlib for main plot, e = x axis, c = y axis
fix, ax = plt.subplots()

# plot each line
for title, style in zip(title_list, styles):
    ec_pairs = [[e, c] for e, c in sorted(cross_sections[title].items())]
    e, c = list(zip(*ec_pairs))
    plt.plot(e, c, style, label=title)

# plot experimental data
# points
plt.scatter([0.25, 0.75], [19.1, 7.9], c='k', s=50)
# error bars
plt.annotate("", xy=(0.25, 8), xytext=(0.25, 19.1 + 10.4),
             arrowprops=dict(arrowstyle="-|>", lw=2, color='k'))
plt.plot([0.25 - 0.03, 0.25 + 0.03], [19.1 + 10.4, 19.1 + 10.4], 'k')

plt.annotate("", xy=(0.75, 2.3), xytext=(0.75, 7.9 + 5.5),
             arrowprops=dict(arrowstyle="-|>", lw=2, color='k'))
plt.plot([0.75 - 0.03, 0.75 + 0.03], [7.9 + 5.5, 7.9 + 5.5], 'k')




#plt.title("Cross-Section for The $^8Li(n, \\gamma) ^9Li$ Reaction, $8\\hbar \\Omega$")
plt.xlabel("$E_{\\mathrm{kin}}$ [MeV]", fontsize=20, fontname='Times New Roman')
plt.ylabel("$\\sigma$ [$\\mu$b]", fontsize=20)
plt.yscale("log")
plt.xlim(0,1.3)
plt.ylim(0.27,220)
plt.xticks(ticks=[0.0,0.2,0.4,0.6,0.8,1.0,1.2],
labels = ["$0.0$","$0.2$","$0.4$","$0.6$","$0.8$","$1.0$","$1.2$"])
ax.xaxis.set_minor_locator(MultipleLocator(0.1))
plt.yticks(ticks=[1,10,100], labels=["$1$","$10$","$100$"])
ax.tick_params(axis="x", which='both', top=True, bottom=True)
ax.tick_params(axis="y", which='both', left=True, right=True)
ax.tick_params(which='both', direction='in', length=6, width=2)
ax.tick_params(which='minor', width=1.5)
ax.legend()
plt.tight_layout()
for extension in [".pdf", ".svg", ".png"]:
    plt.savefig(fig_name+extension, dpi=300)
