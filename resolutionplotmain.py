import calibrationcalculation as calcalc
import matplotlib.pyplot as plt
import argparse

# function to plot the resolution vs energy along with fitted relationship model
def resolution_plot(output_file):

    # call relevant data
    energy_sorted, resolution, y_model, err_resolution, energy_array = calcalc.resolution_calculation(output_file)
    detector_name = input("input the name of the detector bring calibrated:",)
    
    # plot resolution vs energy for the measured peaks and the fitted R-squared model
    plt.figure(figsize=(7, 5))
    plt.plot(energy_sorted, resolution, 'ro', label='Resolution = dE / E' )
    plt.errorbar(energy_sorted, resolution, yerr = err_resolution, fmt = 'ro', ecolor = 'r', capsize = 5)
    plt.plot(energy_array, y_model, label='R-squared model', color='blue')
    plt.xlabel('Energy (keV)')
    plt.xscale('log')
    plt.yscale('log')
    plt.ylabel('Resolution')
    plt.title(f'Variation of Resolution with Energy: {detector_name}')
    plt.legend()
    plt.grid(True)
    plt.show()


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("Output_Filename", type=str, help="the name of the output file from spectramodelfitting.py ")
    return parser.parse_args()

if __name__ == "__main__":
    arguments = parse_arguments()
    resolution_plot(arguments.Output_Filename)