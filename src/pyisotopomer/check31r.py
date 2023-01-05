"""
File: check31r.py
---------------------------------
Created on Tues Dec 27th, 2022

Check accuracy of gamma and kappa by comparing calculated 31R
to measured 31R.

@author: Colette L. Kelly (clkelly@stanford.edu).
"""

import numpy as np
from .constants_new import (
    constants_new,
)  # import alpha and beta values for reference materials


def check31r(f, R, isotopeconstants, ref1, ref2):
    """
    Calculates error in 31R from gamma and kappa values.

    USAGE: error = check31r([gamma1, kappa],
            row,
            isotopeconstants,
            ref1,
            ref2)

    DESCRIPTION:
        Calculates 31R from eqn. (10) in Kelly et al. (in revision for RCMS);
        compares calculated 31R to measured 31R used to calculate gamma and kappa.

    INPUT:
        :param f: gamma and kappa
        :type f: list
        :param R: array with dimensions n x 10 where n is the number of reference pairs.
        The six columns are 31R, 45R, 46R, 15Rbulk, and 17R for reference #1, then
        the same for reference #2, from left to right.
        :type R: numpy array, dtype=float
        :param isotopeconstants: ref_tag, d15Na, and d15Nb of reference materials
            entered into the "scale_normalization" tab of the excel template
        :type isotopeconstants: Pandas Dataframe
        :param ref1: string or number containing name of reference material #1,
        as written in constants.csv
        :type ref1: str, int, or float
        :param ref2: string or number containing name of reference material #2,
        as written in constants.csv
        :type ref1: str, int, or float

    OUTPUT:
        :returns: Numpy Array with dimensions n x 2 where n is the number of measurements.
        The two columns are 31R error for ref 1 and ref 2, equal to (31R_calculated/31Rmeasured - 1)*1000

    @author: Colette L. Kelly (clkelly@stanford.edu).
    """
    # rename inputted data
    x = R[0]  # size-corrected 31/30 ratio for reference material #1
    r17 = R[4]  # 17R calculated iteratively from 45R and 46R for reference material #1

    x2 = R[5]  # size-corrected 31/30 ratio for reference material #2
    r172 = R[9]  # 17R calculated iteratively from 45R and 46R for reference material #2

    # these are the alpha and beta values for the two reference materials
    # they are specified in the data correction spreadsheet
    a, b, a2, b2 = constants_new(isotopeconstants, ref1, ref2)

    # solve two equations with two unknowns
    # f[0] = gamma, and f[1] = kappa
    
    calculated31r = [  # calculate 31R from gamma, kappa, 15Ralpha, 15Rbeta, and 17R in eqn. (10)
            (
                (1 - f[0]) * a
                + f[1] * b
                + a * b
                + (r17) * (1 + f[0] * a + (1 - f[1]) * b)
            )
            / (1 + f[0] * a + (1 - f[1]) * b),
            (
                (1 - f[0]) * a2
                + f[1] * b2
                + a2 * b2
                + (r172) * (1 + f[0] * a2 + (1 - f[1]) * b2)
            )
            / (1 + f[0] * a2 + (1 - f[1]) * b2),
        ]

    # express 31R error in per mil, where 31R error = (31R_calculated/31Rmeasured - 1)*1000
    error = np.array(
        [(calculated31r[0] / x - 1) * 1000, (calculated31r[1] / x2 - 1) * 1000]
    )

    print(error)

    return error
