"""
File: constants.py
---------------------------
Created on Weds April 14th, 2021

Define alpha and beta values for the reference materials used for
the scrambling calibration.

@author: Colette L. Kelly (clkelly@stanford.edu).
"""


import pandas as pd
import numpy as np


def constants(ref1, ref2):
    """
    Return 15Ralpha and 15Rbeta for the two reference materials used to
    calibrate scrambling.

    USAGE: a, b, a2, b2 = constants('ATM', 'S2')

    INPUT:
        :param ref1: name of first reference material used for scrambling calibration
        :type ref1: string
        :param ref2: name of second reference material used for scrambling calibration
        :type ref2: string

    OUTPUT:
        :returns: 15Ralpha #1, 15Rbeta #1, 15Ralpha #2, 15Rbeta #2

    """

    try:  # read in .csv file containing ref. materials used for the scrambling calibration

        data = pd.read_csv("constants.csv")

        # constants for ref1
        a = float(data[data.Ref_material == ref1].R15alpha)
        b = float(data[data.Ref_material == ref1].R15beta)

        # constants for ref2
        a2 = float(data[data.Ref_material == ref2].R15alpha)
        b2 = float(data[data.Ref_material == ref2].R15beta)

    except FileNotFoundError:  # set constants to NaN's if constants.csv is not found

        a = np.NaN
        b = np.NaN
        a2 = np.NaN
        b2 = np.NaN

    return a, b, a2, b2
