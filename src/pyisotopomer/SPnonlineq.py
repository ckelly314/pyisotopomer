"""
File: SPnonlineq.py
---------------------------
Created on Weds April 14th, 2021

Functions to solve for N2O isotopocule values.

@author: Cara Manning (cama@pml.ac.uk),
python version by Colette L. Kelly (clkelly@stanford.edu).
"""


def SPnonlineq(f, R, isotopestandards):
    """
    USAGE: v = least_squares(SPnonlineq, x0, bounds=bounds... args=args)
        Please see calcSPmain.py for definitions of these variables.

    DESCRIPTION:
        Uses values of 31R, 45R and 46R to iteratively solve for 15Ralpha and
        15R beta.

    INPUT:
        R = array with dimensions n x 6 where n is the number of
        measurements.  The three columns are 31R, 45R, 46R, D17O, gamma,
        and kappa, from left to right.
        isotopestandards = IsotopeStandards class from isotopestandards.py,
        containing 15RAir, 18RVSMOW, 17RVSMOW, and beta for the 18O/17O relation.

    OUTPUT:
        F = array with dimensions n x 2 where n is the number of
        measurements.  The two columns are 15Ralpha and 15Rbeta from left to
        right.
    """

    # rename inputted data
    x = R[0]  # size-corrected 31R
    y = R[1]  # size-corrected 45R
    z = R[2]  # size-corrected 46R
    D17O = R[3]

    g = R[4]  # gamma scrambling coefficient
    k = R[5]  # gamma scrambling coefficient

    beta = isotopestandards.O17beta
    R17VSMOW = isotopestandards.R17VSMOW
    R18VSMOW = isotopestandards.R18VSMOW

    # solve two equations with two unknowns
    # f[0] = 15Ralpha = a, and f[2] = 15Rbeta = b
    F = [
        (f[0] + f[1]) * (y - f[0] - f[1])
        + (R18VSMOW)
        * (((y - f[0] - f[1]) / R17VSMOW) / (D17O / 1000 + 1)) ** (1 / beta)
        + f[0] * f[1]
        - z,
        (1 - g) * f[0]
        + k * f[1]
        + f[0] * f[1]
        + (y - f[0] - f[1]) * (1 + g * f[0] + (1 - k) * f[1])
        - x * (1 + g * f[0] + (1 - k) * f[1]),
    ]

    return F
