import pandas as pd
import numpy as np

#user story: As a user, I expect the program to remove any faulty data in my uploaded data set like repeats or nan values.

class CleanData():

    def preClean(input):

        df = input

        df = df.drop_duplicates()
        df = df.fillna(0)
        df= df.reset_index(drop=True,allow_duplicates=False)
        output = df
        return output
    
