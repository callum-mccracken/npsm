"""A simple script to add sigma_gamma_integ files"""
files_to_add = [
    "/home/callum/Documents/Undergrad Work/npsm/input_files/sigma_gamma_integ_nLi8_n3lo-NN3Nlnl-srg2.0_20_Nmax8_pheno_3m_NCSMC_E1M1E2_Li9_3_3.agr",
    "/home/callum/Documents/Undergrad Work/npsm/input_files/sigma_gamma_integ_nLi8_n3lo-NN3Nlnl-srg2.0_20_Nmax8_pheno_1m_NCSMC_E1M1E2_Li9_1_3.agr"
]

resultant_name = "total.agr"
cross_sections_sum = {}

for f in files_to_add:
    with open(f, "r+") as sig_file:
        lines = sig_file.readlines()

    # ignore the first and last lines
    lines = lines[1:-1]

    for line in lines:
        words = line.split()
        # energy
        e = float(words[0])
        # cross-section
        c = float(words[2])
        # if energy not in dict, add it
        if e not in cross_sections_sum.keys():
            cross_sections_sum[e] = c
        # otherwise, add e to the value already there
        else:
            cross_sections_sum[e] += c

# output to file
output = "first line filler\n"
for e,c in sorted(cross_sections_sum.items()):
    output += f"{e} yeet {c}\n"
output += "last line filler\n"

with open(resultant_name, 'w+') as outfile:
    outfile.write(output)

print('saved total as', resultant_name)


