"""
File: automate_gk_eqns.py
-----------------------------
Created on Tues June 21, 2022

Algebraic solutions for gamma and kappa.

@author: Colette L. Kelly (clkelly@stanford.edu).
"""

import pandas as pd
import numpy as np
from .constants_new import constants_new  # import alpha and beta values for reference materials


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
        :param ref1: string or number containing name of reference material #1,
        as written in constants.csv
        :type ref1: str, int, or float
        :param ref2: string or number containing name of reference material #2,
        as written in constants.csv
        :type ref1: str, int, or float

    OUTPUT:
        :returns: Pandas DataFrame with dimensions n x 2 where n is the number of measurements.
        The two columns are gamma and kappa from left to right.

    @author: Colette L. Kelly (clkelly@stanford.edu).
    """
    # these are the alpha and beta values for the two reference materials
    # they are specified in constants.py
    a, b, a2, b2 = constants_new(isotopeconstants, ref1, ref2)

    # calculate difference in SPs of reference materials and print warning if too small
    spdiff = (a - b - a2 + b2) * 1000 / 0.0036765
    if np.abs(spdiff) < 50:
        print(
            "Difference in reference materials SPs may be too small for consistent results with the algebraic method."
        )
        print("Try setting method='least_squares'")
        print(f"SP1 - SP2 = {spdiff:.4} per mille")

    gammas = []  # add to these lists as we loop through the rows of the input array
    kappas = []

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
        gammas.append(gamma1)
        kappas.append(kappa)

    # return a dataframe of gamma and kappa values, same format as automate_gk_solver.py
    gk = pd.DataFrame([])
    gk["gamma"] = gammas
    gk["kappa"] = kappas

    return gk
