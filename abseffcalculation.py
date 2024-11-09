import numpy as np
import peakmatching as pm
import activitiycalculation as ac



# function to calculate absolute efficiency = cps recorded/activity(Bq)
def calc_absolute_eff(calibration_filename, output_file):
    
    # need keys, cps data, present activity, energies

    
    # read in the optimum parameters file
    all_opt_parameters = pm.read_parameters(output_file)

    # set the function
    function = "absolute efficiency"
    
    # unzip the data from the dictionary into lists
    popt_amplitudes, pcov_amplitudes, files_used, keys, popt_means = \
    pm.unzip_popt_pcov(all_opt_parameters, function)

    # match the known energies to the peaks
    equivalent_energies = pm.match_peak_to_energy(keys, popt_means)

    # sort the data in direction of increasing energy
    energy_sorted, amps_sorted = pm.data_sorting(equivalent_energies, popt_amplitudes)
    energy_sorted, err_amps_sorted = pm.data_sorting(equivalent_energies, pcov_amplitudes)
    energy_sorted, files_used_sorted = pm.data_sorting(equivalent_energies, files_used)
    energy_sorted, keys_sorted = pm.data_sorting(equivalent_energies, keys)  
    
    #initialsise a dictionary to store the corresponding activities
    all_activities = {}
    
    # loop over each filename for the peaks
    for file in files_used_sorted:

        # calculate the activity for each 
        current_activity, key, collection_date = ac.present_activty(file, calibration_filename)
        
        # express the activity in becquerels (uCi to Bq - x370,000)
        current_activity  = current_activity*370000

        # create a dictionary key
        act_key = f'element_{key}_in Bq:'
        all_activities[act_key] = current_activity

    # initialise an array to hold the efficiencies
    absolute_efficiency = np.zeros(len(amps_sorted))
    abseff_error = np.zeros(len(err_amps_sorted))

    # Calculate the absolute efficiency for each cps value
    for i in range(len(amps_sorted)):
        # find the relevant acitivity for each peak
        if 'Cobalt' in keys_sorted[i]:
            activity = all_activities['element_60-Co_in Bq:']
        elif 'Caesium' in keys_sorted[i]:
            activity = all_activities['element_Cs_in Bq:']
        elif 'Americium' in keys_sorted[i]:
            activity = all_activities['element_Am_in Bq:']
        elif 'Barium' in keys_sorted[i]:
            activity = all_activities['element_Ba_in Bq:']

        # calculate the efficiency
        absolute_efficiency[i] = amps_sorted[i] / (activity)
        abseff_error[i] = err_amps_sorted[i] / (activity)
    
    # return the data
    return absolute_efficiency, energy_sorted, abseff_error
