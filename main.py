import subprocess
import re
from xml_extractor import xml_extractor
import sys
from interface import prepare_simulation
from interface import generate_update
from contextlib import contextmanager
import os

@contextmanager
def cd(newdir):
    prevdir = os.getcwd()
    os.chdir(newdir)
    try:
        yield
    finally:
        os.chdir(prevdir)

cwd = subprocess.Popen(["pwd"], stdout = subprocess.PIPE, stderr = subprocess.STDOUT).communicate()[0]

with open('settings.xml', 'r') as outfile:  
    prog_path = re.search(r'<code_directory>(.+)</code_directory>', outfile.read()).group(1)

xml_extractor=xml_extractor.XMLExtractor()
xml_extractor.Parse('settings.xml')
max_iter=int(xml_extractor.GetText('main', 'max_iter'))
conv_crit_thresh=float(xml_extractor.GetText('main', 'conv_thresh'))
opt_type=xml_extractor.GetText('optimization', 'type')
num_threads=int(xml_extractor.GetText('simulation', 'num_threads'))
equil_time=float(xml_extractor.GetText('simulation', 'equil_time'))

output = subprocess.Popen([prog_path.strip()+"/init.sh"], stdout = subprocess.PIPE, stderr = subprocess.STDOUT).communicate()[0]
work_dir=output.split("\n")
new_dir=int(work_dir[1].lstrip('step_'))
old_dir=int(work_dir[0].lstrip('step_'))

if old_dir == new_dir:
    if old_dir == 0:
        #need an initial guess
        print "initial guess needed"
        sys.exit()
    else:
        #might need to post process then need to update parameters
        print "post process"
        sys.exit()
        new_dir += 1
if old_dir+1 != new_dir:
    print old_dir, new_dir, "old and new directory are not consistent"

conv_crit = conv_crit_thresh + 1.0
while new_dir <= max_iter and conv_crit >= conv_crit_thresh:
    #move files around
    work_dir[1]=subprocess.Popen([prog_path.strip()+"/prepare_gromacs.sh", str(new_dir)], stdout = subprocess.PIPE, stderr = subprocess.STDOUT).communicate()[0]
    #prepare simulation files, Ryan's python script, json & grompp are in the cwd
    print work_dir[1]
    with cd(cwd.strip()+'/'+work_dir[1].strip()):
        cwd2 = subprocess.Popen(["pwd"], stdout = subprocess.PIPE, stderr = subprocess.STDOUT).communicate()[0]
        print cwd2
        prepare_simulation.PrepareSimulation()
        sys.exit()
        #run simulation
        dum1=subprocess.Popen(["./run_gromacs.sh", num_threads])
        #post process
        if opt_type == 'relative_entropy':
            dum1=subprocess.Popen(["./run_rdf_gromacs.sh", num_threads, equil_time])
        else:
            print 'opt_type not recognized'
            sys.exit()
        #update parameters
        dum1=subprocess.Popen(["./interface/generate_update.py"])
sys.exit()
