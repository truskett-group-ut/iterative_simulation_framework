#!/bin/bash
#
STEP_PRE=step_
i=$1
printf -v j "%03g" $i
NEW_DIR=$STEP_PRE$j
i-=1
printf -v j "%03g" $i
OLD_DIR=$STEP_PRE$j
#
mkdir $NEW_DIR
cp $OLD_DIR/confout.gro $NEW_DIR/conf.gro
cp $OLD_DIR/params_out.json $NEW_DIR/params.json
cp grompp.mdp $NEW_DIR/grompp.mdp
cd $NEW_DIR
#   run a script that updates grompp.mdp cut-off and makes the table.xvg file
grompp -n ../index.ndx -p ../topol.top
mdrun -nt 2 -x traj.xtc -g -v 

