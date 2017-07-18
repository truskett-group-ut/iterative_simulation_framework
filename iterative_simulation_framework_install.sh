#!/bin/bash

echo '--------------------------------------------------------------------------'
echo 'Cloning and preparing git code repository'
echo '--------------------------------------------------------------------------'
git clone https://github.com/truskett-group-ut/iterative_simulation_framework.git
cd ./iterative_simulation_framework
git submodule init
git submodule update
chmod 744 *.sh
chmod 744 multi_g_rdf

echo '--------------------------------------------------------------------------'
echo 'Creating python virtual environment to handle dependencies'
echo '--------------------------------------------------------------------------'
virtualenv venv
source venv/bin/activate
`which pip` install numpy
`which pip` install scipy
`which pip` install numdifftools