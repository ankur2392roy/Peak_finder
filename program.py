#The program for peak finder
import numpy as np
from scipy.signal import find_peaks, peak_prominences, argrelextrema
import matplotlib.pyplot as plt
from astropy.modeling import models, fitting
import os
from peak_finder import significant_peaks, peak_identifier


p = significant_peaks('HD209458b_syn_data.dat',5)


line_center = p[0]
l_base = p[1]
r_base = p[2]

#print(line_center)
#print(l_base)
#print(r_base)

significant_peaks = p[3]
wave = p[4]
transit_depth = p[5]


#significant_peaks('HD.txt',10)
peak_identifier('Table.txt')
