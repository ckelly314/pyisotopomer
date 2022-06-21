"""
File: N2OSPcalcs.py
---------------------------
Created on Weds April 14th, 2021

Example script showing how to use isotopomer solver.

@author: Colette L. Kelly (clkelly@stanford.edu).
"""

# import utils
import numpy as np
import pandas as pd
import calcSPmain
import calcdeltaSP
import parseinput

###############
# USER INPUTS #
###############

# USER INPUT: Input data used to calculate isotopomers
# Enter data into "00_Python_template.xlsx" and save with a different name.
# Each row is one sample.
# Do not change the column headers.
# Input data should include at least six significant figures for accurate
# results.
inputfilename = "00_Python_template.xlsx"

# USER INPUT: isotopomers output filename
# Create a commma delimited file containing the isotope data
# The columns from left to right are:
# d15Nalpha, d15Nbeta, 15N site pref, d15Nbulk,  d17O, d18O
outputfilename = "example_isotopomer_output.csv"

# USER INPUT: scrambling coefficients
# These are calculated with the package of scrambling scripts:
# automate_gk_setinputs.py, automate_gk_solver.py, automate_gk_eqns.py, and constants.py
gamma_kappa = np.array([0.172170839, 0.079714555])

##################################################
# RUN SOLVER - NO NEED TO MODIFY BELOW THIS LINE #
##################################################
# read in data
# R = np.array(pd.read_csv(inputfilename, header=None))
R = parseinput.Input(inputfilename).sizecorrected

# Run function that iteratively solves for 15Ralpha and 15Rbeta (a and b)
# and then calculates 17R and 18R (c and d) by substitution
isol = calcSPmain.calcSPmain(R, scrambling=gamma_kappa)

# Run function that converts the data above to per mil notation referenced
# to AIR (for N) and VSMOW (for O).
deltaVals = calcdeltaSP.calcdeltaSP(isol)

# Create a .csv file containing the isotope data
deltaVals = pd.DataFrame(
    deltaVals, columns=["d15Na", "d15Nb", "SP", "d15Nbulk", "d17O", "d18O"]
)
deltaVals.to_csv(outputfilename)

# for testing:
print("Done 😛")
