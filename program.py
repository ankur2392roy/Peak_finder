#The program for peak finder
import numpy as np
from scipy.signal import find_peaks, peak_prominences, argrelextrema
import matplotlib.pyplot as plt
from astropy.modeling import models, fitting
import os
from peak_finder import significant_peaks


p = significant_peaks('HD209458b_syn_data.dat','Table_rev.txt',5)



