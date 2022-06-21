"""
File: calcSPmain.py
---------------------------
Created on Weds April 14th, 2021

Functions to solve for N2O isotopocule delta values, given
a set of IRMS scrambling coefficients (see pyScramble.py for
scripts to obtain scrambling coefficients).

@author: Cara Manning (cama@pml.ac.uk),
python version by Colette L. Kelly (clkelly@stanford.edu).
"""

import pandas as pd
import numpy as np
from scipy.optimize import least_squares
from .SPnonlineq import SPnonlineq


def calcSPmain(R, initialguess=None, lowerbounds=None, upperbounds=None):
    """
    USAGE: isotoperatios = calcSPmain(R)

    DESCRIPTION:
        Calculate 15Ralpha, 15Rbeta, 17R, and 18R from size-corrected isotope ratios
        and scrambling coefficients.

    INPUT:
        :param R: array with dimensions n x 5 where n is the number of
        measurements.  The three columns are 31R, 45R, 46R, gamma,
        and kappa, from left to right.
        :type R: numpy array, dtype=float
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

    #  python: need to set up empty dataframe to which we'll add values
    isol = pd.DataFrame([])

    bounds = (lb, ub)

    #  python: options for solver function are specified in signature as kwargs

    #  run leastsquares nonlinear solver for each row of data to obtain alpha
    #  and beta
    for n in range(len(R)):
        #  python: scipy.optimize.least_squares instead of matlab "lsqnonlin"
        row = np.array(R[n][:])
        args = (row,)
        # v = least_squares(automate_gk_eqns, x0, bounds=bounds,args=args)
        v = least_squares(
            SPnonlineq,
            x0,
            bounds=bounds,
            ftol=1e-15,
            xtol=1e-15,
            max_nfev=2000,
            args=args,
        )

        #  create a new array from the iterated solutions
        #  first column is gamma, second column is kappa
        isol = isol.append([v.x])

    # Calculate 17R (c) for the third column of isol
    isol[2] = R[:, 1] - isol[0] - isol[1]

    # Calculate 18R (d) for the fourth column of isol
    isol[3] = 0.0020052 * (isol[2] / 0.0003799) ** (1 / 0.516)

    # set column labels for isol
    isol = isol.rename(columns={0: "15Ralpha", 1: "15Rbeta", 2: "17R", 3: "18R"})

    return isol
