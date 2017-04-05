#!/bin/bash

$1/multi_g_rdf --$2 -b $3 -e $4 -n ../index.ndx -- -bin 0.01 << 'EOF' 
2
2
'EOF'

rdf_exit=$?

exit $rdf_exit

