import subprocess
import re
from xml_extractor import xml_extractor
import sys

cwd = subprocess.Popen(["pwd"], stdout = subprocess.PIPE, stderr = subprocess.STDOUT).communicate()[0]

with open('settings.xml', 'r') as outfile:  
    prog_path = re.search(r'<code_directory>(.+)</code_directory>', outfile.read()).group(1)

xml_extractor=xml_extractor.XMLExtractor()
xml_extractor.Parse('settings.xml')

output = subprocess.Popen([prog_path.strip()+"/init.sh"], stdout = subprocess.PIPE, stderr = subprocess.STDOUT).communicate()[0]
work_dir=output.split("\n")
new_dir=int(work_dir[1].lstrip('step_'))
old_dir=int(work_dir[0].lstrip('step_'))

if old_dir == new_dir:
    if old_dir == 0:
        #need an initial guess
        print "initial guess needed"
        new_dir += 1
    else:
        #might need to post process then need to update parameters
        print "post process"
        new_dir += 1
if old_dir+1 != new_dir:
    print old_dir, new_dir, "old and new directory are not consistent"
print "pass"

while new_dir <= max_iter and conv_crit >= conv_crit_thresh:
    #move files around
    dum1=subprocess.Popen(["./prepare_gromacs.sh", new_dir])
    #prepare simulation files, Ryan's python script, json & grompp are in the cwd
    dum1=subprocess.Popen(["./interface/prepare_simulation.py"])
    #run simulation
    dum1=subprocess.Popen(["./run_gromacs.sh", num_threads])
    #post process
    if opt_type == 'RE':
        dum1=subprocess.Popen(["./run_rdf_gromacs.sh", num_threads, equil_time])
    else:
        print 'opt_type not recognized'
        exit(1)
    #update parameters
    dum1=subprocess.Popen(["./interface/generate_update.py"])
sys.exit()
