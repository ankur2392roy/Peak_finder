#%%

#The program for peak finder
import numpy as np
from scipy.signal import find_peaks, peak_prominences, argrelextrema
import matplotlib.pyplot as plt
from astropy.modeling import models, fitting
import os
from peak_finder import significant_peaks, plot_peaks


unique_species, all_positions  = significant_peaks('HD209458b_syn_data.dat','Table_rev.txt',5)


file = 'HD209458b_syn_data.dat'

wav_data = np.loadtxt(file, unpack=True,usecols=0)
data    = np.loadtxt(file, unpack=True,usecols=1)
err_data = np.loadtxt(file, unpack=True,usecols=2)
fig, ax = plot_peaks(unique_species, all_positions, data, wav_data, err_data)

# %%
