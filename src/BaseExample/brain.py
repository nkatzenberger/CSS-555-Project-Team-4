#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
from pathlib import Path
import numpy as np
import scipy.io as sio
from PIL import Image
import h5py
import matplotlib.pyplot as plt
import mne
from mne.datasets import sample, fetch_fsaverage
from mne.beamformer import make_lcmv, apply_lcmv
from mpl_toolkits.axes_grid1 import (make_axes_locatable, ImageGrid,
                                     inset_locator)


# In[2]:


def get_stc():
    data_path = sample.data_path()
    subjects_dir = data_path / 'subjects'
    meg_path = data_path / 'MEG' / 'sample'
    raw_fname = meg_path / 'sample_audvis_filt-0-40_raw.fif'
    
    # Read the raw data
    raw = mne.io.read_raw_fif(raw_fname)
    raw.info['bads'] = ['MEG 2443']  # bad MEG channel
    
    # Set up the epoching
    event_id = 1  # those are the trials with left-ear auditory stimuli
    tmin, tmax = -0.2, 0.5
    events = mne.find_events(raw)
    
    # pick relevant channels
    raw.pick(['meg', 'eog'])  # pick channels of interest
    
    # Create epochs
    proj = False  # already applied
    epochs = mne.Epochs(raw, events, event_id, tmin, tmax,
                        baseline=(None, 0), preload=True, proj=proj,
                        reject=dict(grad=4000e-13, mag=4e-12, eog=150e-6))
    
    # for speed purposes, cut to a window of interest
    evoked = epochs.average().crop(0.05, 0.15)
    
    # Visualize averaged sensor space data
    # evoked.plot_joint()
    
    del raw  # save memory

    data_cov = mne.compute_covariance(epochs, tmin=0.01, tmax=0.25,
                                      method='empirical')
    noise_cov = mne.compute_covariance(epochs, tmin=tmin, tmax=0,
                                       method='empirical')
    # data_cov.plot(epochs.info)
    del epochs

    # Read forward model
    fwd_fname = './BaseExample/data/meg-fwd.fif'
    forward = mne.read_forward_solution(fwd_fname)

    filters = make_lcmv(evoked.info, forward, data_cov, reg=0.05,
                        noise_cov=noise_cov, pick_ori='max-power',
                        weight_norm='unit-noise-gain', rank=None)
    
    filters_vec = make_lcmv(evoked.info, forward, data_cov, reg=0.05,
                            noise_cov=noise_cov, pick_ori='vector',
                            weight_norm='unit-noise-gain-invariant', rank=None)
    
    # save a bit of memory
    src = forward['src']
    del forward

    stc = apply_lcmv(evoked, filters)
    stc_vec = apply_lcmv(evoked, filters_vec)
    del filters, filters_vec
    

    return stc


# In[3]:


def brain3d(s_pred, hemi):
    stc = get_stc()
    print(stc)
    stc.data = s_pred
    data_path = sample.data_path()
    subjects_dir = data_path / 'subjects'
    brain = mne.viz.plot_source_estimates(
            stc, 
            # views= #'lateral', 
            hemi=hemi, #'split', #'both', 
            surface='white', #'inflated'
            background='white',
            size=(1000, 400),
            subjects_dir=subjects_dir, 
            # time_viewer=False, 
            show_traces=False, 
            # colorbar=False,
            )
    


# In[ ]:




