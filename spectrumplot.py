import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 


# function that opens the .mca datafile,
# takes a user input to set the area of the datafile where the spectral 
# data starts and ends, extracts the data into an array and 
# normalises the data by dividing by the exposure time of that recording. 
def extract_cps_data(filename, exp_time):
    
    # initialise lists and binary condition as false
    data_counts = [] 
    data_cps = []
    extract = False

    # take user input to set the start and end lines of the spectral data
    start_of_data = input("input the line in the datafile immediately \
before the numerical spectrum data begins:",)
    end_of_data = input("input the line in the datafile immediately \
after the numerical spectrum data ends:",)

    # open and read the file,
    # change the binary condition while inside the user-defined range
    # append the data to the initialised list
    with open(filename, 'r') as file:  
            for line in file:
                if start_of_data in line:
                    extract = True
                    continue
                if end_of_data in line:
                    extract = False
                    continue
                if extract:
                    data_counts.append(int(line))

    # normalise the data extracted by dividing by exposure time
    # exposure time extracted in the 'expt_info_extraction_mca' function.
    for counts in data_counts:
        cps = float(counts)/float(exp_time[0])
        data_cps.append(cps)

    # convert the list to a numpy array
    data_cps_array = np.asarray(data_cps)

    # create an array of channels of the same length as the dataset
    channels = np.linspace(0,len(data_cps_array), len(data_cps_array))

    # return normalised data
    return data_cps_array, channels



# function to extract the exposure time and data collection date
def expt_info_extraction_spe(filename):

    # initialise the lists to store the data
    date_of_collection = []
    exp_time = []
    real_time = []

    # open the file and append the measurement date and time to lists
    with open(filename, 'r') as file:  
            for line in file:
                if "DATE_MEA" in line:
                    date_of_collection.append(next(file).strip())
                if "MEAS_TIM" in line:
                    real_time.append(next(file).strip())
                    real_time = real_time[0].split()[-1]
                    exp_time.append(float(real_time))


    # create a dictionary to store the data 
    date_and_time = {"Data Collection Date" : date_of_collection, 
                     "Exposure Time (Seconds)" : exp_time }              
    
    # convert the dictionary to a pandas dataframe for for readable output
    expt_info = pd.DataFrame(date_and_time)

    # return the pandas dataframe and the exposure time
    return expt_info, exp_time
        

# function to extract the exposure time and data collection date
def expt_info_extraction_mca(filename):

    # initialise the lists to store the data
    date_of_collection = []
    exp_time = []
    real_time = []

    # open the file and append the measurement date and time to lists
    with open(filename, 'r') as file:  
            for line in file:
                if "START_TIME" in line:
                    date_of_collection.append(line.strip().split('-')[-1])
                if "REAL_TIME" in line:
                    exp_time.append(line.strip().split('-')[-1])
                    
    
     # create a dictionary to store the data 
    date_and_time = {"Data Collection Date" : date_of_collection, 
                     "Exposure Time (Seconds)" : exp_time }              
    
    # convert the dictionary to a pandas dataframe for for readable output
    expt_info = pd.DataFrame(date_and_time)

    # return the pandas dataframe and the exposure time
    return expt_info, exp_time

# a function that completes all data extraction,
# data normalisaton and background subtraction
# for a single .spe file
# returns a dataframe of the data collection date and exposure time
# returns the exposure time as an integer
# returns the cps data and corresponding channels in arrays
def spe_data(filename, background_filename):

    # extract all relevant data from the given file
    expt_info, exp_time = expt_info_extraction_spe(filename)
    data_cps, channels = extract_cps_data(filename, exp_time)

    # extract the same data for the background
    expt_info_bground, exp_time_bground = \
expt_info_extraction_spe(background_filename)
    bground_data, bground_channels = \
extract_cps_data(background_filename, exp_time_bground)

    # subract the background 
    data_cps_array = data_cps - bground_data

    # return the data
    return expt_info, exp_time, data_cps_array, channels


# a function that completes all data extraction,
# data normalisaton and background subtraction
# for a single .mca file
# returns a dataframe of the data collection date and exposure time
# returns the exposure time as an integer
# returns the cps data and corresponding channels in arrays
def mca_data(filename):

    # extract all relevant data from the given file
    expt_info, exp_time = expt_info_extraction_mca(filename)
    data_cps_array, channels = extract_cps_data(filename, exp_time)

     # return the data
    return expt_info ,exp_time, data_cps_array, channels

# a function to take a file,
# assess its filetype 
# and call the relevant data extraction functions
def get_data(filename):
    
    # .spe files require background subtraction
    # user input required for background spectrum filename
    if 'Spe' in filename:
        background = str(input(
            "input the full filename of the background \
spectrum taken for the detector:",
        ))
        expt_info ,exp_time, data_cps_array, channels = \
spe_data(filename, background)
        
        
    # call relevant .mca functions if .mca file
    elif 'mca' in filename:
        expt_info, exp_time = expt_info_extraction_mca(filename)
        data_cps_array, channels = extract_cps_data(filename, exp_time)

    # return the data
    return data_cps_array, channels, exp_time, expt_info


# function to takes a file, runs the data extraction functions 
# plot the data and prints the collection date. 
def plot_spectrum(filename):
    # call the data extraction functions
    data_cps_array, channels, exp_time, expt_info = get_data(filename)

    # plot the spectrum 
    plt.figure(figsize=(7, 4))
    plt.plot(channels, data_cps_array)
    plt.title(f"Spectrum of:{str(filename)}")
    plt.xlabel("Channel")
    plt.ylabel("Counts/Second (CPS)")
    plt.xticks(np.arange(0,np.max(channels), np.max(channels)/10))
    plt.show()

    return data_cps_array, channels, expt_info