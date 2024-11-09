import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import peakmatching as pm

# Define the model function
# Resolution as a function of Energy
def resolution_model(E, a, b, c):
    R = np.sqrt((a * E**(-2)) + (b * E**(-1)) + c)
    return R

# function to calculate resolution
# and plot a function of resolution vs energy
def resolution_calculation(output_file):

    # read in the optimum parameters file
    all_opt_parameters = pm.read_parameters(output_file)

    # set function
    function = "resolution"
    
    # unzip the data from the dictionary into lists
    popt_sigmas, pcov_sigmas, keys, popt_means = pm.unzip_popt_pcov(all_opt_parameters, function)
    
    # match the known energies to the peaks
    equivalent_energies = pm.match_peak_to_energy(keys, popt_means)

    # sort the data in direction of increasing energy
    energy_sorted, sigma_sorted = pm.data_sorting(equivalent_energies, popt_sigmas)
    energy_sorted, err_sigma_sorted = pm.data_sorting(equivalent_energies, pcov_sigmas)

    sigma_sorted = np.asarray(sigma_sorted)
    err_sigma_sorted = np.asarray(err_sigma_sorted)
    
    # calculate fwhm from sigma
    fwhm_sorted = 2*np.sqrt(2*np.log(2))*sigma_sorted
    err_fwhm_sorted = 2*np.sqrt(2*np.log(2))*err_sigma_sorted
    
    # Calculate resolution values from deltaE / E = fwhm / E
    resolution =  fwhm_sorted/energy_sorted
    err_resolution = err_fwhm_sorted/energy_sorted

    # initialise an energy array 
    energy_array = np.linspace(min(energy_sorted), max(energy_sorted), 100)
    
    # Use curve_fit to find the best-fitting parameters a, b, and c
    popt_resolution, pcov_resolution = \
        curve_fit(resolution_model,energy_sorted, resolution)
    
    # Extract the fitted parameters
    a, b, c = popt_resolution
    
    # Calculate the resolution model values using the best-fit parameters
    y_model = resolution_model(energy_array, a, b, c)

    return energy_sorted, resolution, y_model, err_resolution, energy_array

