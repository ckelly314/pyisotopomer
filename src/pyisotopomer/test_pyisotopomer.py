"""
File: test_pyisotopomer.py
--------------

A test script for pyisotopomer implementation.
"""

from pyisotopomer import Scrambling, Isotopomers

gk = Scrambling(
    inputfile="00_Python_template.xlsx",
    ref1="ATM",
    ref2="S2",
    ref3="B6",
    initialguess=[0.17, 0.08],
)

deltavals = Isotopomers(
    inputfile="00_Python_template.xlsx", scrambling=gk.scrambling_mean, saveout=False
)

print(gk)
