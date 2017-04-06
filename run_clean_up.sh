#!/bin/bash
#
if [ ! -f ../convergence.txt ]; then
    touch ../convergence.txt
fi

cat conv.csv >> ../convergence.txt
rm conv.csv
rm rdf_??.???
