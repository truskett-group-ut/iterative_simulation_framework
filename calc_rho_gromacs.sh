#!/bin/bash

unit_convert=1.6605402
gmx energy -b $1 -xvg none < done.txt > rho_stats.dat
gmx_rho=`awk '$1 == "Density" {print $2}' < rho_stats.dat`
if [ $2 -eq '3' ]; then
    echo "$gmx_rho / $unit_convert" | bc -l > rho.dat
elif [ $2 -eq '2' ]; then
    echo "2D isn't coded up yet. curse gromacs v5 and complain to beth"
else 
    echo "why are you trying to do RE in dimensions other than 2 or 3???"
fi
