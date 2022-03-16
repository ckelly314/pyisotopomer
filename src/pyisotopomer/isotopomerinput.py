"""
File: isotopomerinput.py
---------------------------
Created on Weds June 2nd, 2021

Functions and Input class to read in and parse data
from excel template.

@author: Colette L. Kelly (clkelly@stanford.edu).
"""


import pandas as pd
import numpy as np
from itertools import combinations


class IsotopomerInput:
    """
    Read in the scrambling template spreadsheet and generate pairings of reference materials.

    USAGE: inputobj = parseinput.Input(inputfilename, ref1, ref2, ref3)

    DESCRIPTION:
        Uses itertools from the Python standard libraries to generate
        all possible pairings of reference materials from the input spreadsheet.
        Uses Pandas "join" to merge size-corrected isotope ratios for each pairing.

    INPUT:
        :param filename: filename for spreadsheet template, e.g. "00_excel_template.xlsx"
        :type R: string

    OUTPUT:
        :returns: dict with {key: [ref1, ref2, R, df]} for each reference material pairing.
        R is a Numpy array of size-corrected values to be input to automate_gk_solver.py.
        df is a Pandas DataFrame of dates, size-corrected values, and ref tags.

    @author: Colette L. Kelly (clkelly@stanford.edu).
    """

    def __init__(self, filename):

        self.filename = filename

        # full contents of excel template, first tab
        self.data = self.readin(filename)

        # subset of data to be used for Isotopomers
        self.sizecorrected = self.parseratios(self.data)

        self.ratiosscrambling = self.parseisotopomerinput(self.data)

    def readin(self, filename):
        # return Pandas DataFrame of all input data
        return pd.read_excel(filename, "size_correction", skiprows=1)

    def parseratios(self, data):
        # return just the size-corrected isotope ratios in a numpy array
        # for input to calcSPmain
        return np.array(
            data[
                ["size corrected 31R", "size corrected 45R", "size corrected 46R"]
            ].dropna()
        )

    def parseisotopomerinput(self, data):
        # return just the size-corrected isotope ratios in a numpy array
        # for input to calcSPmain
        return np.array(
            data[
                ["size corrected 31R", "size corrected 45R", "size corrected 46R",
                "gamma", "kappa"]
            ].dropna()
        )

    def __repr__(self):
        return f"{self.isotopomerinput}"


if __name__ == "__main__":
    print(Input(filename="00_excel_template.xlsx"))
