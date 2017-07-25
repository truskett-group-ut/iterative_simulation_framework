import subprocess
import re
from xml_extractor import xml_extractor
import sys
from interface import prepare_simulation
from interface import generate_update
from contextlib import contextmanager
import os
from gromacs_interface_tools import gromacs_time
import csv

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
conv_key=xml_extractor.GetText('optimization', 'relative_entropy', 'conv_crit')
num_threads=int(xml_extractor.GetText('simulation', 'num_threads'))
equil_time=float(xml_extractor.GetText('simulation', 'equil_time')) 
#wp:Allows dimension specification as int (e.g. 2)
dim=int(xml_extractor.GetText('simulation', 'dimension'))
#wp: Takes in number of components  as int
num_components=int(xml_extractor.GetText('simulation', 'components'))
#wp: Given how extensively the num of components arguments is used, need to ensure it's a valid option or else quit everything
if num_components > 26 or num_components < 1:
	print "Must have at least one component but not more than 26 for current version. Program executed and buried."
        sys.exit()
#wp: specifies program name e.g. gromacs
sim_prog=xml_extractor.GetText('simulation', 'program')
sim_prog=sim_prog.lower()

if sim_prog == "gromacs":
    inconfig = "conf.gro"
    outconfig = "confout.gro"
    end_time=gromacs_time.GromacsTime()
else:
    print "I don't work with simulations packages other than Gromacs v5 yet"

#wp: pre-processing of steps 
#determine which step we are on and initialize step_000 if needed
script_and_args=[prog_path.strip()+"/init.sh", inconfig, outconfig str(num_components)]
output = subprocess.Popen(script_and_args, stdout = subprocess.PIPE, stderr = subprocess.STDOUT).communicate()[0]
work_dir=output.split("\n") 

new_dir=int(work_dir[1].lstrip('step_'))
old_dir=int(work_dir[0].lstrip('step_'))
conv_crit = conv_crit_thresh + 1.0

#if opt_type == "relative_entropy":
#wp:Chooses post processing file name and opt type
if opt_type == "relative_entropy" and num_components == 1:
    post_process_file="rdf.xvg"
elif opt_type == "relative_entropy" and num_components > 1: 
    post_process_file="rdf_A_B.xvg" #wp: to be modified later

post_process_script="/run_rdf_gromacs.sh"

#determine what (if anything) needs to happen to finish the latest step available
if old_dir == new_dir:
    if old_dir == 0:
        #need an initial guess
        print "initial guess needed"
        sys.exit()
    else:
        #might need to post process then need to update parameters
        with cd(cwd.strip()+'/'+work_dir[1].strip()):
            try:
                check_pp=subprocess.check_output(["ls", post_process_file])
                stat_pp=0
            except subprocess.CalledProcessError as e:
                stat_pp=e.returncode
            if stat_pp != 0:
                proc_rdf=subprocess.Popen([prog_path.strip()+post_process_script, prog_path.strip(), str(num_threads), str(equil_time), str(end_time), str(dim),
					str(dim), str(num_components)])
                proc_rdf.wait()
            conv=generate_update.RelativeEntropy(dim) 
            conv_crit=conv[conv_key]
            with open('conv.csv', 'wb') as f:
                w = csv.DictWriter(f, conv.keys(), delimiter=' ') 
                w.writerow(conv)
            proc_cleanup=subprocess.Popen([prog_path.strip()+"/run_clean_up.sh", str(new_dir)])
            new_dir += 1
if old_dir+1 != new_dir:
    print old_dir, new_dir, "old and new directory are not consistent"

while new_dir <= max_iter and conv_crit >= conv_crit_thresh:
    #move files around
    work_dir[1]=subprocess.Popen([prog_path.strip()+"/prepare_gromacs.sh", str(new_dir), str(num_components)], stdout = subprocess.PIPE, stderr = subprocess.STDOUT).communicate()[0]
    #prepare simulation files, Ryan's python script, json & grompp are in the cwd
    with cd(cwd.strip()+'/'+work_dir[1].strip()):
        #prepare_simulation.Gromacs()
	#wp: takes num_comp to adjust appropriate procedures
        prepare_simulation.Gromacs(num_components)
        #run simulation
        proc=subprocess.Popen([prog_path.strip()+"/run_gromacs.sh", str(num_threads), outconfig])
        proc.wait()
        #post process: compute rdf #wp: argument for dimension fed to the .sh script
        #proc_rdf=subprocess.Popen([prog_path.strip()+post_process_script, prog_path.strip(), str(num_threads), str(equil_time), str(end_time), str(dim)])
        proc_rdf=subprocess.Popen([prog_path.strip()+post_process_script, prog_path.strip(), str(num_threads), str(equil_time), str(end_time), 
					str(dim), str(num_components)])
        proc_rdf.wait()
        #update parameters #wp:passes 'dim' argument and num_components; Adjusts procedure accordingly in submodules
	conv=generate_update.RelativeEntropy(dim, num_components) 
        conv_crit=conv[conv_key]
        with open('conv.csv', 'wb') as f:
            w = csv.DictWriter(f, conv.keys(), delimiter=' ') 
            w.writerow(conv)
        proc_cleanup=subprocess.Popen([prog_path.strip()+"/run_clean_up.sh", str(new_dir)])
    new_dir += 1
print "optimization complete"
sys.exit()
