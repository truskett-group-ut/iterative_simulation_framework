import json
import sys
import re

with open('../settings.xml', 'r') as outfile:  
    path = re.search(r'<code_directory>(.+)</code_directory>', outfile.read()).group(1)

sys.path.insert(0, path)

from xml_extractor import xml_extractor 
from potentials import potential_combiner

#read in the initialization data
with open('../potential_specs__params_state.json') as data_file:    
    potential_specs__params_state = json.load(data_file)
    potential_specs = potential_specs__params_state['specs']
    params_state = potential_specs__params_state['state']
    
#create the potential
potential = potential_combiner.Potential(potential_specs)
potential.SetParamsState(params_state)

#read in potential parameter values
with open('./params_val.json') as data_file:    
    params_val = json.load(data_file)

#load in xml settings
xml_extractor = xml_extractor.XMLExtractor()
xml_extractor.Parse('../settings.xml')

###########################################################################################

optimization_type = xml_extractor.GetText('optimization', 'type').strip().lower()
if optimization_type == 'relative_entropy':
    from relative_entropy_optimizer import relative_entropy_update
    xmlParser = lambda x: xml_extractor.GetText('optimization', 'relative_entropy', x)

    #perform relative entropy update
    relative_entropy_update = relative_entropy_update.RelativeEntropyUpdate()
    relative_entropy_update.LoadPotential(potential, params_val)
    relative_entropy_update.LoadRadialDistFuncs('./rdf.xvg', '../rdf_target.xvg', spacing=float(xmlParser('dr_integrate')))
    params_val_out = relative_entropy_update.CalcUpdate(learning_rate=float(xmlParser('learning_rate')))
else:
    raise Exception('Invalid simulation program provided in settings file.')
    
#write out new potential parameter values
with open('./params_val_out.json', 'w') as data_file:      
    json.dump(params_val_out, data_file, indent=4, sort_keys=True)
    
#write out the old one but in sorted order
with open('./params_val.json', 'w') as data_file:    
    json.dump(params_val, data_file, indent=4, sort_keys=True)