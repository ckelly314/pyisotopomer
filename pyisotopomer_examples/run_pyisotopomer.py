"""
File: run_pyisotopomer.py
--------------

Run Scrambling and Isotopomers functions.
"""

from pyisotopomer import Scrambling, Isotopomers

gk = Scrambling(
    inputfile="00_Python_template_v2.xlsx",  # change to appropriate file name
    # extra keyword arguments:
    tabname="size_correction",
    saveout=True,
    outputfile="example_scrambling_output.xlsx",
    method="algebraic",
    # initialguess=[0.17, 0.08], # only applies to the "least_squares" method
    # lowerbounds=[0.0, 0.0], # only applies to the "least_squares" method
    # upperbounds=[1.0, 1.0], # only applies to the "least_squares" method
    # weights=False, # only applies to the "least_squares" method
    ref1="ATM",  # you can list as many reference materials as you want
    #ref2="S2",
    ref3="B6",
    O17beta=None,
    R15Air=None,
    R17VSMOW = None,
    R18VSMOW = None
)

deltavals = Isotopomers(
    inputfile="00_Python_template_v2.xlsx",
    # extra keyword arguments:
    saveout=True,
    outputfile="example_isotopomer_output.csv",
    initialguess=[0.0037, 0.0037],
    lowerbounds=[0.0, 0.0],
    upperbounds=[1.0, 1.0],
    O17beta=None,
    R15Air=None,
    R17VSMOW = None,
    R18VSMOW = None,
)
