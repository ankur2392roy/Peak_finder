
Welcome to `peak_finder`'s documentation!
=========================================

This package is intended to identify known spectral signatures in a given exoplanet atmospheric tramsmission spectrum and print them out in a file. 

Why
+++

It is helpful to have an autmoted way to get an estimate of the possible molecules present in a spectrum. 
Usually, this step is performed by humans through visual ispection of spectra. 
The list of molecules identified by `peak_finder` can then be used to build models 
for `atmospheric retrievals <https://platon.readthedocs.io/en/latest/intro.html>`_ and other fitting exercises. 
`peak_finder` also allows the user to define a threshold Signal-to-Noise ratio for the features that should 
be detected in the data. The user can also add their own molecules to the table of features, and `peak_finder` 
will automatically include them in its analysis. 

Outputs
+++++++

1. A file called ```output.txt``` listing all the elements (or species) found in the spectra at their respective wavelengths.
2. A file called ```statistics_output.txt``` listing the results from Gaussian fits to individual significant peaks in the signal.
3. Plot with identified peaks in the spectrum.

Installation instructions
+++++++++++++++++++++++++

After cloning the repository, run this:

```pip install -r requirements.txt .```


User Guide:
+++++++++++
.. toctree::
   :maxdepth: 2

   tutorial