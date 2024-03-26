# Run this in order to generate the brain images using data

# from BaseExample import data_preprocessing, main
import scipy.io
import pandas as pd

# if __name__ == "__main__":
#     exec(open("data_preprocessing.py").read())
#     exec(open("main.py").read())
def convertToBB(filename):
    mat = scipy.io.loadmat("./BaseExample/result/sample/Test_result_evoked_"+filename[19:])
    mat_variable = mat['s_pred']
    df = pd.DataFrame(mat_variable)
    single_col_df = df.stack().to_frame()
    single_col_df = df.to_string(index=False, header=False)
    file = open("converted.txt", "w")
    file.write(str(single_col_df))
    file.close
