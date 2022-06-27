# pyisotopomer

[![pypi badge](https://img.shields.io/pypi/v/pyisotopomer.svg?style=popout)](https://pypi.org/project/pyisotopomer)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.5031218.svg)](https://doi.org/10.5281/zenodo.5031218)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Hello!

pyisotopomer is a Python toolbox for processing nitrous oxide (N<sub>2</sub>O) isotopomer data. Its core is a package of scripts to correct for scrambling in the ion source during isotope ratio mass spectrometry. An alternate version of this package exists for [MATLAB](https://github.com/ckelly314/m-isotopomer).

## Intro

While the scrambling calibration is an integral part of obtaining high-quality N<sub>2</sub>O  isotopocule data from isotope ratio mass spectrometry, this calibration is part of a larger data processing pipeline. The scrambling calibration and isotopocule calculation steps can be performed in pyisotopomer.

![](flowchart.jpg)

**Contents:**
- [pyisotopomer](#pyisotopomer)
  - [Basic use](#basic-use)
  - [Configuring python: macOS](#configuring-python-macOS)
  - [Configuring python: Windows](#configuring-python-windows)
  - [Pre-processing](#pre-processing)
  - [Scrambling calibration](#scrambling-calibration)
  - [Calculating isotopomers](#calculating-isotopomers)
  - [Calculating concentrations](#calculating-concentrations)

## Basic use

The import convention for pyisotopomer is:

```Python
from pyisotopomer import Scrambling, Isotopomers
```

To calculate scrambling coefficients, the only function you need is:

```Python
Scrambling(inputfile="FILENAME.xlsx", **kwargs)
```

To calculate isotopomers, the only function you need is:

```Python
Isotopomers(inputfile = "FILENAME.xlsx", **kwargs)
```

You can walk through these steps in this [Jupyter Notebook](https://drive.google.com/file/d/1hEVvs98ZrpDxzNLJ2D0H6zJjnEs2umiq/view?usp=sharing).

## Configuring Python: macOS

Check that you have python3 installed on your computer. On macOS, open a new Terminal window (see below for instructions for Windows). Run the following command:

```bash
colette$ python3 --version
```

This should output something like:

```bash
Python 3.9.2
```

Note that the text before the dollar sign will vary based on the user and computer. Additionally, the dollar sign may be replaced by a percent sign if your terminal is in zshell (zsh) instead of bash, but this is not an important difference for the code below. If python3 is not yet installed on your computer, try this [helpful guide](https://github.com/stanfordpython/python-handouts/blob/master/installing-python-macos.md) for installing Python as well as working with virtual environments.

Install pyisotopomer. Run:

```bash
colette$ pip install --upgrade pip
colette$ pip install pyisotopomer
```

This may take a while; pip (the Python package manager) will download pyisotopomer and its dependencies from the cloud and install them on your machine. 

## Configuring Python: Windows

Requires: 64-bit Windows 10, updated to the 2016 Anniversary build or later. *If you regularly download updates, you'll be fine.*

Windows 10 has added a subsystem called Ubuntu that allows you to open a bash shell. If you don't know what a bash shell is, that's totally fine — just follow the instructions below.

First, follow [these instructions](https://www.howtogeek.com/249966/how-to-install-and-use-the-linux-bash-shell-on-windows-10/) from HowToGeek. These will help you activate the "Windows Subsystem for Linux," get Ubuntu from the Microsoft Store, and launch a `bash` shell on Ubuntu.

Once you're in the `bash` shell, run the following commands to install Python 3.9 on your computer:

```bash
$ sudo add-apt-repository ppa:deadsnakes/ppa
$ sudo apt-get update
$ sudo apt-get install python3.9
```

You can check which version of Python you've installed by running:

```bash
$ python3 --version
```

This should output something like:

```bash
Python 3.9.2
```

Install pyisotopomer. Run:

```bash
$ pip install "prompt-toolkit==2.0.10" "ipython[all]" pyisotopomer
```

This may take a while; pip (the Python package manager) will download pyisotopomer and its dependencies from the cloud and install them on your machine. 

## Pre-processing

Download the data correction [template](https://github.com/ckelly314/pyisotopomer/blob/master/src/00_Python_template_v2.xlsx).

Export IRMS data in Isodat, with separate export templates for the sample peak and designated reference peak for each sample.

Open the .xls file containing Isodat output. Note that the spreadsheet contains two tabs: one contains raw data for each sample, and the other contains raw data for the designated reference peak for each sample.

In the "sample" tab, bring all fragment data in line, then delete extra rows. Do the same in the "standard" tab.

Open the data correction template. In the "size_correction" tab, copy the raw sample data from columns A-O in the sample tab into columns C-Q in the correction template. Copy the "rR" columns from the standards tab (columns M, N, O) into columns S, T, U in the correction template.

Replace the values in row 3, columns W-Y with the appropriate 31R, 45R, and 46R for your N<sub>2</sub>O reference tank (the reference gas used for on-offs/direct injections). The values in the template spreadsheet are specific to the Casciotti Lab's N<sub>2</sub>O reference tank.

Replace the values in row 7, columns W-Y, with your size correction slopes. Ensure that these size correction slopes are normalized to the m/z 44 peak area. Ensure that they apply to the raw "ratio of ratios" 31rR/31rR, 45rR/45rR, and 45rR/45rR in columns AA-AC. The values in the template spreadsheet are specific to the linearity of the Casciotti Lab Delta V, as of February-March 2021.

Go to the "scale_normalization" tab of the excel template. Columns A-F contain the pre-loaded delta values for a set of reference gases. If your reference gases are not listed, add their calibrated delta values in columns A-F, then copy the calculations in columns G-N. Columns M and N contain the "known" 45/44R and 46/44R for each reference material, normalized to the 45/44 and 46/44 of your N2O reference tank.

Columns P-R are references to the names, size corrected 45rR/45rR, and 46rR/46rR of each sample in your run. Drag these cells down to include all of the reference materials in your run. Columns S and T are the "known" 45rR/45rR and 46rR/46rR for each reference material — CHANGE these values so that they point to the appropriate values in columns M and N. Inspect the plot in columns AB-AF to ensure that the slopes and R<sup>2</sup> are close to 1 (if not, check for problem reference materials that are throwing off the calibration). Row 3, columns Y and Z contain the 𝜆 factors needed to scale-normalize the measured 45rR/45rR and 46rR/46rR of the data.

Return to the "size_correction" tab of the excel template. Rows AI-AJ contain the scale-normalized 45rR/45rR and 46rR/46rR of each samples.

The 31R, 45R, and 46R for each sample, normalized to the common reference injection, normalized to a m/z 44 peak area of 20 Vs, and scale-normalized (in the case of 45R and 46R), are found in columns AL-AN. Save the correction template with a new name into your current working directory.

## Scrambling calibration

Here, two coefficients, γ and κ, are used to describe scrambling in the ion source. This is described in further detail in [Frame and Casciotti, 2010](https://www.biogeosciences.net/7/2695/2010/). Below is a description of how to calculate these coefficients in pyisotopomer.

Download [constants.csv](https://drive.google.com/file/d/1hrllkbP2ywSr-BHP93C0DQpUVKVOLX5b/view?usp=sharing).

Open ```constants.csv```. Here, we specify the calibrated isotope ratios of named reference materials. If the reference materials to be used to calibrate scrambling are not in this list, add them, following the format of the existing lines. Save ```constants.csv``` into your current working directory.

Run two (or more) reference gases with known <sup>15</sup>R-α and <sup>15</sup>R-β, prepared in the same format as samples. For the Casciotti lab, this is some amount of N<sub>2</sub>O reference gas injected into a bottle of seawater or DI water that has been purged with He or N2 gas.

Export, size-correct, and scale-normalize these data in the excel correction template, as above. The placeholder samples in the template spreadsheet are arranged in the right order 1-7, but this may not necessarily be the case, depending on how one performs the steps above. The order is not important to what follows, as long as the samples (columns C-Q) and reference peaks (columns S-U) are in the same order.

To mark which rows of the correction template represent reference materials, in column B "ref_tag", add the names of the reference materials, as they appear in ```constants.csv```. For example, here, atmosphere-equilibrated seawater is named "ATM" and is marked as such in the "ref_tag" column.

DO NOT MODIFY COLUMN HEADERS IN THE CORRECTION TEMPLATE. Save the correction template into your current working directory.

### Choice of Method

Pyisotopomer contains two methods for the calculation of γ and κ: a direct calculation of γ and κ based on the algebraic re-arrangement of the equation for <sup>31</sup>R, and a least-squares solver method. Given the right reference materials, it is not necessary to use a numerical algorithm to solve for γ and κ; algebraic manipulations can provide exact and unique solutions for each coefficient. This algebraic solution is the default method of calculation of γ and κ in pyisotopomer. It should be noted that this algebraic solution produces consistent results only when the site preferences of the two reference materials used in the calculation are sufficiently distinct — otherwise, it will return values of γ and κ that vary widely and may not fall in the range of plausible values (i.e., they are either negative or greater than one).

In the event that the user has yet to obtain reference materials that are different enough in their site preferences to produce consistent results with the algebraic method, the least squares approach can be used as a temporary alternative, with the following caveats and modifications:
 - The least squares solver finds a local minimum close to the initial guess for γ and κ. As such, if the solver is fed an initial guess other than the absolute minimum calculated from the algebraic solution, it will find the “wrong” scrambling coefficients.
 - Using these “wrong” scrambling coefficients is OK if your unknowns are close in their delta values to those of the reference materials, but will have a deleterious effect as the unknowns diverge in their isotopomer values from the reference materials.
 - If the least squares solver is fed the correct γ and κ as an initial guess, it will converge on that solution — although this is still not as robust as simply running reference materials of sufficiently distinct site preferences and calculating γ and κ algebraically.

The algebraic method is the default and does not require any modifications to the call to the Scrambling function. To change to the least squares method, specify it as follows. If you have an _a priori_ initial guess for γ and κ, enter it using the "initialguess" keyword argument.

```Python
Scrambling(inputfile="FILENAME.xlsx", method="least_squares", **kwargs)
```

### Example Python script for the scrambling calculation

Download this [Python script](https://github.com/ckelly314/pyisotopomer/blob/master/tests/run_pyisotopomer.py). Save it into your current working directory. The script includes example calls to the functions Scrambling and Isotopomers. Update the keyword arguments to reflect the filename of your template spreadsheet, the names of your reference materials, and the appropriate initial guess for your IRMS (if known). Run the script:

```bash
colette$ python run_pyisotopomer.py
```

### Example Jupyter Notebook for the scrambling calculation

Download this [Jupyter Notebook](https://drive.google.com/file/d/1hEVvs98ZrpDxzNLJ2D0H6zJjnEs2umiq/view?usp=sharing). Save it into your current working directory.

Open a terminal window. Launch Jupyter Notebook:

```bash
colette$ jupyter notebook
```

This should open Jupyter in a new browser window. In Jupyter, navigate to your current working directory. Click on ```run_pyIsotopomer.ipynb``` to open the Jupyter Notebook containing the code to run pyisotopomer. Follow the instructions in the Jupyter Notebook to run pyisotopomer and obtain scrambling coefficients for all possible pairings of reference materials.

Regardless of whether it is run in a Python script or Jupyter Notebook, the Scrambling function will create an output file entitled ```{date}_scrambling_output.xlsx``` with scrambling output, similar to this [example spreadsheet](https://github.com/ckelly314/pyisotopomer/blob/master/tests/example_scrambling_output.xlsx). The Scrambling function will also output two .csv files containing intermediate data products: [normalized_ratios.csv](https://github.com/ckelly314/pyisotopomer/blob/master/src/normalized_ratios.csv) contains the <sup>15</sup>R<sup>bulk</sup>, <sup>17</sup>R, and <sup>18</sup>R that pyisotopomer calculated from the normalized <sup>45</sup>R and <sup>46</sup>R of each reference material, and [normalized_deltas.csv](https://github.com/ckelly314/pyisotopomer/blob/master/src/normalized_deltas.csv) contains the equivalent delta values. You can copy the values from "normalized_deltas.csv" into rows AT-AV of the excel template. If the scale normalization was effective, the δ<sup>15</sup>N<sup>bulk</sup> and δ<sup>18</sup>O of each reference material should be close to their calibrated values.

## Calculating isotopomers

Size-correct your data (including all samples and standards), as above. Enter the appropriate γ and κ in rows AO-AP of the excel template. These should be a running average of γ and κ, calculated using a window of \~10 reference material pairings (see below).

DO NOT MODIFY COLUMN HEADERS IN THE CORRECTION TEMPLATE. Save the correction template into your current working directory.

### How to think about scrambling when calculating isotopomers

You will need to enter the appropriate scrambling coefficients in the excel template. These scrambling coefficients should represent a running average of γ and κ calculated from at least 10 pairings of reference materials (e.g. a week's worth, if unknowns are bookended by reference materials) run alongside unknowns. This is because a small standard deviation in the scrambling coefficients can lead to a large error in site preference, so it is advisable to run sufficient reference materials to bring down the standard deviation of γ and κ.

### Example Python script for the isotopomer calculation

Download this [Python script](https://github.com/ckelly314/pyisotopomer/blob/master/tests/run_pyisotopomer.py). Save it into your current working directory. The script includes example calls to the functions Scrambling and Isotopomers. Update the keyword arguments to reflect the filename of your template spreadsheet, the names of your reference materials, and the appropriate initial guess for your IRMS (if known). Run the script:

```bash
colette$ python run_pyisotopomer.py
```

### Example Jupyter Notebook for the isotopomer calculation

Download this [Jupyter Notebook](https://drive.google.com/file/d/1hEVvs98ZrpDxzNLJ2D0H6zJjnEs2umiq/view?usp=sharing). Save it into your current working directory.

Open a terminal window. Launch Jupyter Notebook:

```bash
colette$ jupyter notebook
```

This should open Jupyter in a new browser window. In Jupyter, navigate to your current working directory. Click on ```run_pyIsotopomer.ipynb``` to open the Jupyter Notebook containing the code to run pyisotopomer. Follow the instructions in the Jupyter Notebook to run pyisotopomer and obtain sample isotopocule values in delta notation, as well as isotope ratios.

Regardless of whether it is run in a Python script or Jupyter Notebook, the Isotopomers function will create an output file entitled ```{date}_isotopeoutput.csv``` with isotopocule delta values, similar to this [example spreadsheet](https://github.com/ckelly314/pyisotopomer/blob/master/tests/example_isotopomer_output.csv). Copy and paste output data back into working (size correction) spreadsheet in olive-highlighted cells (columns AX-BC).

## Calculating concentrations

To calculate the concentration of N<sub>2</sub>O:

Go to the "concentration_constants" tab of the excel template. Following the example calibration curve, calculate the ratio of mass 44 peak area to N<sub>2</sub>O (nmol/Vs) for your instrument. Update the values in row 2, columns B and D to reflect this calibration.

Go to the "size_correction" tab of the excel template. Columns BE-BM contain the concentration calculation for liquid samples — that is, N<sub>2</sub>O dissolved in seawater, DI water, or freshwater. Enter the weights of each sample pre- and post- analysis in columns BE-BF. Column BI calculates volume from weight difference using the appropriate density of each sample matrix; ensure that this refers to the correct densities in the "concentration_constants" tab. Column BJ contains the N<sub>2</sub>O nmol amount in each sample, and column BL contains the concentration.
