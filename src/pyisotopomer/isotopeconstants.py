"""
File: isotopeconstants.py
-------------------------------
Created on Thurs July 7th, 2021

Initialize and store isotope constants as adjustable parameters.

@author: Colette L. Kelly (clkelly@stanford.edu).
"""


import pandas as pd
import numpy as np


def isotopeconstants():
    """
    Return 15Ralpha and 15Rbeta for the two reference materials used to
    calibrate scrambling.

    USAGE: a, b, a2, b2 = constants('ATM', 'S2')

    INPUT:
        :param ref1:
        :type ref1:

    OUTPUT:
        :returns: 15Ralpha #1, 15Rbeta #1, 15Ralpha #2, 15Rbeta #2

    """

    O17slope = 0.516
    O17excess = 0.0
    R15Air = 0.0036765
    R17VSMOW = 0.0003799
    R18VSMOW = 0.002052

    return O17slope, O17excess, R15Air, R17VSMOW, R18VSMOW
