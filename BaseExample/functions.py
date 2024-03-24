#!/usr/bin/env python
# coding: utf-8

# In[1]:


import warnings
warnings.simplefilter(action='ignore')
import scipy.io as sio
import scipy.io
import os
import sklearn
from sklearn import preprocessing
import numpy as np
import h5py
import torch
import torch.nn as nn
import torchvision
import torchvision.transforms as transforms
from torch.autograd import Variable
import torch.nn.init
from torch.utils.data import Dataset, DataLoader
import mne
from mne.datasets import sample
import argparse
from argparse import ArgumentParser
from matplotlib import pylab as plt

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
# print('==================================== device:', device, '====================================')


# In[2]:


def max_min_normalize(data):
    data_min = np.min(data, axis=1)
    data_max = np.max(data, axis=1)
    data_min = np.expand_dims(data_min, axis=1)
    data_max = np.expand_dims(data_max, axis=1)

    data_min = np.tile(data_min, (1, data.shape[1]))
    data_max = np.tile(data_max, (1, data.shape[1]))

    # data_normalized = (data - data_min) / (data_max - data_min)
    data_normalized = np.divide(data - data_min, data_max - data_min)
    return data_normalized


# In[3]:


def input_reshape(data, fname):
    """
    change vector of EEG/MEG data to matrix.
    for ConvDip input
    """
    # load map...................
    matfile = h5py.File(fname)
    maptable = matfile['maptable'][()].T
    print(maptable.shape)
    x = max(maptable[:, 0]) + 1
    y = max(maptable[:, 1]) + 1
    data_num = data.shape[0]
    temp_matrix = np.zeros((data_num, int(x), int(y)))
    for index in range(maptable.shape[0]):
        i = maptable[index, 0]
        j = maptable[index, 1]
        value = maptable[index, 2]
        temp_matrix[:, int(i), int(j)] = data[:, int(value)]
    return temp_matrix


# In[4]:


class RandomDatasetSingle(Dataset):
    def __init__(self, x_data, y_data, length):
        self.x_data = x_data.reshape((x_data.shape[0], 1, x_data.shape[1], x_data.shape[2]))
        self.y_data = y_data
        self.len = length

    def __getitem__(self, index):
        x_batch = torch.Tensor(self.x_data[index, :, :, :]).float()
        y_batch = torch.Tensor(self.y_data[index, :]).float()
        return x_batch, y_batch, index

    def __len__(self):
        return self.len


# In[5]:


class ConvDipSingleCatAtt(torch.nn.Module):
    def __init__(self, channel_num=1, output_num=1984, conv1_num=8, fc1_num=792, fc2_num=500):
        super(ConvDipSingleCatAtt, self).__init__()
        self.cnn = torch.nn.Sequential(
            torch.nn.Conv2d(channel_num, conv1_num, kernel_size=3, stride=1, dilation=1, padding=1),
            torch.nn.ReLU(),
            torch.nn.MaxPool2d(kernel_size=3, stride=1, padding=1),
            )
        # Squeeze-and-Excitation module
        self.SE = torch.nn.Sequential(
            torch.nn.Linear(8, 4),
            torch.nn.ReLU(),
            torch.nn.Linear(4, 8),
            torch.nn.Sigmoid(),
        )
        self.classifier = torch.nn.Sequential(
            torch.nn.Linear(fc1_num, fc2_num, bias=True),
            torch.nn.ReLU(),
            torch.nn.Linear(fc2_num, output_num, bias=True)
            )

    def forward(self, x):
        out = self.cnn(x)
        out = out.view(out.size(0), out.size(1), -1)
        squeeze = torch.mean(out, dim=2)
        excitation = self.SE(squeeze)
        excitation = excitation.unsqueeze(2)
        scale_out = torch.mul(out, excitation)
        flat_out = out.view(scale_out.size(0), -1)
        final_out = self.classifier(flat_out)
        return final_out


# In[6]:


def ConvDip_ESI(task_id, result_path):
    """
    EEG source imaging with ConvDip framework
    task_id: str or list ['LA', 'RA', 'LV', 'RV']
    result_path: path to model output
    """
    data_name = 'sample'
    map_dir = './data/eeg_maptable.mat'
    
    model_flag = 'real_model'
    model_dir = './model/' + data_name + '/' + model_flag
    
    test_data_dir = './data/real_data/'
    # result_dir = './result/' + data_name + '/' + model_flag
    result_dir = result_path + '/' + data_name
    if not os.path.exists(result_dir):
        os.makedirs(result_dir)

    # data: EEG/MEG & source
    # size: (dim, nsample)

    if isinstance(task_id, str):
        # print('type of task id: str')
        task_set = [task_id]
    elif isinstance(task_id, list):
        # print('type of task id: list')
        task_set = task_id
    else:
        raise Exception("Oops! That was not a valid type for task id. Try use 'str' or 'list'!")
    
    for run in task_set:
        print('processing task:',str(run))
        
        if not run in ['LA', 'RA', 'LV', 'RV']:
            raise Exception("Oops! That was not a valid task id. Try use 'LA', 'RA', 'LV' or 'RV'!")
        else:
            data_mat = test_data_dir + '/evoked_' + 'eeg' + '_' + str(run) + '.mat'
            result_mat = result_dir + '/Test_result_' + 'evoked_' + str(run) + '.mat'
        
            # load the real dataset
            dataset = scipy.io.loadmat(data_mat)
            test_input = dataset['eeg'].T
            
            # print("data normalization:")
            test_input = max_min_normalize(test_input)
        
            # change to [timepoint, 12, 14]:
            test_input_matrix = input_reshape(test_input, map_dir)
        
            # print('check input matrix shape:')
            # print(test_input_matrix.shape)  # (166560, 9, 11)
            
            # get the number of samples:
            ntest = test_input_matrix.shape[0]
            test_output = test_input ##################################################################################
        
            # change to [timepoint, 1, 12, 14]:
            RandomDataset_test = RandomDatasetSingle(test_input_matrix, test_output, ntest)
            rand_loader_test = DataLoader(dataset=RandomDataset_test, batch_size=ntest, num_workers=0,
                                           shuffle=False)
        
            # Build model: Model_EEG
            model = ConvDipSingleCatAtt()
        
            model = model.to(device)
            # load pretrained model...
            model.load_state_dict(torch.load('%s/net_params_best.pkl' % (model_dir)))
            # model prediction...
            model.eval()
            with torch.no_grad():
                for data in rand_loader_test:
                    batch_X_eeg, _, _ = data
                    batch_X_eeg = batch_X_eeg.to(device)
        
                    X_eeg = Variable(batch_X_eeg)
        
                    # forward propagation
                    Y_pred = model(X_eeg)
                    Y_pred = Y_pred.cpu().detach().numpy().T
        
            # ================== save test result: ==================
            sio.savemat(result_mat, {'s_pred': Y_pred})
            print("result saved in: " + result_mat)
            # print("======== test finished!! ========")
        
        # print("\n")
        # print('===================== Test Finished! =========================')
    


# In[7]:


def load_result(task, result_path):
    if not isinstance(task, str):
        raise Exception("Oops! That was not a valid type for task. Try type a 'str'!")

    if not task in ['LA', 'RA', 'LV', 'RV']: 
        raise Exception("Oops! That was not a valid task. Try use 'LA', 'RA', 'LV' or 'RV'!")
    else:
        print("load result for task: {}".format(task))
        fname = result_path + '/sample/Test_result_evoked_' + str(task) + '.mat'
        dataset = sio.loadmat(fname)
        s_pred = dataset['s_pred']
        s_pred = np.absolute(s_pred)
        if s_pred.shape[0]!=1984:
            s_pred = s_pred.T
   
    return s_pred
    


# In[ ]:




