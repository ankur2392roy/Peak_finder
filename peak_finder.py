import numpy as np
from scipy.signal import find_peaks, peak_prominences, argrelextrema
import matplotlib.pyplot as plt
from astropy.modeling import models, fitting
import os


def significant_peaks(file,template_file,snr_threshold):
    
    wave              = np.loadtxt(file, unpack=True,usecols=0)
    transit_depth     = np.loadtxt(file, unpack=True,usecols=1)
    transit_depth_err = np.loadtxt(file, unpack=True,usecols=2)

    peaks   = find_peaks(transit_depth)
    rel_min = argrelextrema(transit_depth,np.less)[0]
    indices = peaks[0]

    prominence = peak_prominences(transit_depth,indices)
    peak_prominence = prominence[0]

    snr = peak_prominence/transit_depth_err[indices]

    significant_peaks = []
    line_center  = []
    significant_peaks_error = []
    wave_left = []
    wave_right = []

    for i in range(len(indices)):
        if snr[i] >= snr_threshold:
            significant_peaks.append(transit_depth[indices[i]])
            line_center.append(wave[indices[i]])
            significant_peaks_error.append(transit_depth_err[indices[i]])
            wave_left.append(wave[rel_min[i]])
            wave_right.append(wave[rel_min[i+1]])
        
    

    mean_values=[]
    stddev_values=[]
    for i in range(len(line_center)):
        amp=significant_peaks[i]
        per=line_center[i]
        

        x=[]
        y=[]
        for j in range(len(wave)):
            if wave[j] >= wave_left[i] and wave[j] <= wave_right[i]:
                x.append(wave[j])
                y.append(transit_depth[j])


        gg_init = models.Gaussian1D(amp, per,1)
        fitter = fitting.LevMarLSQFitter()
        gg_fit = fitter(gg_init, x, y)
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
                if k-l <= i <= k+l:
                    if j not in species and i not in identifier:
                        print('found', j)
                        species.append(j)
                        identifier.append(i)

        #print(species)
        with open(path+'/'+'output.txt','w') as f:
            for x,y in zip(species,identifier):
                f.write('{} is present at {} microns \n'.format(x,y))

        with open(path+'/'+'statistics_output.txt','w') as f:
            for x,y in zip(mean_values,stddev_values):
                f.write('Mean   Standard_deviation \n')
                f.write('{} {} \n'.format(x,y))
                f.write(" ")

    return significant_peaks,line_center
