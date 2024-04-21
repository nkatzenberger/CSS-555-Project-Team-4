from flask import Flask, request, render_template, make_response
from flask_cors import CORS
import os
from BaseExample import model
import scipy.io
import pandas as pd
from src.py.submit import uploadToFirebase
from firebase_admin import storage
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
    f = open("./textdocs/emails.txt", "r")
    email = f.readline()
    uploadToFirebase(file.filename, email)
    file.save(file.filename, email)
    task = file.filename[11:12]
    if(task== 'L'):
        model.runModel(file, ['LA', 'LV'], file.filename[11:13])
    elif(task== 'R'):
        model.runModel(file, ['RA', 'RV'], file.filename[11:13])
    else:
        model.runModel(file)
    convertToBB("output.mat")
    response = make_response('File uploaded successfully')
    response.headers['Access-Control-Allow-Origin'] = '*'  # Allow requests from any origin
    return response

@app.route('/loadFromList',methods=['GET'])
def loadFile():
    filename=request.args.get('filename')
    foldername=request.args.get('foldername')

    #make a firebase request for the file
    bucket = storage.bucket()
    blob = bucket.blob(foldername+"/"+filename)

    downloadDirectory = os.path.join(os.path.dirname(__file__), 'data','loadedFileFromUserList.mat')

    blob.download_to_filename(downloadDirectory)
    # Use the downloaded file to run all of the model functions
    task = filename[11:12]  # Extract task from the filename
    if task == 'L':
        model.runModel(downloadDirectory, ['LA', 'LV'], filename[11:13])  # Pass the downloaded file
    elif task == 'R':
        model.runModel(downloadDirectory, ['RA', 'RV'], filename[11:13])  # Pass the downloaded file
    else:
        model.runModel(downloadDirectory)  # Pass the downloaded file

    convertToBB("output.mat")
    uploadToFirebase(filename)
    response = make_response('File uploaded successfully')
    response.headers['Access-Control-Allow-Origin'] = '*'  # Allow requests from any origin

    #let caller know that methods are done so it can be loaded into browser window
    return response

@app.route('/email',methods=['POST'])
def getEmail():
    email = request.args.get('value')
    textf = open("./textdocs/emails.txt", 'w')
    textf.write(email)


if __name__ == '__main__':
    app.run(debug=True, port=8000)

