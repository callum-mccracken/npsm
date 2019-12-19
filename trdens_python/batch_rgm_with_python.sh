#!/bin/bash
#SBATCH --account=rrg-navratil
#SBATCH --ntasks=1024            # number of MPI processes
#SBATCH --mem-per-cpu=4096M      # memory; default unit is megabytes
#SBATCH --time=0-02:00           # time (DD-HH:MM)
#SBATCH --output=trdens-%J.out

cd /scratch/navratil/Li9

potential='NNn3lo3Nlnl-srg2.0'
iNuc='Li8'
Tz2=-2
Jz2=0
freq=20
N_gs=4
proj='n'

sufegv='_10st'
suffile='_2p1p'

# make a trdens.in file with some initial values for nki and nkf
# it doesn't matter what the values are (they must be integers though)
# since they'll be overwritten.


for Nmax in 4

do

    N=$[$Nmax+$N_gs]

    ln -sf mfdp_${N}.egv_${iNuc}_${potential}_Nmax${Nmax}.${freq}${sufegv}  mfdp_${N}.egv_${iNuc}_${potential}_Nmax${Nmax}.${freq}${sufegv}_${Jz2}_${Tz2}
    
    for Jzi in 0 1 -1 2 -2

    do

    Jzi2=$[$Jzi+$Jzi]

    if [ $Jzi -eq 0 ] 
    then
        nki=2
    elif [ $Jzi -eq 1 ] || [ $Jzi -eq -1 ] 
    then
        nki=2
    else
        nki=1
    fi

    for Jzf in 0 1 -1 2 -2

    do

        Jzf2=$[$Jzf+$Jzf]

        if [ $Jzf -eq 0 ]
        then
        nkf=2
        elif [ $Jzf -eq 1 ] || [ $Jzf -eq -1 ] 
        then
        nkf=2
        else
        nkf=1
        fi

        python edit_dot_in.py -o trdens.in -n trdens.in -i ${nki} -f ${nkf}

        if [ $Jzi -eq $Jzf ]
        then
        ln -sf mfdp_${N}.egv_${iNuc}_${potential}_Nmax${Nmax}.${freq}${sufegv}_${Jzi2}_${Tz2} mfdp.egv

        srun  ../trdens_kernels_Oeff_devel.exe > t.o_${proj}${iNuc}_${potential}_Nmax${Nmax}.${freq}${suffile}_${Jzi2}

        mv trdens.out trdens.out_${proj}${iNuc}_${potential}_Nmax${Nmax}.${freq}${suffile}_Jz${Jzi}
        mv RGM_kernels.dat RGM_kernels.dat_${proj}${iNuc}_${potential}_Nmax${Nmax}.${freq}${suffile}_Jz${Jzi}
        mv RGM_kernel_terms.dat RGM_kernel_terms.dat_${proj}${iNuc}_${potential}_Nmax${Nmax}.${freq}${suffile}_Jz${Jzi}
        rm -f mfdp.egv
        else
        ln -sf mfdp_${N}.egv_${iNuc}_${potential}_Nmax${Nmax}.${freq}${sufegv}_${Jzi2}_${Tz2} mfdi.egv
        ln -sf mfdp_${N}.egv_${iNuc}_${potential}_Nmax${Nmax}.${freq}${sufegv}_${Jzf2}_${Tz2} mfdf.egv

        srun  ../trdens_kernels_Oeff_devel.exe > t.o_${proj}${iNuc}_${potential}_Nmax${Nmax}.${freq}${suffile}_${Jzf2}_${Jzi2}

        mv trdens.out trdens.out_${proj}${iNuc}_${potential}_Nmax${Nmax}.${freq}${suffile}_Jz${Jzf}_Jz${Jzi}
        mv RGM_kernels.dat RGM_kernels.dat_${proj}${iNuc}_${potential}_Nmax${Nmax}.${freq}${suffile}_Jz${Jzf}_Jz${Jzi}
        mv RGM_kernel_terms.dat RGM_kernel_terms.dat_${proj}${iNuc}_${potential}_Nmax${Nmax}.${freq}${suffile}_Jz${Jzf}_Jz${Jzi}
        rm -f mfdi.egv
        rm -f mfdf.egv
        fi

    done

    done

done
