#!/bin/bash
#wp:input: 1. new step number (int) 2. num of components (int)

STEP_PRE=step_
i=$1
printf -v j "%03g" $i
NEW_DIR=$STEP_PRE$j
let i-=1
printf -v j "%03g" $i
OLD_DIR=$STEP_PRE$j
#
mkdir $NEW_DIR
cp $OLD_DIR/confout.gro $NEW_DIR/conf.gro

#wp:Adjusts folder update procedure depending num of components
num_components=$2
if [[ $num_components -eq 1 ]]; then
	cp $OLD_DIR/params_val_out.json $NEW_DIR/params_val.json
elif [[ $num_components -gt 1 ]]; then 
	cd $OLD_DIR
	for i in params_val*out.json; do
		#wp:picks out the file component name e.g. _A_A
		comp_pair=${i:10:4}	
		#wp:reconstructs new val param file for appropriate component
		params_val_ij='params_val'$comp_pair'.json' 
		#echo $params_val_ij
		#wp:Then copies it
		cp $i ../$NEW_DIR/$params_val_ij
	done
	cd ..
fi 

cp grompp.mdp $NEW_DIR/grompp.mdp
echo $NEW_DIR
