from main import index
from flask import  render_template
from BaseExample import processes
import scipy.io
import numpy as np
import h5py


def test_index():
    assert index() == render_template('index.html')

def test_inputreshape():
    mat =scipy.io.loadmat("evoked_eeg_LA.mat")
    matfile = h5py.File('BaseExample/data/eeg_maptable.mat')
    maptable = matfile['maptable'][()].T
    print(maptable.shape)
    x = max(maptable[:, 0]) + 1
    y = max(maptable[:, 1]) + 1
    data_num = mat.shape[0]
    temp_matrix = np.zeros((data_num, int(x), int(y)))
    for index in range(maptable.shape[0]):
            i = maptable[index, 0]
            j = maptable[index, 1]
            value = maptable[index, 2]
            temp_matrix[:, int(i), int(j)] = mat[:, int(value)]
    assert processes.input_reshape(mat, 'BaseExample/data/eeg_maptable.mat') == temp_matrix

def test_addition():
    assert 1+1 ==2
