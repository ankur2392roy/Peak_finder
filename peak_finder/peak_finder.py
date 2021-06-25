import numpy as np
from scipy.signal import find_peaks, peak_prominences, argrelextrema
import matplotlib.pyplot as plt
from matplotlib import cm
from astropy.modeling import models, fitting
import os


def significant_peaks(file,template_file,snr_threshold):
    '''Function to detect significant features of pre-tabulated molecules in transmission
       spectroscopy data

    Parameters
    ----------
    file: str
        name of the input file
    template_file: str
        name of the file that contains a list of molecular features, with columns
        'Species' and 'Wavelength (microns)'
    snr_threshold: float
        SNR threshold for a feature to be flagged as significant

    Returns
    -------
    unique_species: list of str
        list of species names that have been detected
    all_positions: list of lists
        list of wavelength positions of detected features of all species
    '''
    
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
                
                    #print('found', j)
                species.append(j)
                identifier.append(i)

    # extract all unique molecules and all their wavelength positions

    unique_species = list(set(species))
    all_positions = []

    for unique_spec in unique_species:
        positions = []
        for i in range(len(species)):
            if species[i] == unique_spec:
                positions.append(identifier[i])
        all_positions.append(list(set(positions)))   


    #print(species)
    with open(path+'/'+'output.txt','w') as f:
        for x,y in zip(unique_species,all_positions):
            f.write('{} is present at {} microns \n'.format(x,y))

    with open(path+'/'+'statistics_output.txt','w') as f:
        f.write('Mean   Standard_deviation \n')
        for x,y in zip(mean_values,stddev_values):                
            f.write('{} {} \n'.format(round(x,4),round(y,4)))
            #f.write(" ")    

    return unique_species, all_positions 


def plot_peaks(species_list, positions_list, data, wav_data, err_data, num_features=None, save_fig=False):
    '''Function that plots all the peaks, molecules, and the data
     

    Parameters
    ----------

    species_list: list of str
        list of species that were identified in the data
    positions_list: list of lists
        wavelength positions corresponding all identified species
    data: numpy array
        the transmission spectrum
    wav_data: numpy array
        wavelength array for the data
    err_data: numpy array
        error-bar array for the data
    num_features (optional): int
        only show  

    Returns
    -------

    fig, ax: matplotlib.pyplot objects

    '''
    

    # create a color cycle for the species

    N = len(species_list)

    color=cm.rainbow(np.linspace(0,1,N))

    fig, ax = plt.subplots(figsize=(8,4))
    
    # plot data
    ax.errorbar(wav_data, data, yerr=err_data, color='black', label='data', marker='o', markersize=3, capsize=2, zorder=2, ls='none', 
    elinewidth=2,)

    # plot molecules and vertical lines for their positions
    #vline_counter = 0
    for i,c in enumerate(color):
        for j,position in enumerate(positions_list[i]):
            if j==0:
                ax.axvline(x=position, color=c, ls='--', alpha=0.5, label=species_list[i])
                #vline_counter += 1
            else:
                ax.axvline(x=position, color=c, ls='--', alpha=0.5)
                #vline_counter += 1
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles, labels, loc='center left', ncol=1, bbox_to_anchor=(1.01,0.5), fontsize=14)
    ax.set_xlabel('Wavelength ($\mu$m)')
    ax.set_ylabel('Transit depth')

    plt.tight_layout()
    #print(vline_counter)

    return fig, ax
            






