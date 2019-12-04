from os import symlink, remove, system, rename
from shutil import copyfile

# physics details
potential='NNn3lo3Nlnl-srg2.0'
iNuc='Li8'
Tz2=-2
Jz2=0
freq=20
N_gs=4
proj='n'

# suffixes for files
sufegv='_10st'
suffile='_2p1p'

# path (relative or full) to trdens_kernels[...].exe
trdens_kernel_exe = "../trdens_kernels_Oeff_devel.exe"
# which word should be used to run the exe file? srun? mpirun?
run_word = "srun"

Nmax_list = [4]

def run_rgm():
    for Nmax in Nmax_list:
        
        N = Nmax + N_gs  # total number of excitations

        # why do we make this link now? It never gets used... as far as I can tell?
        eig_file = "mfdp_"+N+".egv_"+iNuc+"_"+potential+"_Nmax"+Nmax+"."+freq+sufegv
        link = eig_file+"_"+Jz2+"_"+Tz2
        symlink(eig_file, link)
        
        # it's unclear what these loops do
        for Jzi in [0, 1, -1, 2, -2]:
            Jzi2= 2*Jzi
            # get nki
            if Jzi == 0:
                nki = 2
            elif Jzi == 1 or Jzi == -1:
                nki = 2
            else:
                nki = 1

            for Jzf in [0, 1, -1, 2, -2]:
                Jzf2 = 2 * Jzf
                # get nkf
                if Jzf == 0:
                    nkf = 2
                elif Jzf == 1 or Jzf == -1:
                    nkf=2
                else:
                    nkf = 1

                # now in a second, we'll try to run the trdens_kernels code.
                # first, some setup.

                # trdens input file must have the trdens.in name for exe to run.
                copyfile("trdens.in_"+Nmax+"_"+nkf+"_"+nki, "trdens.in")

                # after running the exe, we'll rename our files
                # so they match up with the eigenvector file we used,
                # whose name includes this text
                common_text = iNuc+"_"+potential+"_Nmax"+Nmax+"."+freq
                
                # initial and final eigenvector file names (Jzi2 vs Jzf2)
                eig_i = "mfdp_"+N+".egv_"+common_text+sufegv+"_"+Jzi2+"_"+Tz2
                eig_f = "mfdp_"+N+".egv_"+common_text+sufegv+"_"+Jzf2+"_"+Tz2

                # 2 different ways to run the code, depending on whether Jzi=Jzf
                if Jzi == Jzf:
                    # link to eigenvector file, with a name the exe can read
                    symlink(eig_i, "mfdp.egv")
                    
                    # run exe file, redirect output to output_file
                    output_file = "t.o_"+proj+common_text+suffile+"_"+Jzi2
                    system(run_word+" "+trdens_kernel_exe+" > "+output_file)

                    # new names for output files
                    new_trdens_out = "trdens.out_"+proj+common_text+suffile+"_Jz"+Jzi
                    new_rgm = "RGM_kernels.dat_"+proj+common_text+suffile+"_Jz"+Jzi
                    new_rgm_terms = "RGM_kernel_terms.dat_"+proj+common_text+suffile+"_Jz"+Jzi

                    # rename files
                    rename("trdens.out", new_trdens_out)
                    rename("RGM_kernels.dat", new_rgm)
                    rename("RGM_kernel_terms.dat", new_rgm_terms)

                    # remove link to eigenvector file
                    remove("mfdp.egv")
                else:
                    # links to eigenvector files, with names the exe can read
                    symlink(eig_i, "mfdi.egv")
                    symlink(eig_f, "mfdf.egv")

                    # run exe file, redirect output to output_file
                    output_file = "t.o_"+proj+common_text+suffile+"_"+Jzf2+"_"+Jzi2
                    system(run_word+" "+trdens_kernel_exe+" > "+output_file)
                    
                    # new names for output files
                    new_trdens_out = "trdens.out_"+proj+common_text+suffile+"_Jz"+Jzf+"_Jz"+Jzi
                    new_rgm = "RGM_kernels.dat_"+proj+common_text+suffile+"_Jz"+Jzf+"_Jz"+Jzi
                    new_rgm_terms = "RGM_kernel_terms.dat_"+proj+common_text+suffile+"_Jz"+Jzf+"_Jz"+Jzi

                    # rename files
                    rename("trdens.out", new_trdens_out)
                    rename("RGM_kernels.dat", new_rgm)
                    rename("RGM_kernel_terms.dat", new_rgm_terms)

                    # remove links to eigenvector files
                    remove("mfdi.egv")
                    remove("mfdf.egv")

if __name__ == "__main__":
    run_rgm()
