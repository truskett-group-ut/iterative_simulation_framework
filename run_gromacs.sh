#!/bin/bash
#wp: input: 1. num of cores (int) 2. outconfig file from simulation
#

nt=$1
outconfig_file=$2 

if [ -f $PWD/../my_run_gromacs.sh ]; then
  $PWD/../my_run_gromacs.sh
else
  gmx grompp -n ../index.ndx -p ../topol.top
  grompp_status=$?
  #ensures grompp is done correctly else doesn't run simulation
  if [ $grompp_status -eq 0 ]; then
	gmx mdrun -nt $nt -x traj.xtc -g 
	if [ -f $outconfig_file ]; then
	  touch done.txt
	else
	  echo "gromacs crashed for some reason, consult the log file" 
	  exit 1 
	fi 
  else
	echo "Grompp failed. Check your input"
	exit 1;
  fi
fi
