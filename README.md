# peak_finder
This package is intended to identify known spectral signatures from a given exoplanet atmospheric tramsmission spectrum and produce them as results.
It is helpful to give a primary estimate of the lines present in a spectrum where the Signal-to-Noise ratio of the data can be user defined, without manual intervention.

## Outputs

1. A file called output.txt listing all the elements (or species) found in the spectra at their respective wavelengths.
2. A file called statistics_output.txt listing the results from Gaussian fits to individual significant peaks in the signal.
3. Plot with identified peaks in the spectrum.

## Installation instructions

After cloning the repository, run this:

```pip install -r requirements.txt -e .```

## Example Notebook 

After installing the package, you can refer to the notebook inside docs/tutorial for an example implementation of ```peak_finder```. 

[ipython notebook](https://github.com/ankur2392roy/Peak_finder/blob/main/docs/tutorial/tutorial.ipynb)