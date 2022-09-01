"""
File: constants_new.py
--------------------------------
Created on Weds July 6th, 2021

Define alpha and beta values for the reference materials used for
the scrambling calibration.

NEW: Read in data from excel template instead of from a separate file.

@author: Colette L. Kelly (clkelly@stanford.edu).
"""

import pandas as pd
import numpy as np


def constants_new(isotopeconstants, ref1, ref2):
    """
    Return 15Ralpha and 15Rbeta for the two reference materials used to
    calibrate scrambling.

    USAGE: a, b, a2, b2 = constants_new(isotopeconstants, ref1, ref2)

    INPUT:
        :param isotopeconstants: ref_tag, d15Na, and d15Nb of reference materials
            entered into the "scale_normalization" tab of the excel template
        :type isotopeconstants: Pandas Dataframe
        :param ref1: name of first reference material used for scrambling calibration
        :type ref1: string
        :param ref2: name of second reference material used for scrambling calibration
        :type ref2: string

    OUTPUT:
        :returns: 15Ralpha #1, 15Rbeta #1, 15Ralpha #2, 15Rbeta #2

    """
    d15Na_1 = float(isotopeconstants[isotopeconstants["ref_tag"] == ref1].d15Na)
    a = (d15Na_1 / 1000 + 1) * 0.0036765

    d15Nb_1 = float(isotopeconstants[isotopeconstants["ref_tag"] == ref1].d15Nb)
    b = (d15Nb_1 / 1000 + 1) * 0.0036765

    d15Na_2 = float(isotopeconstants[isotopeconstants["ref_tag"] == ref2].d15Na)
    a2 = (d15Na_2 / 1000 + 1) * 0.0036765

    d15Nb_2 = float(isotopeconstants[isotopeconstants["ref_tag"] == ref2].d15Nb)
    b2 = (d15Nb_2 / 1000 + 1) * 0.0036765

    return a, b, a2, b2
