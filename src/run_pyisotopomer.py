"""
File: run_pyisotopomer.py
--------------

Run Scrambling and Isotopomers functions.

@author: Colette L. Kelly (clkelly@stanford.edu).
"""

from pyisotopomer import Scrambling, Isotopomers

gk = Scrambling(
    inputfile="00_Python_template_v2.xlsx",
    ref1="ATM",
    ref2="S2",
    ref3="B6",
    method="algebraic",
    initialguess=[0.17, 0.08]
)

deltavals = Isotopomers(
    inputfile="00_Python_template_v2.xlsx",
)
