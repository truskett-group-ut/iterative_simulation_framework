#!/bin/bash
#
# script to run iterative optimization prcedures 
# requiring a simulation component
MAX_ITER=100
CONV_CRIT=0.01
#
# first check to find the last completed step
#
STEP_PRE=step_
i=0
j=000
TEST_DIR=$STEP_PRE$j
while [ -d $TEST_DIR ]; do
    let i+=1
    printf -v j "%03g" $i
    TEST_DIR=$STEP_PRE$j
done
let i-=1
printf -v j "%03g" $i
TEST_DIR=$STEP_PRE$j
while [ ! -f $TEST_DIR/done.txt ] && [ $i -ge 0 ]; do
    let i-=1
    printf -v j "%03g" $i
    TEST_DIR=$STEP_PRE$j
done
OLD_DIR=$STEP_PRE$j
let i+=1
printf -v j "%03g" $i
NEW_DIR=$STEP_PRE$j
#
# Archive any later incomplete steps
#
if [ $i -eq 0 ]; then
    mkdir $NEW_DIR
    cp conf.gro $NEW_DIR/confout.gro
    if [ $SOME_FLAG -eq 'yes' ]; then
        cd $NEW_DIR
#   call a script to generate an initial guess if needed
        cd .. 
    elif [ $SOME_FLAG -eq 'no' ]; then
        cp A-A.pot.new $NEW_DIR/A-A.pot.new
    else;
        echo "initial guess flag must be x, x, or x"
        exit
    fi
    let i+=1
    printf -v j "%03g" $i
    NEW_DIR=$STEP_PRE$j
fi
while [ $i -lt $MAX_ITER ]; do
    mkdir $NEW_DIR
    cp $OLD_DIR/confout.gro $NEW_DIR/conf.gro
    cp $OLD_DIR/A-A.pot.new $NEW_DIR/A-A.pot.old
    cp grompp.mdp $NEW_DIR/grompp.mdp
#   run a script that updates grompp.mdp cut-off and makes the table.xvg file
    cd $NEW_DIR
    grompp -n index.ndx
    mdrun -nt 2 -x traj.xtc -g -v 
#   some sort of bash script to run your analysis
#   the potential update script
done
