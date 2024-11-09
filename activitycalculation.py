import numpy as np
import pandas as pd
import spectrumplot as sp

# function to return the half life for a given source
def call_half_life(key):

    # create a dictionary of half-lives
    source_halflives = {
    'Cs': np.array([30.09]),
    'Am': np.array([432.2]),
    'Ba': np.array([10.537]),
    '60-Co': np.array([5.2714])}

    # call one based on its source element
    half_life = source_halflives[key]

    # return the value of the half life as a string
    return half_life[0]

# function that calculate the current activity for a source 
# takes collection date, data containing calibration date
def activty_calculation(collection_date, data, key, filename):

    # import the time conversion classmethod
    from datetime import datetime

    # loop over each 
    for entry in data:
        calibration_time = datetime.strptime(entry['Reference Time'], '%Y-%m-%d %H:%M:%S GMT')
        if 'Spe' in filename:
            collection_time = datetime.strptime(collection_date, '%m/%d/%Y %H:%M:%S')
        elif 'mca' in filename:
            collection_time = datetime.strptime(collection_date, ' %m/%d/%Y %H:%M:%S')
        
        # Calculate the time difference in years
        time_difference_years = (collection_time - calibration_time).days / 365.25
        
        # half life and decay constant for the source
        half_life_years = float(call_half_life(key)) # Half-life in years for Americium-241
        decay_constant = np.log(2) / half_life_years  # Decay constant λ
        
        # Initial activity from the dictionary
        calibration_activity = entry['Activity uCi']
        
        # Calculate current activity using the decay formula
        current_activity = calibration_activity * np.exp(-decay_constant * time_difference_years)
    
    return current_activity


# function to extract the data from the file containing 
# the calibration info for the sources
def get_calibration_data(filename):
    data = pd.read_csv(filename, skipinitialspace=True, skiprows = 4)
    
    # Convert the DataFrame to a dictionary
    data_dict = data.to_dict(orient='records')

    return data_dict

# another function to return the source element from a given file 
# differs from the first function by handling filenames of a different convention.

def discern_element2(filename):
    if 'Caesium' in filename:
        return 'Cs'
    elif 'Barium' in filename:
        return 'Ba'
    elif 'Cobalt' in filename:
        return '60-Co'
    elif 'Americium' in filename:
        return 'Am'
    return None

# function to calculate and return the present activity for a given source


def present_activty(filename, sourcedatafilename):

    # extract the calibration data from input file
    calibration_data = sp.get_calibration_data(sourcedatafilename)

    # extract the collection data from input file dependent on the detector used
    if 'Spe' in filename:
         expt_info, exp_time = sp.expt_info_extraction_spe(filename)
    elif 'mca' in filename:
         expt_info, exp_time = sp.expt_info_extraction_mca(filename)

    # extract the collection date and the source element used
    collection_date = expt_info.iloc[0,0]
    key = discern_element2(filename)

    # if statemetnt failsafe in case discern_element2 returned NONE
    if key:
        # this code filters the dictionary to only leave the entry with the identified source
        data = [entry for entry in calibration_data if key in entry['# Nuclide']]

    # send the source calibration info and the collection date to the activity calculation function
    current_activity = activty_calculation(collection_date, data, key, filename)

    #print(f"Calibrated Activity: {initial_activity:.4f} uCi for measurement date: {reference_time}")
    #print(f"Current Activity: {current_activity:.4f} uCi for measurement date: {collection_date}")

    # return the present activity and the source name
    return current_activity, key, collection_date