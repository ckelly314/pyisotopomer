"""
File: automate_gk_setinputs.py
---------------------------
Created on Weds April 14th, 2021

Example script showing how to use scrambling solver.

@author: Colette L. Kelly (clkelly@stanford.edu).
"""

# import utils
import pandas as pd
import parseinput
import parseoutput

###############
# USER INPUTS #
###############

# USER INPUT: Input data used to calculate scrambling.
# Enter data into "00_Python_template.xlsx" and save with a different name.
# Enter the names of reference materials in the "ref_tag" column (column B)
# as they appear in constants.py.
# Each row is one reference material.
# Do not change the column headers.
# Input data should include at least six significant figures for accurate
# results.
inputfilename = "00_Python_template.xlsx"

# USER INPUT: Scrambling output filename.
# The first sheet of this excel file will contain all scrambling data.
# Subsequent sheets will contain scrambling data for each pairing
# of reference materials.
outputfilename = "example_scrambling_output.xlsx"

# USER INPUT:
# function call & reference materials used to calculate scrambling
# make sure these have been added to constants.py
inputobj = parseinput.Input(inputfilename, ref1="ATM", ref2="S2", ref3="B6")

##################################################
# RUN SOLVER - NO NEED TO MODIFY BELOW THIS LINE #
##################################################

# set up empty list of output df's
outputdfs, dfnames, maindf = parseoutput.parseoutput(inputobj)

# Create an excel file containing the output data
with pd.ExcelWriter(outputfilename) as writer:
    maindf.to_excel(writer, sheet_name="all")  # save out main dataframe to one sheet
    for df, name in zip(outputdfs, dfnames):
        # write each output dataframe to a separate sheet in the output spreadsheet
        df.to_excel(writer, sheet_name=name)

# for testing:
print("Done 😛")
