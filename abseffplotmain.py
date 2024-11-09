import abseffcalculation as abseff
import matplotlib.pyplot as plt
import argparse 


# function to plot the absolute efficiency vs energy for given photopeaks
def absolute_eff(calibration_filename, output_file):

    # calculate the absolute efficiency for the given peaks
    absolute_efficiency, energy_sorted, abseff_error = abseff.calc_absolute_eff(calibration_filename, output_file)
    detector_name = input("input the name of the detector bring calibrated:",)
    # plot the graph
    plt.figure(figsize=(7, 5))
    plt.scatter(energy_sorted, absolute_efficiency*100, color='red')
    plt.errorbar(energy_sorted, absolute_efficiency*100, yerr = abseff_error*100, fmt = 'o', ecolor = 'b', capsize = 7)
    plt.xlabel('Energy (keV)')
    plt.ylabel('Absolute \n Efficiency (%)')
    plt.title(f'Absolute Efficiency vs Energy: {detector_name}')
    plt.grid(True)
    plt.show()


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("Output_Filename", type=str, help="the name of the output file from spectramodelfitting.py ")
    parser.add_argument("Calibration_Filename", type=str, help="The name of the file containing calibration data for the sources.")
    return parser.parse_args()

if __name__ == "__main__":
    arguments = parse_arguments()
    absolute_eff(, arguments.Calibration_Filename, arguments.Output_Filename)
