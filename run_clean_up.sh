#!/bin/bash
#
if [ ! -f ../convergence.txt ]; then
    touch ../convergence.txt
fi

echo $1 > conv2.csv
paste conv2.csv conv.csv > conv3.csv

cat conv3.csv >> ../convergence.txt
rm conv.csv
rm conv?.csv
rm rdf_??.???
rm rho.dat
