#!/bin/bash
#
if [ -f $PWD/../my_run_gromacs.sh ]; then
  $PWD/../my_run_gromacs.sh
else
  gmx grompp -n ../index.ndx -p ../topol.top
  #mdrun -nt $1 -x traj.xtc -g -v
  gmx mdrun -nt $1 -x traj.xtc -g 
fi
if [ -f $2 ]; then
  touch done.txt
else
  echo "gromacs crashed for some reason, consult the log file" 
fi 
exit 
