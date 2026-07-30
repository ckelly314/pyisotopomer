"""
File: automate_gk_solver.py
---------------------------
Created on Weds April 14th, 2021

Functions to solve for IRMS scrambling coefficients to be used in
isotopomer calculations.

@author: Colette L. Kelly (clkelly@stanford.edu).
"""


import pandas as pd
import numpy as np
from scipy.optimize import least_squares
from .automate_gk_eqns import (
    automate_gk_eqns,
)  # import alpha and beta values for reference materials
from .check31r import check31r


def automate_gk_solver(
    R, isotopeconstants, ref1, ref2, x0=None, lb=None, ub=None, weights=False
):
    """
    Calculate gamma and kappa from measured rR31/30 and r45/44, given known a, b, 17R.

    USAGE: gk = automate_gk_solver(R,ref1=ref1, ref2=ref2)

    DESCRIPTION:
        Uses known values of alpha, beta, and 17R for two sample gases and one
        standard gas, plus measured rR31/30 for sample and standard gases,
        to calculate scrambling coefficients gamma and kappa.

    INPUT:
        :param R: array with dimensions n x 10 where n is the number of reference pairs.
        The six columns are 31R, 45R, 46R, 15Rbulk, and 17R for reference #1, then
        the same for reference #2, from left to right.
        :type R: numpy array, dtype=float
        :param isotopeconstants: ref_tag, d15Na, and d15Nb of reference materials
            entered into the "scale_normalization" tab of the excel template
        :type isotopeconstants: Pandas Dataframe
        :param x0: initial guess for gamma and kappa (e.g. x0=np.array([0.1, 0.1], dtype=float))
        :type x0: numpy array, dtype=float
        :param lb: lower bounds for solver (e.g. lb=np.array([0.0, 0.0], dtype=float))
        :type lb: numpy array, dtype=float
        :param ub: upper bounds for solver (e.g. ub=np.array([1.0, 1.0], dtype=float))
        :type ub: numpy array, dtype=float
        :param weights: if True, weight each ref. material by variance in its 31R
        :type weights: bool

    OUTPUT:
        :returns: Pandas DataFrame with dimensions n x 4, where n is the number of measurements.
        The four columns are gamma, kappa, ref 1 31R error, and ref 2 31R error,
        from left to right.

    @author: Colette L. Kelly (clkelly@stanford.edu).
    """
    #  python: need to set up empty dataframe to which we'll add values
    gk = np.zeros((len(R), 4))  # set up numpy array to populate with solutions

    #  an approximate initial solution: initial guess for gamma and kappa
    if x0 is not None:  # check if solver has been given an x0 parameter
        x0 = x0
    else:
        x0 = np.array([0.1, 0.1], dtype=float)  # set default x0

    #  lower and upperbounds for 15Ralpha and 15Rbeta
    #  these constraints ensure that the solver converges to a solution in the
    #  correct range
    if lb is not None:
        lb = lb
    else:
        lb = np.array([0.0, 0.0], dtype=float)

    if ub is not None:
        ub = ub
    else:
        ub = np.array([1.0, 1.0], dtype=float)

    bounds = (lb, ub)

    if weights == True:  # if variance kwarg is True, calculate weights
        if (np.var(R[:, 0]) != 0) & (np.var(R[:, 3]) != 0):  # if variance isn't zero
            # calculate variance of each ref. material's 31R as a proportion of total variance
            var1percent = np.var(R[:, 0]) / (np.var(R[:, 0]) + np.var(R[:, 3]))
            var2percent = np.var(R[:, 3]) / (np.var(R[:, 0]) + np.var(R[:, 3]))
            # invert variances to obtain weights
            weights = [1.0 / var1percent, 1.0 / var2percent]

            print(f"{ref1} weight = {1./var1percent}\n{ref2} weight = {1./var2percent}")

        else:
            weights = [1.0, 1.0]  # if variances are zero, set weights to 1

    elif weights == False:

        weights = [1.0, 1.0]  # if variance kwarg is False, set weights to 1

    #  python: options for solver function are specified in signature as kwargs

    #  run leastsquares nonlinear solver for each row of data to obtain alpha
    #  and beta
    for n in range(len(R)):
        #  python: scipy.optimize.least_squares instead of matlab "lsqnonlin"
        row = np.array(R[n][:])
        args = (
            row,
            isotopeconstants,
            ref1,
            ref2,
            weights,
        )
        # v = least_squares(automate_gk_eqns, x0, bounds=bounds,args=args)
        v = least_squares(
            automate_gk_eqns,
            x0,
            bounds=bounds,
            ftol=1e-15,
            xtol=1e-15,
            max_nfev=2000,
            args=args,
        )

        error = check31r(v.x, row, isotopeconstants, ref1, ref2)

        #  fill in array  with the iterated solutions & corresponding error
        gk[n][:2] = v.x  #  first column is gamma, second column is kappa
        gk[n][
            2:
        ] = error  # third & fourth columns are ref 1 31R error & ref 2 31R error

    gkdf = pd.DataFrame(gk).rename(
        columns={0: "gamma", 1: "kappa", 2: "error1", 3: "error2"}
    )

    return gkdf
