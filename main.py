from flask import Flask, request, render_template, make_response
from flask_cors import CORS
import os
from BaseExample import model
import scipy.io
import pandas as pd
from src.py.submit import uploadToFirebase
# Convert ConvDip data into brainbrowser format
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
    file = open("./data/converted.txt", "w")
    file.write(str(single_column_df))
    file.close()

# Get the absolute path to the project root directory
project_root = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__, template_folder='.', static_folder='.', static_url_path='')
CORS(app)  # Enable CORS for all routes in Flask app

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    # Handle the file as required (save, process, etc.)
    # For example, you can save the file:
    file.save(file.filename)
    task = file.filename[11:12]
    if(task== 'L'):
        model.runModel(file, ['LA', 'LV'], file.filename[11:13])
    elif(task== 'R'):
        model.runModel(file, ['RA', 'RV'], file.filename[11:13])
    else:
        model.runModel(file)
    convertToBB("output.mat")
    uploadToFirebase(file.filename)
    response = make_response('File uploaded successfully')
    response.headers['Access-Control-Allow-Origin'] = '*'  # Allow requests from any origin
    return response

@app.route('/loadFromList',methods=['GET'])
def loadFile():
    filename=request.args.get('filename')


if __name__ == '__main__':
    app.run(debug=True, port=8000)

