import spectrumplot as sp
import argparse 

def main(filename): 
    data_cps_array, channels, expt_info = sp.plot_spectrum(filename)

    # print the dataframe with the collection date and exposure time
    print(expt_info)


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("Spectrum_Filename", type=str, help="the name of the .spe or .mca datafile ")
    return parser.parse_args()

if __name__ == "__main__":
    arguments = parse_arguments()
    main(arguments.Spectrum_Filename)