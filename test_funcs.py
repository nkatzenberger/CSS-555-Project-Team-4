import pytest
from main import index
from flask import  render_template, Flask
from flask_cors import CORS
from BaseExample import processes
import scipy.io
import numpy as np
import h5py


def test_():
    app = Flask(__name__, template_folder='.', static_folder='.', static_url_path='')
    CORS(app)  # Enable CORS for all routes in Flask app
    app.route('/')
    render_template('index.html')
    assert index() == True

def test_inputreshape():
    dataset =scipy.io.loadmat("evoked_eeg_LA.mat")
    test_input = dataset['eeg'].T
    matfile = h5py.File('BaseExample/data/eeg_maptable.mat')
    maptable = matfile['maptable'][()].T
    print(maptable.shape)
    x = max(maptable[:, 0]) + 1
    y = max(maptable[:, 1]) + 1
    data_num = test_input.shape[0]
    temp_matrix = np.zeros((data_num, int(x), int(y)))
    for index in range(maptable.shape[0]):
            i = maptable[index, 0]
            j = maptable[index, 1]
            value = maptable[index, 2]
            temp_matrix[:, int(i), int(j)] = test_input[:, int(value)]
    assert processes.input_reshape(test_input, 'BaseExample/data/eeg_maptable.mat') == True

def test_min_max():
    dataset = scipy.io.loadmat("evoked_eeg_LA.mat")
    data = dataset['eeg'].T
    data_min = np.min(data, axis=1)
    data_max = np.max(data, axis=1)
    data_min = np.expand_dims(data_min, axis=1)
    data_max = np.expand_dims(data_max, axis=1)

    data_min = np.tile(data_min, (1, data.shape[1]))
    data_max = np.tile(data_max, (1, data.shape[1]))
    data_normalized = np.divide(data - data_min, data_max - data_min)
    assert processes.max_min_normalize(data) == True

