"""Quick script to plot cross section values from sigma_gamma_integ file"""

import matplotlib.pyplot as plt

sigma_gamma_integ = "/global/scratch/ccmccracken/npsm/cross_sections/nLi8_n3lo-NN3Nlnl-srg2.0_20_Nmax6_pheno_all_adjusted_3m/sigma_gamma_integ_nLi8_n3lo-NN3Nlnl-srg2.0_20_Nmax6_pheno_all_adjusted_3m_NCSMC_E1M1E2_Li9_2J_3.agr"
fig_name = "cross_section_3m.png"

with open(sigma_gamma_integ, "r+") as sig_file:
    lines = sig_file.readlines()

# ignore the first and last lines
lines = lines[1:-1]

energies = []
cross_sections = []
for line in lines:
    words = line.split()
    e = float(words[0])
    energies.append(e)
    c = float(words[2]) * 10000
    cross_sections.append(c)

plt.plot(energies, cross_sections)
plt.title("Cross-Section for The $^8Li(n, \\gamma) ^9Li$ Reaction, $6\\hbar \\Omega$")
plt.xlabel("Energy ($MeV$)")
plt.ylabel("Cross-Section ($\\mu b$)")
plt.yscale("log")
plt.xlim(0,1.1)
plt.xticks(ticks=[0.0,0.2,0.4,0.6,0.8,1.0])
plt.savefig(fig_name)
