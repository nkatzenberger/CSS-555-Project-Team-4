#!/usr/bin/env python
# coding: utf-8
from BaseExample import processes
from BaseExample import brain
#from brain import brain3d


# # 1. Brain Source Localization with ConvDip

# In[1]:
def runModel(file=None, tasks = ['RV', 'RA'], task = 'RV'):
    #exec(open("./processes.py").read())
    # In[2]:
    """
    The subject underwent four tasks, and corresponding EEG data were collected.
    task list: ['LA','LV','RA','RV']
    """
    # you can choose single or multiple task ids from task list ['LA','LV','RA','RV']
    # set your result path
    # or 'LA' or ['LA'], etc.
    result_path = './result/'
    processes.ConvDip_ESI(tasks, result_path, file)
    # In[3]:
    # choose only ONE task from ['LA','LV','RA','RV']
    #task = 'LA' 
    s_pred = processes.load_result(task, result_path)
    print(s_pred.shape) # s_pred: estimated sources at different timepoints

    # # 2. 3D Visualization

    # In[4]:
    #exec(open("brain.py").read()) #only works in jupyter

    # In[5]:


    """
    hemi: Hemisphere id (ie ‘lh’, ‘rh’, ‘both’, or ‘split’). 
    In the case of ‘lh’, only left hemisphere is shown in the window. 
    In the case of ‘rh’, only right hemispheres is shown in the window. 
    In the case of ‘both’, both hemispheres are shown in the same window. 
    In the case of ‘split’ hemispheres are displayed side-by-side in different viewing panes.
    """
    """""
    hemi='split' # choose from ['lh', 'rh', 'split', 'both']
    brain.brain3d(s_pred, hemi)"""
