"""
File: run_pyisotopomer.py
-------------------------

# This is an example script, showing how to use pyisotopomer.
# The only required argument for each function is "inputfile" - 
# the others listed can be deleted and will revert to a default value.

@author: Colette L. Kelly (clkelly@stanford.edu).
"""

from pyisotopomer import Scrambling, Isotopomers

gk = Scrambling(
    inputfile="00_Python_template_v3.xlsx",  # change to appropriate file name
    # extra keyword arguments:
    tabname="size_correction",
    saveout=True,
    outputfile="example_scrambling_output.xlsx",
    method="least_squares",
    # initialguess=[0.17, 0.08], # only applies to the "least_squares" method
    # lowerbounds=[0.0, 0.0], # only applies to the "least_squares" method
    # upperbounds=[1.0, 1.0], # only applies to the "least_squares" method
    # weights=False, # only applies to the "least_squares" method
    ref1="ATM",  # you can list as many reference materials as you want
    ref2="S2",
    ref3="B6",
    O17beta=None,
    R15Air=None,
    R17VSMOW=None,
    R18VSMOW=None,
)

deltavals = Isotopomers(
    inputfile="00_Python_template_v3.xlsx",
    # extra keyword arguments:
    saveout=True,
    outputfile="example_isotopomer_output.csv",
    initialguess=[0.0037, 0.0037],
    lowerbounds=[0.0, 0.0],
    upperbounds=[1.0, 1.0],
    O17beta=None,
    R15Air=None,
    R17VSMOW=None,
    R18VSMOW=None,
)

from pyisotopomer import Tracers

Tracers(inputfile="00_Tracer_template.xlsx", outputfile = "tracer_output.csv")