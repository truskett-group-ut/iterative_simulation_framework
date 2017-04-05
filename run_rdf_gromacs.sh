#!/bin/bash

if [ $2 -lt 10 ]; then
    flag='-'
else
    flag='--'
fi

nt=$flag$2

$1/multi_g_rdf $nt -b $3 -e $4 -n ../index.ndx -- -bin 0.01 << 'EOF' 
2
2
'EOF'

rdf_exit=$?

exit $rdf_exit

