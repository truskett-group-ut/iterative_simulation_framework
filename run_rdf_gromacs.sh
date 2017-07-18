#!/bin/bash
#wp:input: 1. program directory (str) 2. num of threads (int) 3. beginning of rdf collection time(ps) 
# 	   4. end rdf collection time(ps) 5. system dimension (int)

if [ $2 -lt 10 ]; then
    flag='-'
else
    flag='--'
fi

nt=$flag$2

dimension=$5
if [ $dimension -eq 2 ]; then 
#wp:flag -xy tells gromacs to compute the 2D rdf from a 3D run
#wp:using '<<-' allows tabs in the here-doc section 
$1/multi_g_rdf $nt -b $3 -e $4 -n ../index.ndx -- -bin 0.01 -xy <<-'EOF' 
	2
	2
	EOF
	#wp:exit status
	rdf_exit=$?  
	exit $rdf_exit 
else #wp: 3D assumed 
$1/multi_g_rdf $nt -b $3 -e $4 -n ../index.ndx -- -bin 0.01 <<-'EOF' 
	2
	2
	EOF
	#wp:exit status
	rdf_exit=$?  
	exit $rdf_exit 
fi 
#---end of script
