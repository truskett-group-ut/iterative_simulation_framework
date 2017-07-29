import json
import sys
import re

#wp: takes 'dim' and 'num_components' argument from main.py 
#def RelativeEntropy(dim):
def RelativeEntropy(dim,num_components):
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

	    #prepare the update module
	    from relative_entropy_optimizer import relative_entropy_update
	    xmlParser = lambda x: xml_extractor.GetText('optimization', 'relative_entropy', x)

	    #perform relative entropy update
	    relative_entropy_update = relative_entropy_update.RelativeEntropyUpdate()
	    relative_entropy_update.LoadPotential(potential, params_val)
	    relative_entropy_update.LoadRadialDistFuncs('./rdf.xvg', '../rdf_target.xvg', spacing=float(xmlParser('dr_integrate')))
	    #wp:passes down the dimension variable
	    learning_rate=float(xmlParser('learning_rate'))
	    params_val_out, conv_score = relative_entropy_update.CalcUpdate(learning_rate,dim)

	    #write out new potential parameter values
	    with open('./params_val_out.json', 'w') as data_file:      
		json.dump(params_val_out, data_file, indent=4, sort_keys=True)

	    #write out the old one but in sorted order
	    with open('./params_val.json', 'w') as data_file:    
		json.dump(params_val, data_file, indent=4, sort_keys=True)
		
	    return conv_score
    elif num_components > 1: 
	    #wp:Create list of names depending on the number of components chosen
	    potential_name_root="potential_specs__params_state"; potential_val_root="params_val"; 
	    potential_name_postfix=".json"
	    table_name="table"; table_postfix=".xvg"
	    #wp:To be used for table.xvg naming conventions where component A is 1, B, 2 etc etc
	    num2component={1:'A',2:'B',3:'C',4:'D',5:'E',6:'F',7:'G',8:'H',9:'I',10:'J',
	    		11:'K',12:'L',13:'M',14:'N',15:'O',16:'P',17:'Q',18:'R',19:'S',
	    		20:'T',21:'U',22:'V',23:'W',24:'X',25:'Y',26:'Z'}
	    #wp:Create empty directory to keep track of convergence metrics if necessary later
	    conv_score={} 

	    #wp: +1 since range goes for numbers less than max but we need to get max
	    for i in range(1,num_components+1):
	    	for j in range(i,num_components+1): 
		    from xml_extractor import xml_extractor 
		    from potentials import potential_combiner

		    #wp:generate file name read in the initialization data 
		    potential_specs_name_ij=potential_name_root+"_"+num2component[i]+'_'+num2component[j]+potential_name_postfix
		    potential_val_name_ij=potential_val_root+"_"+num2component[i]+'_'+num2component[j]+potential_name_postfix
		    #wp:read in the initialization data
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

		    #load in xml settings
		    xml_extractor = xml_extractor.XMLExtractor()
		    xml_extractor.Parse('../settings.xml')

		    ########################################################################################### 
		    #prepare the update module
		    from relative_entropy_optimizer import relative_entropy_update
		    xmlParser = lambda x: xml_extractor.GetText('optimization', 'relative_entropy', x)

		    #perform relative entropy update
		    relative_entropy_update = relative_entropy_update.RelativeEntropyUpdate()
		    relative_entropy_update.LoadPotential(potential, params_val)
		    #wp:generate rdf file names for each component
		    rdf_root="rdf_"; rdf_target_root="rdf_target_";
		    rdf_postfix=".xvg";
		    rdf_name=rdf_root+num2component[i]+'_'+num2component[j]+rdf_postfix
		    rdf_target_name=rdf_target_root+num2component[i]+'_'+num2component[j]+rdf_postfix 
		     
		    #relative_entropy_update.LoadRadialDistFuncs('./rdf.xvg', '../rdf_target.xvg', spacing=float(xmlParser('dr_integrate')))
		    relative_entropy_update.LoadRadialDistFuncs('./'+rdf_name, '../'+rdf_target_name, spacing=float(xmlParser('dr_integrate')))
		     
		    #wp:selects learning rate for each component defined as 'learning_rate_AA' etc 
		    learning_rate_name='learning_rate_'+num2component[i]+num2component[j] 
		    try: 
		    	learning_rate=float(xmlParser(learning_rate_name))
		    except: 
		    	#wp:Assume some default value 
		    	learning_rate=float(xmlParser('learning_rate')) 
		    
		    #wp:passes down the dimension variable
		    params_val_out, conv_score_ij = relative_entropy_update.CalcUpdate(learning_rate,dim)
		    #wp: creates extended dictionary of 'conv_score' for every component combo
		    for item in conv_score_ij.keys(): 
		   	#wp: idea is to conserve one pair of keys unmodified for compatilility later
		   	if i == num_components and j == num_components: 	
		   	    conv_score[item]=conv_score_ij[item] 
		   	else:
		   	    conv_score[num2component[i]+num2component[j]+'_'+item]=conv_score_ij[item] 

		    #write out new potential parameter values #wp: reflecting proper component
		    potential_val_name_ij_out=potential_val_root+"_"+num2component[i]+'_'+num2component[j]+'_out'+potential_name_postfix
		    #with open('./params_val_out.json', 'w') as data_file:      
		    with open('./'+potential_val_name_ij_out, 'w') as data_file:      
			json.dump(params_val_out, data_file, indent=4, sort_keys=True)

		    #write out the old one but in sorted order
		    #with open('./params_val.json', 'w') as data_file:    
		    with open('./'+potential_val_name_ij, 'w') as data_file:    
			json.dump(params_val, data_file, indent=4, sort_keys=True)
		
	    return conv_score
