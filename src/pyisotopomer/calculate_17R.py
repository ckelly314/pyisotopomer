"""
File: calculate_17R.py
-------------------------------
Created on Monday, June 20 2022

Solve for 15Rbulk and 17R values from measured 45R and 46R
of reference materials, to obtain 17R values consistent with
both 45R and 46R to use in scrambling calculation.

@author: Colette L. Kelly (clkelly@stanford.edu).
"""

# import utils
import pandas as pd
import numpy as np

# for solving equations for 15R and 17R
from scipy.optimize import least_squares


def bulknonlineq(f, R, IsotopeStandards):
    """
    Equations to solver for 15Rav, 18R and 17R from 45R and 46R.
    """

    # rename inputted data
    x = R[0]  # size-corrected 31R
    y = R[1]  # size-corrected 45R
    z = R[2]  # size-corrected 46R
    D17O = R[3]

    # solve two equations with two unknowns
    # f[0] = 15R, and f[1] = 17R
    F = [
        2 * f[0] + f[1] - y,  # 45R = 2*15R + 17R
        # 46R ~ 18R + 2*15R*17R + 15R^2
        IsotopeStandards.R18VSMOW * ((f[1] / IsotopeStandards.R17VSMOW) ) ** (1 / IsotopeStandards.O17slope)  # 18R expressed in terms of 17R
        + 2 * f[0] * f[1]  # 2*15R*17R
        + f[0] ** 2  # 15R^2
        - z,
    ]

    return F


def calcdeltabulk(isol, IsotopeStandards):
    """
    Convert 15Rav, 18R and 17R to delta values.
    """

    # Calculate d15N referenced to AIR
    d15N = 1000 * (
        isol["15Rbulk"] / IsotopeStandards.R15Air - 1
    )

    # Calculate d17O and d18O referenced to VSMOW
    d17O = 1000 * (
        isol["17R"] / IsotopeStandards.R17VSMOW - 1
    )
    d18O = 1000 * (
        isol["18R"] / IsotopeStandards.R18VSMOW - 1
    )

    # Create array of isotope data and return
    deltaVals = np.array([d15N, d17O, d18O]).T
    deltaVals = pd.DataFrame(deltaVals, columns=["d15Nbulk", "d17O", "d18O"])

    return deltaVals


def calculate_17R(R, IsotopeStandards):

    x0 = np.array([IsotopeStandards.R15Air, IsotopeStandards.R17VSMOW])  # initial guess for 15Rav and 17R

    isol = np.zeros((len(R), 2))  # set up numpy array to populate with solutions.

    #  run leastsquares nonlinear solver for each row of data to obtain 15Rav and 17R

    for n in range(len(R)):
        row = np.array(R[n][:])
        args = (row, IsotopeStandards)

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


    # convert to Pandas DataFrame to save out - is this necessary?
    saveout = pd.DataFrame(isol).rename(columns={0: "15Rbulk", 1: "17R"})

    saveout["D17O"] = R[:, 3]

    # calculate r18 from r17
    saveout["18R"] = IsotopeStandards.R18VSMOW * ((saveout["17R"] / IsotopeStandards.R17VSMOW)) ** (
        1 / IsotopeStandards.O17slope
    )  # 18R expressed in terms of 17R

    print((saveout["18R"]/0.002052 - 1)*1000)
    #print(IsotopeStandards.R18VSMOW)

    saveout.to_csv("normalized_ratios.csv")  # saveout isotope ratios to .csv file
    # want the delta values as check values
    calcdeltabulk(saveout, IsotopeStandards).to_csv("normalized_deltas.csv")

    return isol
