# pyIsotopomer

Hello!

pyIsotopomer is a Python toolbox for performing data corrections for N2O isotopomer data. Its core is a package of scripts to correct for scrambling in the ion source during isotope ratio mass spectrometry. An alternate version of this package exists for [MATLAB](https://link-to-MATLAB-README.md).

## Overview

In this document, we will go over:

1. Basic use of the pyIsotopomer package
2. Configuring Python on your computer
3. Correcting IRMS data for the effect of peak area on isotope ratios
4. Calibrating your instrument for scrambling with pyIsotopomer
5. Correcting raw Isodat files for isotopomers with pyIsotopomer

## Basic use

The import convention for pyIsotopomer is:

```
from pyIsotopomer import Scrambling, Isotopomers
```

To calculate scrambling coefficients, the only function you need is:

```
gk = Scrambling(inputfile='FILENAME.csv', ref1="NAME", ref2="NAME", **kwargs)
```

To calculate isotopomers, the only function you need is:

```
deltavals = Isotopomers(inputfile = 'FILENAME.csv', scrambling = [0.1..., 0.0...], **kwargs)
```

## Configuring Python on your computer: macOS

Check that you have python3 installed on your computer. On macOS, open a new Terminal window (see below for instructions for Windows). Run the following command:

```bash
colette$ python3 --version
```

This should output something like:

```bash
Python 3.9.2
```

Note that the text before the dollar sign will vary based on the user and computer. If python3 is not yet installed on your computer, try this [helpful guide](https://github.com/stanfordpython/python-handouts/blob/master/installing-python-macos.md) for installing Python as well as working with virtual environments.

Install the packages necessary to run pyIsotopomer. Run:

```bash
colette$ pip install --upgrade pip
colette$ pip install jupyter jupyterlab numpy scipy pandas
```

This may take a while; pip (the Python package manager) will check if these packages have already been installed, and if not, download them from the cloud and install them on your machine.

## Configuring Python on your computer: Windows

[...]

## Size correction

Export IRMS data in Isodat, with separate export templates for the sample peak and designated reference peak for each sample.

Open the .xls file containing Isodat output. Note that the spreadsheet contains two tabs: one contains raw data for each sample, and the other contains raw data for the designated reference peak for each sample.

In the "sample" tab, bring all fragment data in line, then delete extra rows. Do the same in the "standard" tab.

Open the data correction template "00_excel_template.xlsx". Copy the raw sample data from columns A-O in the sample tab into columns B-P in the correction template. Copy the "rR" columns from the standards tab (columns M, N, O) into columns R, S, T in the correction template. Save the correction template with a new name.

Check to make sure all references in columns V, W, X are correct. Note that the 31R, 45R, and 46R in columns V-X are specific to the Casciotti Lab's N2O reference gas. Note also that the size correction slopes in columns V-X are specific to the linearity of the Casciotti Lab Delta V, as of February-March 2021.

The 31R, 45R, and 46R for each sample, normalized to the common reference injection and normalized to a peak area of 20 Vs, are found in columns AH-AJ.

## Calibrating your instrument for scrambling with pyIsotopomer:

Here, two coefficients, $\gamma$ and $\kappa$, are used to describe scrambling in the ion source. This is described in further detail in [Frame and Casciotti, 2010](https://www.biogeosciences.net/7/2695/2010/). Below is a description of how to calculate these coefficients in pyIsotopomer.

Run two reference gases with known 15R-alpha and 15R-beta, prepared in the same format as samples (i.e., some amount of N2O reference gas injected into a bottle of seawater or DI water that has been purged with He or N2 gas). Export and size-correct these data in the excel correction template, as above.

From the correction template, copy and paste the size-corrected 31R, 45R, and 46R (columns AH, AI, AJ) from the size_correction tab into the scrambling_input tab, columns C-E. 

Reorganize the size corrected data...
