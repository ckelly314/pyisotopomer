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


def SPnonlineq(f, R):
    """
    USAGE: v = least_squares(SPnonlineq, x0, bounds=bounds... args=args)
        Please see calcSPmain.py for definitions of these variables.

    DESCRIPTION:
        Uses values of 31R, 45R and 46R to iteratively solve for 15Ralpha and
        15R beta (see Frame and Casciotti, 2010, Appendix B).

    INPUT:
        R = array with dimensions n x 5 where n is the number of
        measurements.  The three columns are 31R, 45R, 46R, gamma,
        and kappa, from left to right.

    OUTPUT:
        F = array with dimensions n x 2 where n is the number of
        measurements.  The two columns are 15Ralpha and 15Rbeta from left to
        right.
    """

    # rename inputted data
    x = R[0]  # size-corrected 31R
    y = R[1]  # size-corrected 45R
    z = R[2]  # size-corrected 46R

    g = R[3]  # gamma scrambling coefficient
    k = R[4]  # gamma scrambling coefficient

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
