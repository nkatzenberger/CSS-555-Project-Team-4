"""Module for converting data to BrainBrowser format."""
# Run this in order to generate the brain images using data

import scipy.io
import pandas as pd

def convertToBB(filename):
    # Construct the full file path
    file_path = "./result/sample/"+filename
    
    # Load data from the file
    matlab_file = scipy.io.loadmat(file_path)
    matlab_variable = matlab_file['s_pred']
    
    # Convert data to DataFrame
    df = pd.DataFrame(matlab_variable)
    
    # Convert DataFrame to a string
    single_column_df = df.stack().to_frame()
    single_column_df = df.to_string(index=False, header=False)
    
    # Write the string to a file
    file = open("converted.txt", "w")
    file.write(str(single_column_df))
    file.close()