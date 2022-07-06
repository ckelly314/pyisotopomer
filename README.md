# pyisotopomer

[![pypi badge](https://img.shields.io/pypi/v/pyisotopomer.svg?style=popout)](https://pypi.org/project/pyisotopomer)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.5031218.svg)](https://doi.org/10.5281/zenodo.5031218)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Hello!

pyisotopomer is a Python toolbox for processing nitrous oxide (N<sub>2</sub>O) isotopomer data. Its core is a package of scripts to correct for scrambling in the ion source during isotope ratio mass spectrometry. If you're unsure about how to install and run Python on your computer, you can easily run pyisotopomer on your Google Drive using Google Colab - see [Running pyisotopomer in Google Colab](#Running-pyisotopomer-in-Google-Colab) below.

## Intro

While the scrambling calibration is an integral part of obtaining high-quality N<sub>2</sub>O  isotopocule data from isotope ratio mass spectrometry, this calibration is part of a larger data processing pipeline. The scrambling calibration and isotopocule calculation steps can be performed in pyisotopomer.

![](flowchart.jpg)

**Contents:**
- [pyisotopomer](#pyisotopomer)
  - [Basic use](#basic-use)
  - [Running pyisotopomer in Google Colab](#Running-pyisotopomer-in-Google-Colab)
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

You can walk through these steps in this [Colab Notebook](https://drive.google.com/file/d/1hEVvs98ZrpDxzNLJ2D0H6zJjnEs2umiq/view?usp=sharing).

## Running pyisotopomer in Google Colab

You can install and run pyisotopomer locally on your computer, or you can run it online in Google Colaboratory (Colab). Google Colab is free and allows you to run Python (and pyisotopomer) without installing it on your computer. This [Google Colab notebook](https://drive.google.com/file/d/1hEVvs98ZrpDxzNLJ2D0H6zJjnEs2umiq/view?usp=sharing) contains instructions on how to use the Google Colab environment and example code to run pyisotopomer. Once you click on this link, you should see an option to "Open with Google Colaboratory"; click on this to open the notebook. If you have never used Google Colab before, you need to connect Google Colab to your Google Drive. To do that, follow the link above, at the top of the page click on “Connect More Apps” and choose “Colab”. Sometimes, you need to load the webpage a few times before you see Google Colab in the app choices.

## Pre-processing

Download the data correction [template](https://docs.google.com/spreadsheets/d/1YMyaIXTMbX56r5_1C3ovAb_GBVsQJXfr/edit?usp=sharing&ouid=104573000701514802850&rtpof=true&sd=true).

Export IRMS data in Isodat, with separate export templates for the sample peak and designated reference peak for each sample.

Open the .xls file containing Isodat output. Note that the spreadsheet contains two tabs: one contains raw data for each sample, and the other contains raw data for the designated reference peak for each sample.

In the "sample" tab, bring all fragment data in line, then delete extra rows. Do the same in the "standard" tab.

Open the data correction template. In the "size_correction" tab, copy the raw sample data from columns A-O in the sample tab into columns C-Q in the correction template. Copy the "rR" columns from the standards tab (columns M, N, O) into columns S, T, U in the correction template.

Replace the values in row 3, columns W-Y with the appropriate 31R, 45R, and 46R for your N<sub>2</sub>O reference tank (the reference gas used for on-offs/direct injections). The values in the template spreadsheet are specific to the Casciotti Lab's N<sub>2</sub>O reference tank.

Replace the values in row 7, columns W-Y, with your size correction slopes. Ensure that these size correction slopes are normalized to the m/z 44 peak area. Ensure that they apply to the raw "ratio of ratios" 31rR/31rR, 45rR/45rR, and 45rR/45rR in columns AA-AC. The values in the template spreadsheet are specific to the linearity of the Casciotti Lab Delta V, as of February-March 2021.

Go to the "scale_normalization" tab of the excel template. Columns A-F contain the pre-loaded delta values for a set of reference gases. If your reference gases are not listed, add their calibrated delta values in columns A-F, then copy the calculations in columns G-N. Columns M and N contain the "known" 45/44R and 46/44R for each reference material, normalized to the 45/44 and 46/44 of your N2O reference tank.

Columns P-R are references to the names, size corrected 45rR/45rR, and 46rR/46rR of each sample in your run. Drag these cells down to include all of the reference materials in your run. Columns S and T are the "known" 45rR/45rR and 46rR/46rR for each reference material — CHANGE these values so that they point to the appropriate values in columns M and N. Inspect the plot in columns AB-AF to ensure that the slopes and R<sup>2</sup> are close to 1 (if not, check for problem reference materials that are throwing off the calibration). Row 3, columns Y and Z contain the 𝜆 factors needed to scale-normalize the measured 45rR/45rR and 46rR/46rR of the data.

Return to the "size_correction" tab of the excel template. Rows AI-AJ contain the scale-normalized 45rR/45rR and 46rR/46rR of each samples.

The 31R, 45R, and 46R for each sample, normalized to the common reference injection, normalized to a m/z 44 peak area of 20 Vs, and scale-normalized (in the case of 45R and 46R), are found in columns AL-AN. Save the correction template with a new name into your current working directory, or, if you're using Google Colab, upload it to your data processing folder in your drive.

## Scrambling calibration

Here, two coefficients, γ and κ, are used to describe scrambling in the ion source. This is described in further detail in [Frame and Casciotti, 2010](https://www.biogeosciences.net/7/2695/2010/). Below is a description of how to calculate these coefficients in pyisotopomer.

Run two (or more) reference gases with known <sup>15</sup>R-α and <sup>15</sup>R-β, prepared in the same format as samples. For the Casciotti lab, this is some amount of N<sub>2</sub>O reference gas injected into a bottle of seawater or DI water that has been purged with He or N2 gas.

Download the data correction [template](https://docs.google.com/spreadsheets/d/1YMyaIXTMbX56r5_1C3ovAb_GBVsQJXfr/edit?usp=sharing&ouid=104573000701514802850&rtpof=true&sd=true). Pre-process the data according to the pyisotopomer [README](https://github.com/ckelly314/pyisotopomer). Save it into your current working directory.

Go to the "scale_normalization" tab of the excel template. Make sure it contains all of the reference materials you will use for the scrambling calculation. In column A "ref_tag", enter the names of your reference materials — these can be whatever you want, as long as they contain only alphanumeric characters and are short (15 characters or fewer).

Go to the "size_correction" tab of the excel template. To mark which rows of the correction template represent reference materials, in column B "ref_tag", add the names of the reference materials, as they appear in the "scale_normalization" tab. For example, here, atmosphere-equilibrated seawater is named "ATM" and is marked as such in the "ref_tag" column.

DO NOT MODIFY COLUMN HEADERS IN THE CORRECTION TEMPLATE. Save the correction template into your current working directory.

### Choice of Method

Pyisotopomer contains two methods for the calculation of γ and κ: a direct calculation of γ and κ based on the algebraic re-arrangement of the equation for <sup>31</sup>R, and a least-squares solver method. Given the right reference materials, it is not necessary to use a numerical algorithm to solve for γ and κ; algebraic manipulations can provide exact and unique solutions for each coefficient. This algebraic solution is the default method of calculation of γ and κ in pyisotopomer. It should be noted that this algebraic solution produces consistent results only when the site preferences of the two reference materials used in the calculation are sufficiently distinct — otherwise, it will return values of γ and κ that vary widely and may not fall in the range of plausible values (i.e., they are either negative or greater than one).

In the event that the user has yet to obtain reference materials that are different enough in their site preferences to produce consistent results with the algebraic method, the least squares approach can be used as a temporary alternative, with the following caveats and modifications:
 - The least squares solver finds a local minimum close to the initial guess for γ and κ. As such, if the solver is fed an initial guess other than the absolute minimum calculated from the algebraic solution, it will find the “wrong” scrambling coefficients.
 - Using these “wrong” scrambling coefficients is OK if your unknowns are close in their delta values to those of the reference materials, but will have a deleterious effect as the unknowns diverge in their isotopomer values from the reference materials.
 - If the least squares solver is fed the correct γ and κ as an initial guess, it will converge on that solution — although this is still not as robust as simply running reference materials of sufficiently distinct site preferences and calculating γ and κ algebraically.

The algebraic method is the default and does not require any modifications to the call to the Scrambling function. To change to the least squares method, specify it with the "method" keyword argument. If you have an _a priori_ initial guess for γ and κ, enter it using the "initialguess" keyword argument.

To calculate scrambling with the algebraic method, modify the "inputfile" keyword to reflect the name of your excel data corrections spreadsheet, then run the following code:

```Python
Scrambling(inputfile="00_Python_template_v2.xlsx", **kwargs)
```

To calculate scrambling with the least squares method, modify the "inputfile" keyword to reflect the name of your excel data corrections spreadsheet, set the method to "least_squares", and enter an initial guess for gamma and kappa (format [gamma, kappa]). Run the following code:

```Python
Scrambling(inputfile="00_Python_template_v2.xlsx", method="least_squares",
          initialguess=[0.17, 0.08], **kwargs)
```

The Scrambling function will create an output file entitled ```{date}_scrambling_output.xlsx``` with scrambling output, similar to this [example spreadsheet](https://docs.google.com/spreadsheets/d/1Z_jMqslWt4LfdaFTM_Ngt3a2VtxXn-mm/edit?usp=sharing&ouid=104573000701514802850&rtpof=true&sd=true). The Scrambling function will also output two .csv files containing intermediate data products: [normalized_ratios.csv](https://drive.google.com/file/d/1baG9H-MQuVRv9crKAKPQlj2wrp3l4qvj/view?usp=sharing) contains the <sup>15</sup>R<sup>bulk</sup>, <sup>17</sup>R, and <sup>18</sup>R that pyisotopomer calculated from the normalized <sup>45</sup>R and <sup>46</sup>R of each reference material, and [normalized_deltas.csv](https://drive.google.com/file/d/1bx-Mop1dzjX5rhooWN79dgdfTjhWOvUi/view?usp=sharing) contains the equivalent delta values. You can copy the values from "normalized_deltas.csv" into rows AT-AV of the excel template. If the scale normalization was effective, the δ<sup>15</sup>N<sup>bulk</sup> and δ<sup>18</sup>O of each reference material should be close to their calibrated values.

### Google Colab notebook for the scrambling calculation

This [Google Colab notebook](https://drive.google.com/file/d/1hEVvs98ZrpDxzNLJ2D0H6zJjnEs2umiq/view?usp=sharing) contains instructions on how to use the Google Colab environment and example code to run the Scrambling function of pyisotopomer.

### Example Python script for the scrambling calculation

This [Python script](https://github.com/ckelly314/pyisotopomer/blob/master/tests/run_pyisotopomer.py) contains an example script that runs the code above. Save it into your current working directory. Run the script with:

```bash
colette$ python run_pyisotopomer.py
```

## Calculating isotopomers

Size-correct your data (including all samples and standards), as above. Enter the appropriate γ and κ in columns AO-AP of the excel template. These should be a running average of γ and κ, calculated using a window of \~10 reference material pairings (see below).

DO NOT MODIFY COLUMN HEADERS IN THE CORRECTION TEMPLATE. Save the correction template into your current working directory.

### How to think about scrambling when calculating isotopomers

You will need to enter the appropriate scrambling coefficients in the excel template. These scrambling coefficients should represent a running average of γ and κ calculated from at least 10 pairings of reference materials (e.g. a week's worth, if unknowns are bookended by reference materials) run alongside unknowns. This is because a small standard deviation in the scrambling coefficients can lead to a large error in site preference, so it is advisable to run sufficient reference materials to bring down the standard deviation of γ and κ. To calculate these running averages, it can be helpful to keep a spreadsheet with a running log of scrambling coefficients.

To calculate isotopomers, modify the "inputfile" keyword to reflect the name of your excel data corrections spreadsheet, then run the following code:

```Python
Isotopomers(inputfile = "00_Python_template_v2.xlsx", **kwargs)
```

the Isotopomers function will create an output file entitled ```{date}_isotopeoutput.csv``` with isotopocule delta values, similar to this [example spreadsheet](https://drive.google.com/file/d/1ZWws_32rjzutNkmD4HYebJBWjjIPRwt1/view?usp=sharing). Copy and paste output data back into working (size correction) spreadsheet in olive-highlighted cells (columns AX-BC).

### Google Colab notebook forthe isotopomer calculation

This [Google Colab notebook](https://drive.google.com/file/d/1hEVvs98ZrpDxzNLJ2D0H6zJjnEs2umiq/view?usp=sharing) contains instructions on how to use the Google Colab environment and example code to run the Isotopomers function of pyisotopomer.

### Example Python script for the isotopomer calculation

This [Python script](https://github.com/ckelly314/pyisotopomer/blob/master/tests/run_pyisotopomer.py) contains an example script that runs the code above. Save it into your current working directory. Run the script with:

```bash
colette$ python run_pyisotopomer.py
```

## Calculating concentrations

To calculate the concentration of N<sub>2</sub>O:

Go to the "concentration_constants" tab of the excel template. Following the example calibration curve, calculate the ratio of mass 44 peak area to N<sub>2</sub>O (nmol/Vs) for your instrument. Update the values in row 2, columns B and D to reflect this calibration.

Go to the "size_correction" tab of the excel template. Columns BE-BM contain the concentration calculation for liquid samples — that is, N<sub>2</sub>O dissolved in seawater, DI water, or freshwater. Enter the weights of each sample pre- and post- analysis in columns BE-BF. Column BI calculates volume from weight difference using the appropriate density of each sample matrix; ensure that this refers to the correct densities in the "concentration_constants" tab. Column BJ contains the N<sub>2</sub>O nmol amount in each sample, and column BL contains the concentration.
