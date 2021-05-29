"""
File: automate_gk_setinputs.py
---------------------------
Created on Weds April 14th, 2021

Example script showing how to use scrambling solver.

@author: Colette L. Kelly (clkelly@stanford.edu).
"""

#import utils
from automate_gk_solver import automate_gk_solver
import numpy as np
import pandas as pd

###############
# USER INPUTS #
###############

# USER INPUT: Input data used to solve equation.
# Columns are 31R, 45R and 46R for ref. #1, then 31R, 45R and 46R for ref. #2,
# from left to right.
# Each row is the data for one reference material pairing.
# Input data should include at least six significant figures for accurate 
# results.
inputfilename = 'example_scrambling_input.csv'

# USER INPUT: scrambling output filename
# columns are gamma, kappa from left to right
# Each row is the data for one reference material pairing.
outputfilename = 'example_scrambling_output.csv'

# USER INPUT: two reference materials used to calculate scrambling
# make sure these have been added to constants.py
ref1 = 'ATM'
ref2 = 'S2'

##################################################
# RUN SOLVER - NO NEED TO MODIFY BELOW THIS LINE #
##################################################

# read in data
R = np.array(pd.read_csv(inputfilename, header=None)) # need R to be an array

# Run function that iteratively solves for gamma and kappa
gk = automate_gk_solver(R,ref1=ref1, ref2=ref2)

# Create a .csv file containing the output data
# The columns from left to right are gamma and kappa
gk.to_csv(outputfilename, header=False, index=False)

# print out results
print(gk)
