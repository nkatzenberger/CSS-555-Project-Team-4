from flask import Flask, request, render_template
from flask_cors import CORS
import os
#from BaseExample import model

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
    return 'File uploaded successfully'

if __name__ == '__main__':
    app.run(debug=True, port=8000)

