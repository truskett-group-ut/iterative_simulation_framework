#!/bin/bash

if [ $1 -lt 10 ]; then
    ./multi_g_rdf -$1 -b $2 -e 5500 -- -bin 0.01 << 'EOF' 
    2
    2
    'EOF'

else
    ./multi_g_rdf --$1 -b $2 -e 5500 -- -bin 0.01 << 'EOF' 
    2
    2
    'EOF'

fi

rdf_exit=$?

exit $rdf_exit

