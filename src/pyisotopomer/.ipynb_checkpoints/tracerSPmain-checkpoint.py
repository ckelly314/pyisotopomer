"""
File: calcSPmain.py
---------------------------
Created on Tues Dec 13th, 2022

Functions to solve for N2O isotopocule values in 15N-labeled
tracer experiments.

@author: Colette L. Kelly (clkelly@stanford.edu).
"""

import pandas as pd
import numpy as np
import warnings
from scipy.optimize import least_squares
from .tracernonlineq import tracernonlineq


def tracerSPmain(
    R, isotopestandards, initialguess=None, lowerbounds=None, upperbounds=None
):
    """
    Calculate gamma and kappa from measured rR31/30 and r45/44, given known a, b, 17R.

    USAGE: gk = automate_gk_solver(R,ref1=ref1, ref2=ref2)

    DESCRIPTION:
        Uses known values of alpha, beta, and 17R for two sample gases and one
        standard gas, plus measured rR31/30 for sample and standard gases,
        to calculate scrambling coefficients gamma and kappa.

    INPUT:
        :param R: array with dimensions n x 8 where n is the number of
        measurements.  The three columns are 31R, 45R, 46R, cap17O, gamma,
        kappa, delta17O (calculated from t0's), and 46R added (calculated from t0s),
        from left to right.
        :type R: numpy array, dtype=float
        :param IsotopeStandards: IsotopeStandards class from isotopestandards.py,
        containing 15RAir, 18RVSMOW, 17RVSMOW, and beta for the 18O/17O relation.
        :type isotopestandards: Class
        :param initialguess: Initial guess for 15Ralpha and 15Rbeta
        If None, default to [0.0037, 0.0037].
        :type initialguess: list or Numpy array
        :param lowerbounds: Lower bounds for least_squares solver
        If None, default to [0.0, 0.0].
        :type lowerbounds: list or Numpy array
        :param upperbounds: Upper bounds for least_squares solver
        If None, default to [1.0, 1.0].
        :type upperbounds: list or Numpy array
    OUTPUT:
        :returns: pandas DataFrame with dimensions n x 4 where n is the number of measurements.
        The four columns are 15Ralpha, 15Rbeta, 17R and 18R from left to right.

    @author: Colette L. Kelly (clkelly@stanford.edu).
    """

    # default arguments
    # an approximate initial solution: initial guess for 15Ralpha and 15Rbeta
    if initialguess is not None:
        x0 = np.array(initialguess, dtype=float)
    elif initialguess is None:
        x0 = np.array([0.0037, 0.0037], dtype=float)
    # lower and upperbounds for 15Ralpha and 15Rbeta
    # these constraints ensure that the solver converges to a solution in the
    # correct range
    if lowerbounds is not None:
        lb = np.array(lowerbounds, dtype=float)
    elif lowerbounds is None:
        lb = np.array([0.0, 0.0], dtype=float)

    if upperbounds is not None:
        ub = np.array(upperbounds, dtype=float)
    elif upperbounds is None:
        ub = np.array([1.0, 1.0], dtype=float)

    beta = isotopestandards.O17beta
    R17VSMOW = isotopestandards.R17VSMOW
    R18VSMOW = isotopestandards.R18VSMOW

    #  python: need to set up empty dataframe to which we'll add values
    # isol = pd.DataFrame([])
    isol = np.zeros((len(R), 2))  # set up numpy array to populate with solutions.

    bounds = (lb, ub)

    #  python: options for solver function are specified in signature as kwargs

    #  run leastsquares nonlinear solver for each row of data to obtain alpha
    #  and beta
    for n in range(len(R)):
        #  python: scipy.optimize.least_squares instead of matlab "lsqnonlin"
        row = np.array(R[n][:])
        args = (row, isotopestandards)
        try:  # try different initial guesses to account for samples w/ extreme delta values
            with warnings.catch_warnings():  # suppress RuntimeWarning when it can't find a solution
                warnings.simplefilter("ignore")
                v = least_squares(
                    tracernonlineq,
                    x0,
                    bounds=bounds,
                    ftol=1e-15,
                    xtol=1e-15,
                    max_nfev=2000,
                    args=args,
                )
        except ValueError:  # try finding a solution with initial guess = 0,0
            print(f"row {n+3}: initial guess set to 0")
            v = least_squares(
                tracernonlineq,
                np.array([0.0, 0.0]),
                bounds=bounds,
                ftol=1e-15,
                xtol=1e-15,
                max_nfev=2000,
                args=args,
            )
        #  create a new array from the iterated solutions
        #  first column is gamma, second column is kappa
        isol[n][:] = v.x

    # set column labels for isol
    isol = pd.DataFrame(isol).rename(columns={0: "15Ralpha", 1: "15Rbeta"})

    # Calculate 17R
    isol["17R"] = R[:, 1] - isol["15Ralpha"] - isol["15Rbeta"]

    # add D17O
    isol["D17O"] = R[:, 3]

    # Calculate 18R (d) for the fourth column of isol
    isol["18R"] = R18VSMOW * ((isol["17R"] / R17VSMOW) / (isol["D17O"] / 1000 + 1)) ** (
        1 / beta
    )

    return isol
