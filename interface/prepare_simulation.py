import json
import sys
import re

def MakeBool(text):
    text = text.lower()
    if re.match(r'\s*true\s*', text):
        return True
    elif re.match(r'\s*false\s*', text):
        return False

def Gromacs(num_components):
    """wp:Loads up potential specifications, values and writes gromacs potential table for a given number of components"""
    from xml_extractor import xml_extractor 
    from potentials import potential_combiner
	

    if num_components == 1:
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

        from gromacs_interface_tools import gromacs_potential_maker
        xmlParser = lambda x1, x2: xml_extractor.GetText('simulation', x1, x2)

        #generate gromacs data
        gromacs_potential_maker = gromacs_potential_maker.SimulationPotentialConverter()
        gromacs_potential_maker.LoadPotential(potential, params_val)
        gromacs_potential_maker.TabulatePotential(r_max=float(xmlParser('table', 'r_max')), 
                                                  dr=float(xmlParser('table', 'dr'))
                                                 )
        gromacs_potential_maker.CutShiftTabulated(e_max=float(xmlParser('potential', 'e_max')), 
                                                  f_max=float(xmlParser('potential', 'f_max')), 
                                                  r_max=float(xmlParser('potential', 'r_max')), 
                                                  shift=MakeBool(xmlParser('potential', 'shift'))
                                                 )
        gromacs_potential_maker.MakeTable(filename='./table.xvg')
        gromacs_potential_maker.InsertGromppCutoff(r_buffer=float(xmlParser('gromacs', 'r_buffer')), 
                                                   filename='./grompp.mdp')
        return None
    elif num_components > 1: #wp:using 'elif' rather than 'else' to avoid things like 0 and -1 etc 
        """In order to handle multicompo stuff for n systems, standard filenames will be assumed. e.g. 
       potential_specs_params_state_A_A.json == first component  self-self interactions
       potential_specs_params_state_A_B.json == second component  cross interactions etc """
	
        #load in xml settings to be used later
        xml_extractor = xml_extractor.XMLExtractor()
        xml_extractor.Parse('../settings.xml')
        
        ###########################################################################################
        
        #wp:Create list of names depending on the number of components chosen
        potential_name_root="potential_specs__params_state"; potential_val_root="params_val"; 
        potential_name_postfix=".json"
        table_name="table"; table_postfix=".xvg"
	#wp:To be used for table.xvg naming conventions where component A is 1, B, 2 etc etc
	num2component={1:'A',2:'B',3:'C',4:'D',5:'E',6:'F',7:'G',8:'H',9:'I',10:'J',
        		11:'K',12:'L',13:'M',14:'N',15:'O',16:'P',17:'Q',18:'R',19:'S',
        		20:'T',21:'U',22:'V',23:'W',24:'X',25:'Y',26:'Z'}
        
        #wp: +1 since range goes for numbers less than max but we need to get max
        for i in range(1,num_components+1):
            for j in range(i,num_components+1):
        	potential_specs_name_ij=potential_name_root+"_"+num2component[i]+'_'+num2component[j]+potential_name_postfix
        	potential_val_name_ij=potential_val_root+"_"+num2component[i]+'_'+num2component[j]+potential_name_postfix
        
        	#read in the initialization data for each component
        	#with open('../potential_specs__params_state.json') as data_file:    
        	with open('../'+potential_specs_name_ij) as data_file:    
        	    potential_specs__params_state = json.load(data_file)
        	    potential_specs = potential_specs__params_state['specs']
        	    params_state = potential_specs__params_state['state']
        
        	#create the potential
        	potential = potential_combiner.Potential(potential_specs)
        	potential.SetParamsState(params_state)
        
        	#read in potential parameter values
        	#with open('./params_val.json') as data_file:    
        	with open('./'+potential_val_name_ij) as data_file:    
        	    params_val = json.load(data_file)
        
        ###########################################################################################
        	from gromacs_interface_tools import gromacs_potential_maker
        	xmlParser = lambda x1, x2: xml_extractor.GetText('simulation', x1, x2) 
        
        	#generate gromacs data #wp: for now all potentials are processed the same way 
        	gromacs_potential_maker = gromacs_potential_maker.SimulationPotentialConverter()
        	gromacs_potential_maker.LoadPotential(potential, params_val)
        	gromacs_potential_maker.TabulatePotential(r_max=float(xmlParser('table', 'r_max')), 
        						  dr=float(xmlParser('table', 'dr'))
        						 )
        	gromacs_potential_maker.CutShiftTabulated(e_max=float(xmlParser('potential', 'e_max')), 
        						  f_max=float(xmlParser('potential', 'f_max')), 
        						  r_max=float(xmlParser('potential', 'r_max')), 
        						  shift=MakeBool(xmlParser('potential', 'shift'))
        				 )
		#wp:Creates variable name for each component table 
        	table_name_ij=table_name+"_"+num2component[i]+'_'+num2component[j]+table_postfix
        	#gromacs_potential_maker.MakeTable(filename='./table.xvg')
        	gromacs_potential_maker.MakeTable(filename='./'+table_name_ij)
        	gromacs_potential_maker.InsertGromppCutoff(r_buffer=float(xmlParser('gromacs', 'r_buffer')), 
        						   filename='./grompp.mdp')
        
        return None 
