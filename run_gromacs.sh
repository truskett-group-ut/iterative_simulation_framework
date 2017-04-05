#!/bin/bash
#
if [ -f $PWD/../my_run_gromacs.sh ]; then
  $PWD/../my_run_gromacs.sh
else
  grompp -n ../index.ndx -p ../topol.top
  mdrun -nt $1 -x traj.xtc -g -v
fi
touch done.txt
exit 
