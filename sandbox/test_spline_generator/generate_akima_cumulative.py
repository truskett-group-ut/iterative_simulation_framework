import sys
import json
from numpy import arange, maximum, minimum

def GenerateAkimaCumulative(r_min, r_max, dr, d, epsilon=1.0, alpha=8, max_ur=float(1e8)):
    if r_max <= d*(2.0**(1.0/alpha)):
        raise Exception('The provided "r_max" is to short for generating an initial guess. Increase this by at least a little bit or decrease the input "d".')
    r_max = r_max + 1.0*dr
    r = arange(r_min, r_max+dr/2.0, dr)
    r = maximum(0.0001, r)
    ur = (r <= d*(2.0**(1.0/alpha)))*(4.0*epsilon*((d/r)**(2*alpha) - (d/r)**(alpha)) + epsilon)
    ur = minimum(max_ur, ur)
    return zip(r, ur)

if __name__ == "__main__":
    #print 'Input format:'
    #print '<spline_id> <positive_constraint>(true/false) <r_min> <r_max> <dr> <d>'
    
    #get provided input
    spline_id = sys.argv[1].strip()
    positive_constraint = sys.argv[2].lower() == 'true'
    r_min = float(sys.argv[3])
    r_max =float(sys.argv[4])
    dr = float(sys.argv[5])
    d = float(sys.argv[6])
    
    #generate the data
    r__ur = GenerateAkimaCumulative(r_min, r_max, dr, d)

    #format the data
    params_val = {}
    params_state = {}
    for r, ur in r__ur[:-2]:
        param_id = spline_id + '__' + unicode(r)
        params_val[param_id] = ur
        if positive_constraint:
            params_state[param_id] = {'opt': True, 'min': 0.0}
        else:
            params_state[param_id] = {'opt': True}
    for r, ur in r__ur[-2:]:
        param_id = spline_id + '__' + unicode(r)
        params_val[param_id] = ur
        params_state[param_id] = {'opt': False}
    
    potential_specs__params_state = {'specs': {spline_id: 'akima_cumulative'},
                                     'state': params_state
                                    }
    #dump the potential_specs__params_state
    with open('./potential_specs__params_state.json', 'w') as data_file:      
        json.dump(potential_specs__params_state, data_file, indent=4, sort_keys=True)
        
    #dump the params_val
    with open('./params_val.json', 'w') as data_file:      
        json.dump(params_val, data_file, indent=4, sort_keys=True)
