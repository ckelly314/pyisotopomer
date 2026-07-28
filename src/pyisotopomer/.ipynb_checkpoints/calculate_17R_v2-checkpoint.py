"""
File: calculate_17R_v2.py
------------------------------------
Created on Wednesday, August 31 2022

Solve for 15Rbulk and 18R values from measured 45R and 46R
of reference materials, then calculate 17R from 18R.
Obtain 17R values consistent with both 45R and 46R to use in
scrambling calculation.

@author: Colette L. Kelly (clkelly@stanford.edu).
"""

# import utils
import pandas as pd
import numpy as np

# for solving equations for 15R and 17R
from scipy.optimize import least_squares


def bulknonlineq(f, R, isotopestandards):
    """
    Equations to solver for 15Rav, 18R and 17R from 45R and 46R.
    """

    # rename inputted data
    x = R[0]  # size-corrected 31R
    y = R[1]  # size-corrected 45R
    z = R[2]  # size-corrected 46R
    D17O = R[3]

    beta = isotopestandards.O17beta
    R17VSMOW = isotopestandards.R17VSMOW
    R18VSMOW = isotopestandards.R18VSMOW

    # solve two equations with two unknowns
    # f[0] = 15R, and f[1] = 18R
    F = [  # 45R = 2*15R + 17R
        2 * f[0]
        + R17VSMOW * ((f[1] / R18VSMOW) ** beta) * (D17O / 1000 + 1)
        - y,  # phrase 17R in terms of 18R
        # 46R ~ 18R + 2*15R*17R + 15R^2
        f[1]
        + 2 * f[0] * (R17VSMOW * ((f[1] / R18VSMOW) ** beta) * (D17O / 1000 + 1))
        + f[0] ** 2
        - z,
    ]

    return F


def calcdeltabulk(isol, isotopestandards):
    """
    Convert 15Rav, 18R and 17R to delta values.
    """

    beta = isotopestandards.O17beta
    R15Air = isotopestandards.R15Air
    R17VSMOW = isotopestandards.R17VSMOW
    R18VSMOW = isotopestandards.R18VSMOW

    # Calculate d15N referenced to AIR
    d15N = 1000 * (isol["15Rbulk"] / R15Air - 1)

    # Calculate d17O and d18O referenced to VSMOW
    d17O = 1000 * (isol["17R"] / R17VSMOW - 1)
    d18O = 1000 * (isol["18R"] / R18VSMOW - 1)

    # Create array of isotope data and return
    deltaVals = np.array([d15N, d17O, d18O]).T
    deltaVals = pd.DataFrame(deltaVals, columns=["d15Nbulk", "d17O", "d18O"])

    return deltaVals


def calculate_17R(R, isotopestandards):
    """
    USAGE: r17array = calculate_17R(sizecorrected, isotopestandards)

    DESCRIPTION:
        Solve for 15Rbulk and 17R values from measured 45R and 46R
        of reference materials, to obtain 17R values consistent with
        both 45R and 46R to use in scrambling calculation.

    INPUT:
        :param R: array with dimensions n x 4 where n is the number of
        measurements.  The four columns are 31R, 45R, 46R, and D17O,
        from left to right.
        :type R: numpy array, dtype=float
        :param IsotopeStandards: IsotopeStandards class from isotopestandards.py,
        containing 15RAir, 18RVSMOW, 17RVSMOW, and beta for the 18O/17O relation.
        :type isotopestandards: Class

    OUTPUT:
        :param isol: array with dimensions n x 2, where n is the number of
        measurements. The two columns are the estimated 15Rbulk and 17R,
        from left to right.
        :type isol: Numpy array

    @author: Colette L. Kelly (clkelly@stanford.edu).
    """
    x0 = np.array(
        [0.0036765, 0.002094030360]
    )  # 18R initial guess is that of atmospheric N2O

    isol = np.zeros((len(R), 2))  # set up numpy array to populate with solutions.

    beta = isotopestandards.O17beta
    R15Air = isotopestandards.R15Air
    R17VSMOW = isotopestandards.R17VSMOW
    R18VSMOW = isotopestandards.R18VSMOW

    #  run leastsquares nonlinear solver for each row of data to obtain 15Rav and 17R

    for n in range(len(R)):
        row = np.array(R[n][:])
        args = (row, isotopestandards)

        v = least_squares(
            bulknonlineq,
            x0,
            bounds=([0, 0], [1, 1]),
            ftol=1e-15,
            xtol=1e-15,
            max_nfev=2000,
            args=args,
            verbose=0,
        )

        #  create a new array from the iterated solutions
        #  first column is 15Rav, second column is 17R
        isol[n][:] = v.x

    r17array = np.zeros(
        (len(R), 3)
    )  # set up output array with 3 cols, for 15Rav, 17R, and 18R
    r17array[:, 0] = isol[:, 0]
    r17array[:, 1] = isol[:, 1]
    r17array[:, 2] = R17VSMOW * ((isol[:, 1] / R18VSMOW) ** beta) * (R[:, 3] / 1000 + 1)

    # convert to Pandas DataFrame to save out
    saveout = pd.DataFrame(isol).rename(columns={0: "15Rbulk", 1: "18R"})

    saveout["D17O"] = R[:, 3]

    # calculate r17 from r18
    saveout["17R"] = (
        R17VSMOW * ((saveout["18R"] / R18VSMOW) ** beta) * (saveout["D17O"] / 1000 + 1)
    )

    saveout.to_csv("normalized_ratios.csv")  # saveout isotope ratios to .csv file
    # want the delta values as check values
    calcdeltabulk(saveout, isotopestandards).to_csv("normalized_deltas.csv")

    return r17array
