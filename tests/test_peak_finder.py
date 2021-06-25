import numpy as np
from scipy.signal import find_peaks, peak_prominences, argrelextrema
import matplotlib.pyplot as plt
from astropy.modeling import models, fitting
import os
from peak_finder.peak_finder import significant_peaks, plot_peaks


def test_significant_peaks():
    #path = os.getcwd()
    #data_file = path +'/HD209458b_syn_data.dat'
    
    #data_file = os.path.abspath(os.path.join(os.path.dirname(__file__),'HD209458b_syn_data.dat'))
    #print(os.getcwd())
    #mol_table_file = os.path.abspath(os.path.join(os.path.dirname(__file__),'Table_test.txt'))
    data_file = 'tests/HD209458b_syn_data.dat'
    #mol_table_file = os.path.abspath(os.path.join(os.path.dirname(__file__),'Table_test.txt'))
    #print(mol_table_file)
    mol_table_file = 'tests/Table_test.txt'

    #data_file = os.path.abspath('HD209458b_syn_data.dat')
    #mol_table_file = os.path.abspath('Table_test.txt')

    snr=10

    unique_species, all_positions  = significant_peaks(data_file,mol_table_file,snr)

    assert unique_species[0] == 'H2O'
    assert all_positions[0][0] == 1.4234
