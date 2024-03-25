#!/usr/bin/env python
# coding: utf-8

import functions
import brain



# # 1. Brain Source Localization with ConvDip

# In[1]:

exec(open("functions.py").read())


# In[2]:


"""
The subject underwent four tasks, and corresponding EEG data were collected.
task list: ['LA','LV','RA','RV']
"""
# you can choose single or multiple task ids from task list ['LA','LV','RA','RV']
tasks = ['LA', 'LV'] # or 'LA' or ['LA'], etc.
# set your result path
result_path = './result/'
ConvDip_ESI(tasks, result_path)


# In[3]:


# choose only ONE task from ['LA','LV','RA','RV']
task = 'LA' 
s_pred = load_result(task, result_path)
print(s_pred.shape) # s_pred: estimated sources at different timepoints


# # 2. 3D Visualization

# In[4]:


exec(open("brain.py").read())


# In[5]:


"""
hemi: Hemisphere id (ie ‘lh’, ‘rh’, ‘both’, or ‘split’). 
In the case of ‘lh’, only left hemisphere is shown in the window. 
In the case of ‘rh’, only right hemispheres is shown in the window. 
In the case of ‘both’, both hemispheres are shown in the same window. 
In the case of ‘split’ hemispheres are displayed side-by-side in different viewing panes.
"""

hemi='split' # choose from ['lh', 'rh', 'split', 'both']
brain3d(s_pred, hemi)


# In[ ]:




