import matplotlib.pyplot as plt
import argparse 
import inteffcalculation as inteff

# function to plot the intrinsic efficiency vs energy
def intrinsic_eff_plot(calibration_filename, output_file):

    # call the data
    energy_sorted, intrinsic_efficiency, inteff_error, energy, efficiency_model = \
        inteff.intrinsic_eff_calculation(calibration_filename, output_file)
    
    # user input detector name for the plot title
    detector_name = input("input the name of the detector bring calibrated:",)
    
    # plot the datapoints for the peaks and a quadratic best fit model
    plt.figure(figsize=(7, 5))
    plt.scatter(energy_sorted, intrinsic_efficiency, label='Intrinsic efficiency', color='red')
    plt.errorbar(energy_sorted, intrinsic_efficiency, yerr = inteff_error, fmt = 'o', ecolor = 'b', capsize = 10)
    plt.plot(energy, efficiency_model, 'r--', label='Quadratic best fit')
    plt.xlabel('Energy (keV)')
    plt.ylabel('Intrinsic \n Efficiency')
    plt.title(f'Variation of Intrinsic Efficiency with Energy: {detector_name}')
    plt.xscale('log')
    plt.yscale('log')
    plt.legend()
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