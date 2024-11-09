import numpy as np
import json 


# function to identify which source used in a given file
def discern_element(key):
    if 'Caesium' in key:
        return 'Caesium'
    elif 'Barium' in key:
        return 'Barium'
    elif 'Cobalt' in key:
        return 'Cobalt'
    elif 'Americium' in key:
        return 'Americium'
    return None

# function to read in the data from the output file using json
def read_parameters(output_file):
    with open(output_file) as file:
        output = file.read()

    all_opt_parameters = json.loads(output)

    return all_opt_parameters

# function to take the dictionary of popts and pcovs
# extract the data into lists
# return the data
def unzip_popt_pcov(all_opt_parameters, function):

    # intitialise the lists 
    popt_means = []
    popt_sigmas = []
    popt_amplitudes = []
    keys = []
    pcov_means = []
    pcov_sigmas = []
    pcov_amplitudes = []
    files_used = []
    
    if function == "calibration":
        # loop over all keys in the dictionary
        for single_key in all_opt_parameters:
            element_name = discern_element(single_key)
            
            # failsafe in case element_name retruns 'None'
            if element_name:
                # take all the popt keys
                # append the means and sigmas to lists
                if 'popt' in single_key:
                    keys.append(element_name)
                    # Get the first element of the popt array (the mean)
                    popt_mean_value = all_opt_parameters[single_key][0]
                    popt_means.append(popt_mean_value)
    
                # take all the pcovs
                # calculate the errors of the popts from the diagonal elements of pcov
                elif 'pcov' in single_key:
                    array = np.asarray(all_opt_parameters[single_key])
                    errors = np.sqrt(np.diag(array))
                    pcov_means.append(errors[0])

        return popt_means, pcov_means, keys

    elif function == "resolution":
        # loop over all keys in the dictionary
        for single_key in all_opt_parameters:
            element_name = discern_element(single_key)
            
            # failsafe in case element_name retruns 'None'
            if element_name:
                # take all the popt keys
                # append the means and sigmas to lists
                if 'popt' in single_key:
                    keys.append(element_name)
                    # Get the first element of the popt array (the mean)
                    popt_mean_value = all_opt_parameters[single_key][0]
                    popt_means.append(popt_mean_value)
                    # Get the second element of the popt array (the sigma)
                    popt_sigma_value = all_opt_parameters[single_key][1]
                    popt_sigmas.append(popt_sigma_value)
    
                # take all the pcovs
                # calculate the errors of the popts from the diagonal elements of pcov
                elif 'pcov' in single_key:
                    array = np.asarray(all_opt_parameters[single_key])
                    errors = np.sqrt(np.diag(array))
                    pcov_sigmas.append(errors[1])

        return popt_sigmas, pcov_sigmas, keys, popt_means

    elif function == "absolute efficiency":
        # loop over all keys in the dictionary
        for single_key in all_opt_parameters:
            element_name = discern_element(single_key)

            # failsafe in case element_name retruns 'None'
            if element_name:
                # take all the popt keys
                # append the means and sigmas to lists
                if 'popt' in single_key:
                    keys.append(element_name)
                    # Get the first element of the popt array (the mean)
                    popt_mean_value = all_opt_parameters[single_key][0]
                    popt_means.append(popt_mean_value)
                    # Get the third element of the popt array (the amplitude)
                    popt_amp_value = all_opt_parameters[single_key][2]
                    popt_amplitudes.append(popt_amp_value)
    
                # take all the pcovs
                # calculate the errors of the popts from the diagonal elements of pcov
                elif 'pcov' in single_key:
                    array = np.asarray(all_opt_parameters[single_key])
                    errors = np.sqrt(np.diag(array))
                    pcov_amplitudes.append(errors[2])

            else:
                if 'list_of_files' in single_key:
                    files_used = all_opt_parameters[single_key]

        return popt_amplitudes, pcov_amplitudes, files_used, keys, popt_means

# function to convert the data from lists to sorted arrays
# arrays need to be sorted in increasng energy order for plotting
def data_sorting(equivalent_energies, other_param):
    
    # turn all lists to arrays
    equivalent_energies = np.asarray(equivalent_energies)
    other_param = np.asarray(other_param)
    # sort the energies in increasing order for ease of plotting
    # sort the data by completing the same transfers so they are still related
    sorting_index = np.argsort(equivalent_energies)
    
    energy_sorted = [equivalent_energies[i] for i in sorting_index]
    other_param_sorted = [other_param[i] for i in sorting_index]

    # return the sorted data
    return energy_sorted, other_param_sorted


# define an array of known photopeaks
known_peaks = {
    'Caesium': np.array([31.8174, 32.1939, 36.31, 37.26, 661.657 ]),
    'Americium': np.array([11.89, 13.9, 17.81, 20.82, 26.3446, 33.1963, 59.5409]),
    'Barium': np.array([ 30.625, 30.973, 34.92, 35.82, 53.1622, 79.6142, 80.9979, 276.3989, 
                        302.8508, 356.0129, 383.8485]),
    'Cobalt': np.array([ 1173.228, 1332.492])}


# function to take the optimum parameters file
# extract the data
# link a known energy to a given peak
def match_peak_to_energy(keys, popt_means):
    
    equivalent_energies = []
    
    for i, element_name in enumerate(keys):
        # Energies of known peaks stored in dictionary
        # asks user input to link a known energy to the means
        list_of_peaks = known_peaks[element_name]
        
        energy_value = float(input(f"which of the following peaks: \
{list_of_peaks} corresponds to {element_name} with mean counts {popt_means[i]}", ))
        
        equivalent_energies.append(energy_value)
                
    # returns the energies
    return equivalent_energies


