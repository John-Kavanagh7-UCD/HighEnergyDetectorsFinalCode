import numpy as np
import matplotlib.pyplot as plt
import argparse 
import peakmatching as pm

# function to plot the means vs energies to get a calibration function that relates the two
def calibration_plot(output_file):

    # read in the optimum parameters file
    all_opt_parameters = pm.read_parameters(output_file)

    # set function
    function = "calibration"
    
    # unzip the data from the dictionary into lists
    popt_means, pcov_means, keys = pm.unzip_popt_pcov(all_opt_parameters, function)
    
    # match the known energies to the peaks
    equivalent_energies = pm.match_peak_to_energy(keys, popt_means)

    
    # sort the data in direction of increasing energy
    energy_sorted, means_sorted = pm.data_sorting(equivalent_energies, popt_means)
    energy_sorted, err_means_sorted = pm.data_sorting(equivalent_energies, pcov_means)

    
    # use numpy to fit a quadratic polynomial to the datapoints
    quadratic_fit_coeffs = np.polyfit(means_sorted, energy_sorted, 2)
    y_model = np.polyval(quadratic_fit_coeffs, means_sorted)
    a, b, c = quadratic_fit_coeffs
    
    # the quadratic equation
    equation = f"y = {a:.4f}x^2 + {b:.4f}x + {c:.4f}"

    detector_name = input("input the name of the detector bring calibrated:",)
    
    # Plot means vs known energies from the predefined dictionary arrays
    fig, ax =plt.subplots(figsize=(5,5))
    ax.plot(means_sorted, energy_sorted, 'o')
    ax.errorbar(means_sorted, energy_sorted, xerr = err_means_sorted, fmt = 'o', ecolor = 'b', capsize = 2)
    ax.plot(means_sorted, y_model, 'r--', label='Quadratic best fit')
    ax.set_ylabel('Known Peak Energy (keV)')
    ax.set_xlabel('Channel')
    ax.set_title(f'Calibration Curve for {detector_name}')
    ax.legend()
    plt.text(0.2, 0.1, equation , fontsize = 10,  transform=ax.transAxes)
    plt.show()

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("Output_Filename", type=str, help="the name of the output file from spectramodelfitting.py ")
    return parser.parse_args()

if __name__ == "__main__":
    arguments = parse_arguments()
    main(arguments.Output_Filename)