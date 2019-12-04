from os import symlink, remove, system, rename
from shutil import copyfile

potential='NNn3lo3Nlnl-srg2.0'
nuc='Li8'
Ngs=4
Tz2=-2
freq=20
Nmax=4
proj='n'

sufegv='_10st'
suffile='_2p1p_10m'

nucA='Li9'
Nmaxi=4

Jz2=0

N = Nmax + Ngs


# path (relative or full) to exe file
exe_path = "../trdens_kernels_Oeff_devel.exe"
# which word should be used to run the exe file? srun? mpirun?
run_word = "srun"

# make link to eigenvector file
real_eig = f"mfdp_{N}.egv_{nuc}_{potential}_Nmax{Nmax}.{freq}{sufegv}"
eig_link = f"{real_eig}_{Jz2}_{Tz2}"
symlink(real_eig, eig_link)

Jzf_list = [0, 1, -1, 2, -2]

def run_coupling():
    for Jzf in Jzf_list:
        Jzf2 = 2 * Jzf

        if Jzf == 0:
            nkf=2
        elif Jzf == 1 or Jzf == -1:
            nkf=2
        else:
            nkf=1

        copyfile("trdens.in_"+Nmax+"_"+nkf, "trdens.in")
        
        real_eig_f = real_eig+"_"+Jzf2+"_"+Tz2
        
        symlink(real_eig_f, "mfdf.egv")
        
        output_file = "t.o_"+nucA+"_"+nuc+"_"+potential+"_Nmax"+Nmaxi+"_Nmax"+Nmax+"."+freq+""+suffile+"_"+Jzf2

        system(run_word+" "+exe_path+" > "+output_file)
        
        rename("trdens.out", "trdens.out_"+nucA+"_"+nuc+"_"+potential+"_Nmax"+Nmaxi+"_Nmax"+Nmax+"."+freq+""+suffile+"_Jz"+Jzf)
        rename("NCSMC_kernels.dat", "NCSMC_kernels.dat_"+nucA+"_"+nuc+"_"+potential+"_Nmax"+Nmaxi+"_Nmax"+Nmax+"."+freq+""+suffile+"_Jz"+Jzf)
        remove("mfdf.egv")

if __name__ == "__main__":
    run_coupling()
