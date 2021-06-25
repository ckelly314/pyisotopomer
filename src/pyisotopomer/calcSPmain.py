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


def calcSPmain(R, scrambling):
    """
    Calculate gamma and kappa from measured rR31/30 and r45/44, given known a, b, 17R.

    USAGE: gk = automate_gk_solver(R,ref1=ref1, ref2=ref2)

    DESCRIPTION:
        Uses known values of alpha, beta, and 17R for two sample gases and one
        standard gas, plus measured rR31/30 for sample and standard gases,
        to calculate scrambling coefficients gamma and kappa.

    INPUT:
        :param R: array with dimensions n x 6 where n is the number of reference pairs.
        The six columns are 31R, 45R and 46R for reference #1, then 31R, 45R, 46R for reference #2, from left to right.
        :type R: numpy array, dtype=float
        :param x0: initial guess for gamma and kappa (e.g. x0=np.array([0.17, 0.08], dtype=float))
        :type x0: numpy array, dtype=float
        :param lb: lower bounds for solver (e.g. lb=np.array([0.0, 0.0], dtype=float))
        :type lb: numpy array, dtype=float
        :param ub: upper bounds for solver (e.g. ub=np.array([1.0, 1.0], dtype=float))
        :type ub: numpy array, dtype=float

    OUTPUT:
        :returns: pandas DataFrame with dimensions n x 4 where n is the number of measurements.
        The four columns are 15Ralpha, 15Rbeta, 17R and 18R from left to right.

    @author: Colette L. Kelly (clkelly@stanford.edu).
    """

    #  python: need to set up empty dataframe to which we'll add values
    isol = pd.DataFrame([])

    # an approximate initial solution: initial guess for 15Ralpha and 15Rbeta
    x0 = np.array([0.0037, 0.0037], dtype=float)

    # lower and upperbounds for 15Ralpha and 15Rbeta
    # these constraints ensure that the solver converges to a solution in the
    # correct range
    lb = np.array([0.00, 0.00], dtype=float)
    ub = np.array([1.0, 1.0], dtype=float)

    bounds = (lb, ub)

    #  python: options for solver function are specified in signature as kwargs

    #  run leastsquares nonlinear solver for each row of data to obtain alpha
    #  and beta
    for n in range(len(R)):
        #  python: scipy.optimize.least_squares instead of matlab "lsqnonlin"
        row = np.array(R[n][:])
        args = (
            row,
            scrambling,
        )
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
