"""
File: parseoutput.py
---------------------------
Created on Tues June 8th, 2021

Functions to parse output from scrambling solver.

@author: Colette L. Kelly (clkelly@stanford.edu).
"""

# import utils
import pandas as pd
import numpy as np
from .automate_gk_solver import automate_gk_solver


def parseoutput(inputobj, initialguess=None, lowerbounds=None, upperbounds=None):
    """
    Parse output from scrambling solver.

    USAGE: self.outputs, self.pairings, self.alloutputs = parseoutput.parseoutput(self.inputobj)

    DESCRIPTION:
        Takes in an Input class from parseinput.py, extracts arrays of isotope ratios,
        and calls automate_gk_solver.py.

    INPUT:
        :param inputobj: Input class from parseinput.py
        :type inputobj: Class
        :param initialguess: Initial guess for gamma and kappa.
        If None, default to [0.17, 0.08].
        :type initialguess: list or Numpy array
        :param lowerbounds: Lower bounds for automate_gk_solver.
        If None, default to [0.0, 0.0].
        :type lowerbounds: list or Numpy array
        :param upperbounds: Upper bounds for automate_gk_solver.
        If None, default to [1.0, 1.0].
        :type upperbounds: list or Numpy array

    OUTPUT:
        :returns: outputdfs, dfnames, maindf
        :param outputdfs: Tables of scrambling coefficients for each pairing of ref. materials.
        :type outputdfs: List of Pandas DataFrames
        :param dfnames: List of ref. material pairings generated from parseinputs
        :type dfnames: List of tuples
        :param maindf: One table of all scrambling coefficients for all pairings.
        :type maindf: Pandas DataFrame

    @author: Colette L. Kelly (clkelly@stanford.edu).
    """

    # default arguments
    if initialguess is not None:
        initialguess = np.array(initialguess, dtype=float)
    elif initialguess is None:
        initialguess = np.array([0.17, 0.08], dtype=float)

    if lowerbounds is not None:
        lowerbounds = np.array(lowerbounds, dtype=float)
    elif lowerbounds is None:
        lowerbounds = np.array([0.0, 0.0], dtype=float)

    if upperbounds is not None:
        upperbounds = np.array(upperbounds, dtype=float)
    elif upperbounds is None:
        upperbounds = np.array([1.0, 1.0], dtype=float)

    # set up outputs
    outputdfs = []  # list of output DataFrames for each pairing of ref. materials
    dfnames = []  # list of each pairing of ref. materials as strings
    maindf = pd.DataFrame(
        [],
        columns=[
            "ref_tag_1",
            "size corrected 31R_1",
            "size corrected 45R_1",
            "size corrected 46R_1",
            "ref_tag_2",
            "size corrected 31R_2",
            "size corrected 45R_2",
            "size corrected 46R_2",
            "gamma",
            "kappa",
        ],
    )

    # loop through pairings of reference materials by popping items off input dict
    while True:
        if not inputobj.scrambleinput:  # stop the loop when dict is empty
            break

        # each entry in the input dict contains the names of ref materials,
        # input array for gk_solver,
        # and output DataFrame of paired reference materials
        key, [ref1, ref2, R, df] = inputobj.scrambleinput.popitem()
        # print(key)

        try:  # Run function that iteratively solves for gamma and kappa
            gk = automate_gk_solver(
                R, ref1=ref1, ref2=ref2, x0=initialguess, lb=lowerbounds, ub=upperbounds
            )

            try:
                # attach scrambling coeffs to output dataframe
                df["gamma"] = np.array(gk.gamma)
                df["kappa"] = np.array(gk.kappa)

                # write each output dataframe to a separate sheet in the output spreadsheet
                outputdfs.append(df)
                dfnames.append(f"{ref1}-{ref2}")
                maindf = maindf.append(df)

            except AttributeError:
                print(f"{ref1} and/or {ref2} have not been entered in constants.csv")

        except ValueError:
            print(
                "Please ensure constants.csv is saved in the current working directory\n"
            )

    return outputdfs, dfnames, maindf
