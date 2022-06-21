"""
File: automate_gk_eqns.py
---------------------------------
Created on Tues June 21, 2022

Algebraic solutions for gamma and kappa.

@author: Colette L. Kelly (clkelly@stanford.edu).
"""

import pandas as pd
import numpy as np
from .constants import constants  # import alpha and beta values for reference materials


def algebraic_gk_eqns(R, ref1, ref2):
    """
    Calculates gamma and kappa from measured rR31/30, given known a, b, 17R.

    USAGE: v = least_squares(automate_gk_eqns, x0, bounds=bounds... args=args)
        See automate_gk_solver for solver arg descriptions.

    DESCRIPTION:
        Sets up equations as in Frame and Casciotti (2010), Appendix B,
        to iteratively solve for gamma and kappa (scrambling coefficients).

    INPUT:
        :param f: guesses for g and k
        :type f: list
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
        :param weights: list or array containing weights for each reference material
        to be multiplied by their respective cost equations
        :type weights: list or array [weight1, weight2]

    OUTPUT:
        :returns: [gamma, kappa]

    @author: Colette L. Kelly (clkelly@stanford.edu).
    """
    # these are the alpha and beta values for the two reference materials
    # they are specified in constants.py
    a, b, a2, b2 = constants(ref1, ref2)

    spdiff = (a - b - a2 + b2)*1000/0.0036765
    if spdiff < 50:
        print("Difference in reference materials SPs may be too small for consistent results with the algebraic method:")
        print(f"SP1 - SP2 = {spdiff:.4} per mille")

    gammas = []
    kappas = []
    
    for n in range(len(R)):
        # I'm still not sure why, but looping through the rows prevents an IndexError
        row = np.array(R[n][:])
        # rename inputted data
        x = row[0]  # size-corrected 31/30 ratio for reference material #1
        y = row[1]  # size-corrected 45/44 ratio for reference material #1
        r17 = row[4]  # 17R calculated iteratively from 45R and 46R for reference material #1

        x2 = row[5]  # size-corrected 31/30 ratio for reference material #2
        y2 = row[6]  # size-corrected 45/44 ratio for reference material #2
        r172 = row[9]  # 17R calculated iteratively from 45R and 46R for reference material #2

        # solve two equations with two unknowns
        kappa = ((a-x+r17)*(1+b)/(a*(1+x-r17)) - (a2-x2+r172)*(1+b2)/(a2*(1+x2-r172)))/(b2/a2-b/a)
        gamma1 = (a+kappa*b+a*b-(x-r17)*(1+(1-kappa)*b))/(a*(1+x-r17))
        gamma2 = (a2+kappa*b2+a2*b2-(x2-r172)*(1+(1-kappa)*b2))/(a2*(1+x2-r172))

        #print(gamma1 - gamma2) # the two gamma values should be within machine precision of each other
        gammas.append(gamma1)
        kappas.append(kappa)

    gk = pd.DataFrame([])
    gk["gamma"] = gammas
    gk["kappa"] = kappas

    return gk
