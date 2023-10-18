"""
File: automate_gk_eqns.py
-----------------------------
Created on Tues June 21, 2022

Algebraic solutions for gamma and kappa.

@author: Colette L. Kelly (clkelly@stanford.edu).
"""

import pandas as pd
import numpy as np
from .constants_new import (
    constants_new,
)  # import alpha and beta values for reference materials
from .automate_gk_eqns import (
    automate_gk_eqns,
)
from .check31r import check31r


def algebraic_gk_eqns(R, isotopeconstants, ref1, ref2):
    """
    Calculates gamma and kappa from algebraic solution for each parameter,
    using the known 15Ralpha and 15Rbeta and measured 31/30R and 17R of two
    reference materials.

    USAGE: gk = algebraic_gk_eqns(R, ref1=ref1, ref2=ref2)

    DESCRIPTION:
        Sets up equations for gamma and kappa as in Kelly et al. (in revision for RCMS).

    INPUT:
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
        :returns: Pandas DataFrame with dimensions n x 4, where n is the number of measurements.
        The four columns are gamma, kappa, ref 1 31R error, and ref 2 31R error,
        from left to right.

    @author: Colette L. Kelly (clkelly@stanford.edu).
    """
    # these are the alpha and beta values for the two reference materials
    # they are specified in the data correction spreadsheet
    a, b, a2, b2 = constants_new(isotopeconstants, ref1, ref2)

    gk = np.zeros((len(R), 4))  # set up numpy array to populate with solutions

    for n in range(len(R)):
        # I'm still not sure why, but looping through the rows prevents an IndexError
        row = np.array(R[n][:])
        # rename inputted data
        x = row[0]  # size-corrected 31/30 ratio for reference material #1
        r17 = row[
            4
        ]  # 17R calculated iteratively from 45R and 46R for reference material #1

        x2 = row[5]  # size-corrected 31/30 ratio for reference material #2
        r172 = row[
            9
        ]  # 17R calculated iteratively from 45R and 46R for reference material #2

        # algebraic solutions for gamma and kappa
        kappa = (
            (a - x + r17) * (1 + b) / (a * (1 + x - r17))
            - (a2 - x2 + r172) * (1 + b2) / (a2 * (1 + x2 - r172))
        ) / (b2 / a2 - b / a)
        gamma1 = (a + kappa * b + a * b - (x - r17) * (1 + (1 - kappa) * b)) / (
            a * (1 + x - r17)
        )
        gamma2 = (a2 + kappa * b2 + a2 * b2 - (x2 - r172) * (1 + (1 - kappa) * b2)) / (
            a2 * (1 + x2 - r172)
        )

        # print(gamma1 - gamma2) # the two gamma values should be within machine precision of each other

        error = check31r([gamma1, kappa], row, isotopeconstants, ref1, ref2)

        gk[n][0] = gamma1  # populate numpy array with solutions
        gk[n][1] = kappa
        gk[n][
            2:
        ] = error  # 31R error for gamma and kappa solutions, (31R_calculated/31Rmeasured - 1)*1000

    # return a dataframe of gamma and kappa values, same format as automate_gk_solver.py
    gkdf = pd.DataFrame(gk).rename(
        columns={0: "gamma", 1: "kappa", 2: "error1", 3: "error2"}
    )

    return gkdf
