#!/usr/bin/env python
# coding: utf-8

# # 1. Raw Data Preprocess

# ## 1.1 Load raw.fif data

# In[1]:


import os
import scipy.io as sio
import mne
from mne.datasets import sample


# In[2]:


"""
set data path (load sample data from MNE)
"""
data_path = sample.data_path()
raw_fname = data_path / 'MEG' / 'sample' / 'sample_audvis_filt-0-40_raw.fif'
raw = mne.io.read_raw_fif(raw_fname, preload=True)


# ## 1.2 data filtering

# In[3]:


"""
set low frequency & high frequency
"""
l_freq, h_freq = 1, 30
raw.filter(l_freq, h_freq, method='fir', fir_design='firwin')


# ## 1.3 data resampling

# In[4]:


"""
set resample frequency
"""
sfreq_resample = 480
raw = raw.resample(sfreq_resample)


# ## 1.4 plot events

# In[5]:


"""
get events
"""
events = mne.find_events(raw, stim_channel="STI 014")


# In[6]:


"""
set events id (for mne sample data, we ignore event 5 & 32)
"smiley": 5
"buttonpress": 32
"""
# LA: auditory/left
# RA: auditory/right
# LV: visual/left
# RV: visual/right
event_dict = {
    "LA": 1,
    "RA": 2,
    "LV": 3,
    "RV": 4,
}


# In[7]:


"""
plot events distribution
"""
fig = mne.viz.plot_events(
    events, sfreq=raw.info["sfreq"], first_samp=raw.first_samp, event_id=event_dict
)


# In[8]:


"""
plot events with raw data
"""
fig = raw.plot(
    events=events,
    start=5,
    duration=10,
    color="gray",
    event_color={1: "r", 2: "g", 3: "b", 4: "m", 5: "y", 32: "k"}, # set color according to events id
)


# ## 1.5 get averaged EEG data for each task

# In[9]:


# choose event id from [1, 2, 3, 4] or ["LA", "RA", "LV", "RV"]
event_id = 'LA'

# set path to save data
path = './data/real_data/'
if not os.path.exists(path):
    os.makedirs(path)
fig_name = path + 'evoked_eeg_'+str(event_id)+'.png'
mat_name = path + 'evoked_eeg_'+str(event_id)+'.mat'


# In[10]:


# fix
tmin = -0.1  # start of each epoch (100ms before the event)
tmax = 0.4  # end of each epoch (400ms after the event)
raw.info['bads'] = ['MEG 2443', 'EEG 053']
baseline = (None, 0)  # means from the first instant to t = 0
reject = dict(grad=4000e-13, mag=4e-12, eog=150e-6)
picks = mne.pick_types(raw.info, meg=True, eeg=True, eog=True, exclude='bads')
epochs = mne.Epochs(raw, events, event_dict, tmin, tmax, proj=True,
                    picks=picks, baseline=baseline, reject=reject)
epoch_use = epochs[event_id]
evoked_use = epoch_use.average()


# In[11]:


fig = evoked_use.plot_topomap(times=[0.0, 0.08, 0.1, 0.12, 0.2], ch_type="eeg")
fig.savefig(fig_name, dpi=300, bbox_inches='tight')


# In[12]:


data = evoked_use.data[:, :]
sio.savemat(mat_name, {'eeg': data})


# In[ ]:




