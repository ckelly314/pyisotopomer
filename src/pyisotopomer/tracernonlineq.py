"""
File: tracernonlineq.py
---------------------------
Created on Tues Dec 13, 2022

Functions to solve for N2O isotopocule values in 15N-labeled
tracer experiments.

@author: Colette L. Kelly (clkelly@stanford.edu).
"""


def tracernonlineq(f, R, isotopestandards): #, scrambling):
    """
    USAGE: v = least_squares(SPnonlineq, x0, bounds=bounds... args=args)
        Please see calcSPmain.py for definitions of these variables.

    DESCRIPTION:
        Uses values of 31R, 45R and 46R to iteratively solve for 15Ralpha and
        15R beta.

    INPUT:
        R = array with dimensions n x 8 where n is the number of
        measurements.  The three columns are 31R, 45R, 46R, cap17O, gamma,
        kappa, delta17O (calculated from t0's), and 46R added (calculated from t0s),
        from left to right.
        isotopestandards = IsotopeStandards class from isotopestandards.py,
        containing 15RAir, 18RVSMOW, 17RVSMOW, and beta for the 18O/17O relation.

    OUTPUT:
        F = array with dimensions n x 2 where n is the number of
        measurements.  The two columns are 15Ralpha and 15Rbeta from left to
        right.
    """

    # rename inputted data
    x = R[0]
    y = R[1]
    z = R[2]

    D17O = R[3]

    g = R[4]  # gamma scrambling coefficient
    k = R[5]  # gamma scrambling coefficient

    delta17O = R[6]
    r15addition = R[7]

    # known 17R
    r17 = (delta17O/1000 + 1)*0.0003799

    beta = isotopestandards.O17beta
    R17VSMOW = isotopestandards.R17VSMOW
    R18VSMOW = isotopestandards.R18VSMOW

    # solve two equations with two unknowns
    # f[0] = 15Ralpha = a, and f[2] = 15Rbeta = b
    F = [
        (f[0] + f[1]) * (y - f[0] - f[1]) # replacing (y - f[0] - f[1]) w/ r17 shouldn't make a difference
        +(R18VSMOW)
        * (((y - f[0] - f[1]) / R17VSMOW) / (D17O / 1000 + 1)) ** (1 / beta)
        + f[0] * f[1] # a*b term - assuming that a*b at this timepoint ~ a*b at t0
        + r15addition # added 46R
        - z,

        f[0] + f[1] + r17 - y, #  this is how we hold d17O (and d18O) constant

        (1 - g) * f[0]
        + k * f[1]
        + f[0] * f[1] # a*b term
        + r15addition
        + (y - f[0] - f[1]) * (1 + g * f[0] + (1 - k) * f[1])
        - x * (1 + g * f[0] + (1 - k) * f[1]),
    ]

    return F
