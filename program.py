#The program for peak finder
import numpy as np
from scipy.signal import find_peaks, peak_prominences
import matplotlib.pyplot as plt
from lmfit import Model
from astropy.modeling import models, fitting
import os

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

	return line_center,l_base,r_base,significant_peaks


l_base = significant_peaks('HD.txt',10)[1]
r_base = significant_peaks('HD.txt',10)[2]
line_center = significant_peaks('HD.txt',10)[0]
significant_peaks = significant_peaks('HD.txt',10)[3]



def peak_identifier(template_file):
	mean_values=[]
	stddev_values=[]
	for i in range(len(l_base)):
		amp=significant_peaks[i]
		per=line_center[i]
		a = np.logical_and(wave >= l_base[i], wave <= r_base[i])
		k=np.where(a)[0]
		x=wave[k[0]:k[-1]]
		y=significant_peaks[k[0]:k[-1]]
		gg_init = models.Gaussian1D(amp, per, 1)
		fitter = fitting.SLSQPLSQFitter()
		gg_fit = fitter(gg_init, x, y)
		print(gg_fit.mean.value,gg_fit.stddev.value)
		mean_values.append(gg_fit.mean.value)
		stddev_values.append(gg_fit.stddev.value)

		path=os.getcwd()
		with open(path+'/'+template_file,'r') as f:
			wavelength=[]
			name=[]
			header=f.readline()
			for line in f:
				line=line.strip().split()
				x=line[0]
				y=float(line[1])
				name.append(x)
				wavelength.append(y)

		species=[]
		identifier=[]
		for i,j in zip(wavelength,name):
			for k,l in zip(mean_values,stddev_values):
				if i-k <= wavelength <= i+k:
					print('found')
					species.append(j)
					identifier.append(i)

 		#print(species)
		with open(path+'/'+'output.txt','w') as f:
			for x,y in zip(species,identifier):
				f.write('{} is present at {} microns \n'.format(x,y))


significant_peaks('HD.txt',10)
#peak_identifier('test.txt')
