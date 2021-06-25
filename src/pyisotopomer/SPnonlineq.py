"""
File: SPnonlineq.py
---------------------------
Created on Weds April 14th, 2021

Functions to solve for N2O isotopocule delta values, given
a set of IRMS scrambling coefficients (see pyScramble.py for
scripts to obtain scrambling coefficients).

@author: Cara Manning (cama@pml.ac.uk),
python version by Colette L. Kelly (clkelly@stanford.edu).
"""


def SPnonlineq(f, R, scrambling):
    """
    USAGE: v = least_squares(SPnonlineq, x0, bounds=bounds... args=args)
        Please see calcSPmain.py for definitions of these variables.

    DESCRIPTION:
        Uses values of 31R, 45R and 46R to iteratively solve for 15Ralpha and
        15R beta (see Frame and Casciotti, 2010, Appendix B).

    INPUT:
        R = array with dimensions n x 3 where n is the number of
        measurements.  The three columns are 31R, 45R and 46R from left to
        right.

    OUTPUT:
        F = array with dimensions n x 2 where n is the number of
        measurements.  The two columns are 15Ralpha and 15Rbeta from left to
        right.
    """

    # rename inputted data
    x = R[0]
    y = R[1]
    z = R[2]

    # pull scrambling coefficients
    g = scrambling[0]
    k = scrambling[1]

    # calibrated sample: atmosphere-equilibrated seawater
    a = 0.003734221050  # alpha, from "N2Ocalibrationsummary.xlsx"
    b = 0.003664367550  # beta

    # calibrated sample: Toyoda Lab S2
    a2 = 0.003696905  # alpha
    b2 = 0.003629183  # beta

    # solve two equations with two unknowns
    # f[0] = 15Ralpha = a, and f[2] = 15Rbeta = b
    F = [
        (f[0] + f[1]) * (y - f[0] - f[1])
        + (0.0020052) * ((y - f[0] - f[1]) / 0.0003799) ** (1 / 0.516)
        + f[0] * f[1]
        - z,
        (1 - g) * f[0]
        + k * f[1]
        + f[0] * f[1]
        + (y - f[0] - f[1]) * (1 + g * f[0] + (1 - k) * f[1])
        - x * (1 + g * f[0] + (1 - k) * f[1]),
    ]

    return F
