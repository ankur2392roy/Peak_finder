#The program for peak finder
import numpy as np 
from scipy.signal import find_peaks, peak_prominences
import matplotlib.pyplot as plt 


def significant_peaks(file,snr_threshold):
	#file = "HD209458b_syn_data.dat"
	#file = input("Enter the input spectrum with three cols (wavelength, transit depth, error on transit transit_depth): ")
	#snr_threshold = 10
	#snr_threshold = float(input("Enter snr threshold: "))
	wave              = np.loadtxt(file, unpack=True,usecols=0)
	transit_depth     = np.loadtxt(file, unpack=True,usecols=1)
	transit_depth_err = np.loadtxt(file, unpack=True,usecols=2)

	peaks = find_peaks(transit_depth)
	indices = peaks[0]
	prominence = peak_prominences(transit_depth,indices)
	peak_prominence = prominence[0]
	left_base = prominence[1]
	right_base = prominence[2]
	snr = peak_prominence/transit_depth_err[indices]

	significant_peaks = []
	line_center  = []
	significant_peaks_error = []
	l_base = []
	r_base = []
	for i in range(len(indices)):
		if snr[i] >= snr_threshold:
			significant_peaks.append(transit_depth[indices[i]])
			line_center.append(wave[indices[i]])
			significant_peaks_error.append(transit_depth_err[indices[i]])
			l_base.append(wave[left_base[i]])
			r_base.append(wave[right_base[i]])

	return line_center,l_base,r_base


significant_peaks('HD209458b_syn_data.dat',10)