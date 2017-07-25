#!/bin/bash
#wp:input: 1. program directory (str) 2. num of threads (int) 3. beginning of rdf collection time(ps) 
# 	   4. end rdf collection time(ps) 5. system dimension (int) 6. components number (int)

if [ $2 -lt 10 ]; then
    flag='-'
else
    flag='--'
fi

#wp:num of cores to use in multi_g_rdf
nt=$flag$2
#wp:pass down dimension and components args
dimension=$5
num_components=$6 
if [ $dimension -eq 2 ]; then 
	if [ $num_components -eq 1 ]; then
	#wp:flag -xy tells gromacs to compute the 2D rdf from a 3D run
	#wp:using '<<-' allows tabs in the here-doc section 
	$1/multi_g_rdf $nt -b $3 -e $4 -n ../index.ndx -- -bin 0.01 -xy <<-'EOF' 
		2
		2
		EOF
		#wp:exit status
		rdf_exit=$?  
		exit $rdf_exit 
	elif [ $num_components -gt 1 ]; then 
		#wp: Computes rdf for every component pair i-j and renames output files to corresponding components e.g. 1-2 --> A_B etc
		component_name=( A  B  C  D  E  F  G  H  I  J  K  L  M  N  O  P  Q  R  S  T  U  V  W  X  Y  Z )
		for (( i = 1 ; i <= $num_components; i++ )); do
			for (( j=$i; j<=$num_components; j++ )); do
			#wp: it is implicit that the index file for gromacs is such that A->1, B->2 etc; No quotation on delimeter EOF to replace variables
			$1/multi_g_rdf $nt -b $3 -e $4 -n ../index.ndx -- -bin 0.01 -xy <<-EOF 
				$i
				$j
				EOF

				#wp:renames files; Array index begins from 0
				ii=$(($i-1)); jj=$(($j-1))
				rdf_ij="rdf_"${component_name[ii]}"_"${component_name[jj]}".xvg"
				mv rdf.xvg $rdf_ij
			done
		done 
		#wp: remove temp rdf files
		rm *#*rdf*
		#wp:exit status
		rdf_exit=$?  
		exit $rdf_exit 
	fi	
else #wp: 3D assumed #will add the multicompo once the 2D is proven to work
$1/multi_g_rdf $nt -b $3 -e $4 -n ../index.ndx -- -bin 0.01 <<-'EOF' 
	2
	2
	EOF
	#wp:exit status
	rdf_exit=$?  
	exit $rdf_exit 
fi 
#---end of script
