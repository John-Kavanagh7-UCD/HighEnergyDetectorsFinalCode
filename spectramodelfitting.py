import numpy as np
import matplotlib.pyplot as plt 
import json 
import scipy.optimize as spo
import argparse 
import spectrumplot as sp


# function to define the suffix for readable outputs
def set_suffix(index):
    
    if index == 0: suffix = 'st'
    elif index == 1: suffix = 'nd'
    elif index == 2: suffix = 'rd'
    else: suffix = 'th'
    
    return suffix

# function to plot a spectrum from a given file 
# request user input to define the range of data 
# storing the photopeaks
def find_peaks(filename):

    # run the relavent functions to plot the spectrum
    data_cps_array, channels, expt_info = sp.plot_spectrum(filename)

    # initialise relevant lists
    peak_starts = []
    peak_ends = []

    # request user input to define what peaks they want to analyse 
    num_peaks = int(input('please input the total number of \
photopeaks you wish to analyse:'))
    
    # loop over number peaks input
    # set the suffix depending on which peak it is.
    for index in range(0, num_peaks):         
        suffix = set_suffix(index)

    # request user input to define range of channels the photopeaks is stored
        start = float(input(f'please input the approximate count value at \
which the {index+1}{suffix} photopeak begins:'))
        end = float(input(f'please input the approximate count value at \
which the {index+1}{suffix} photopeak ends:'))
    
        # append the data to the lists
        peak_starts.append(start)
        peak_ends.append(end)

    return peak_starts, peak_ends, data_cps_array, channels

# function defining a gaussian model
def model_gaussian(x, mu, sigma, A):
    gauss = ((A / (np.sqrt(2 * np.pi) * sigma)) *
             np.exp(-((x - mu) ** 2) / (2 * sigma ** 2)))
    return gauss

# function to take the pre-set channels containing the peak 
# and return a cropped array of just those channels
# note: only completes this for 1 peak
def crop_to_peak(data_cps_array, channels, peak_starts, peak_ends):

    # initialise the lists for storage
    cps_crop = []
    channels_crop = []

    # loop over all channels,
    # store the data if within the pre-set range
    for i in range(len(channels)):
        if peak_starts <= channels[i] <= peak_ends:
            channels_crop.append(channels[i])
            cps_crop.append(data_cps_array[i])

    # return the data containing the peak
    return cps_crop, channels_crop

# function that takes a single peak,
# and uses curve_fit to fit a gaussian to it.
def gauss_curve_fit(cps_crop, channels_crop, index):

    # set suffix for ouptuts
    suffix = set_suffix(index)
    
    # plot the photopeak so the user can guess the parameters
    fig, ax =plt.subplots(figsize=(3,3))
    ax.plot(channels_crop,  cps_crop)
    ax.set_xlabel('Channel')
    ax.set_ylabel('Counts/Second \n (CPS)')
    fig.suptitle(f'The {index+1}{suffix} Photopeak')
    plt.show()
    
    # request guesses for fitting the gaussian model
    mu_guess = float(input(f'please input a guess for the channel \
that corresponds to the {index+1}{suffix} photopeaks max:', ))
    sigma_guess = float(input(f'please input a guess for the FWHM \
that corresponds to the {index+1}{suffix} photopeak:', ))
    A_guess = float(input(f'please input a guess for the Amplitude \
that corresponds to the {index+1}{suffix} photopeak:', ))

    # use curve_fit to find the optimum paramters for the model fit
    popt, pcov = spo.curve_fit(model_gaussian, channels_crop, cps_crop, 
                               p0 = [mu_guess, sigma_guess, A_guess])

    # plot the model fit with the photopeak
    fig, ax =plt.subplots(figsize=(3,3))
    ax.plot(channels_crop,  cps_crop)
    ax.plot(channels_crop, model_gaussian(channels_crop, *popt), 
             'g', label = 'Gaussian')
    ax.legend()
    ax.set_xlabel('Channel')
    ax.set_ylabel('Counts/Second \n (CPS)')
    fig.suptitle(f'The Gaussian Modelled {index+1}{suffix} Photopeak')
    plt.show()
    
    # return the optimised parameters
    return popt, pcov

# function that takes a single file
# plots the spectrum
# assists user in identiying the peaks 
# loops over each peak 
# fits the gaussian model to the peak
# returns a dictionary storing the optimum parameters
def fit_single_spectrum(filename):

    # initialise a dictionary to store popt and pcov
    opt_parameters = {}
    peak_filenames = []

    # extract the data from the file and identify peaks of interest
    peak_starts, peak_ends, data_cps_array, channels = find_peaks(filename)

    # loop over the peaks
    for index in range(len(peak_starts)): 

        # analyse section of spectrum containing peak only
        cps_crop, channels_crop = crop_to_peak(data_cps_array, channels, 
                                        peak_starts[index], peak_ends[index])

        # apply curve_fit and extract the optimum parameters
        popt, pcov = gauss_curve_fit(cps_crop, channels_crop, index)
        popt_key = f'popt_{filename}_peak{index+1}'
        pcov_key = f'pcov_{filename}_peak{index+1}'
        peak_filenames.append(filename)

        # Store popt and pcov in the dictionary
        opt_parameters[popt_key] = popt
        opt_parameters[pcov_key] = pcov
        
    # return the optimum parameters
    return opt_parameters, peak_filenames

# function that takes a list of files 
# loops each one through the single file analyis
# stores all optimised curve_fit parameters in a dictionary
def fit_all_spectra(list_of_files):

    # initialise a dictionary to store popt and pcov
    all_opt_parameters = {}
    all_peak_filenames = []
    all_peak_filenames_new = {}

    # loop over the files
    for file in list_of_files:

        # apply single file analysis 
        # and append the parameers to dictionary
        opt_parameters, peak_filenames = fit_single_spectrum(file)
        all_opt_parameters.update(opt_parameters)
        # create a list of all the filenames associated to the peaks
        for name in peak_filenames:
            all_peak_filenames.append(name)

    # convert the list to a dictionary and add it to the opt parameters dict
    filenames_key = 'list_of_files'
    all_peak_filenames_new[filenames_key] = all_peak_filenames
    all_opt_parameters.update(all_peak_filenames_new)
    
    # convert the arrays in the dctionary to lists for json
    # code adapted from https://stackoverflow.com/a/51915312
    all_opt_parameters_new = {k: v.tolist() if isinstance(v, np.ndarray) else v
                              for k, v in all_opt_parameters.items()}

    # open a file and use json to write the dictionary into the file
    with open(input("what you would like to name the output txt file:",), "w") as output:
        json.dump(all_opt_parameters_new, output)


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("Spectra_Filenames", type=str,
                        nargs = '+',help="the names of the .spe or .mca datafiles")
    return parser.parse_args()

if __name__ == "__main__":
    arguments = parse_arguments()
    main(arguments.Spectrum_Filename)
