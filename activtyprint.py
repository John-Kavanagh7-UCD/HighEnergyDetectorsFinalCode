import activitycalculation as ac
import argparse

def print_activity(filename, sourcedatafilename):
    current_activity, key, collection_date = present_activty(filename, sourcedatafilename)
    print(f"Current Activity: {current_activity:.4f} uCi for measurement date: {collection_date}")

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("Raw_Data_Filename", type=str, help="The name of the raw data file from the detector")
    parser.add_argument("Calibration_Filename", type=str, help="The name of the file containing calibration data for the sources.")
    return parser.parse_args()

if __name__ == "__main__":
    arguments = parse_arguments()
    print_activity(arguments.Raw_Data_Filename, arguments.Calibration_Filename)