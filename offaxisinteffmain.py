import numpy as np
import peakmatching as pm
import inteffcalculation as inteff
import matplotlib.pyplot as plt
import argparse


# function that runs the data extraction for the output file
# searches through the keys for a number 
# returns that number 
# for the specific filename format given in the README for this script 
# this returns the angles of observation.

def extract_angles(all_opt_parameters):

    # import re for the search function 
    import re

    # initialise lists
    angles = []
    
    # code using re.search adapted from stackoverflow
    # https://stackoverflow.com/questions/8234641/how-do-i-find-one-number-in-a-string-in-python
    for single_key in all_opt_parameters:
        if 'popt' in single_key:
            number = re.search(r'\d+', single_key).group()
            angles.append(int(number))

    # convert from list to array
    angles = np.asarray(angles)
    
    # return the angles
    return angles

# function to run intrinsic efficiency for each file
# plot int eff vs angle from normal
def off_axis_response_inteff(calibration_filename, output_file):
    # extract the data
    all_opt_parameters = pm.read_parameters(output_file)
    
    # set function
    function = "resolution"
    
    # unzip the data from the dictionary into lists
    popt_sigmas, pcov_sigmas, keys, popt_means = pm.unzip_popt_pcov(all_opt_parameters, function)
    
    # match the known energies to the peaks
    equivalent_energies = pm.match_peak_to_energy(keys, popt_means)

    energy_sorted, intrinsic_efficiency, inteff_error, energy, efficiency_model = \
        inteff.intrinsic_eff_calculation(calibration_filename, output_file)

    angles_sorted = pm.data_sorting(equivalent_energies, angles)
    
    detector_name = input("input the name of the detector bring calibrated:",)
    element = pm.discern_element(next(iter(all_opt_parameters)))

    # plot the datapoints for the peaks and a quadratic best fit model
    plt.figure(figsize=(7, 5))
    plt.scatter(angles_sorted, intrinsic_efficiency, label='Intrinsic efficiency', color='red')
    plt.errorbar(angles_sorted, intrinsic_efficiency, yerr = inteff_error, fmt = 'o', ecolor = 'b', capsize = 8)
    plt.xlabel('Angle (°)')
    plt.ylabel('Intrinsic \n Efficiency')
    plt.title(f'Variation of Intrinsic Efficiency with Angle:{detector_name}, {element}')
    plt.grid(True)
    plt.show()

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("Output_Filename", type=str, help="the name of the output file from spectramodelfitting.py ")
    parser.add_argument("Calibration_Filename", type=str, help="The name of the file containing calibration data for the sources.")
    return parser.parse_args()

if __name__ == "__main__":
    arguments = parse_arguments()
    intrinsic_eff_plot(, arguments.Calibration_Filename, arguments.Output_Filename)