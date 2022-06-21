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

    def __init__(self, filename, tabname=None):

        self.filename = filename

        if tabname is not None:
            self.tabname = tabname
        elif tabname is None:
            self.tabname = "size_correction"

        try:
            # full contents of excel template, first tab
            self.data = self.readin(self.filename, self.tabname)
        except FileNotFoundError:
            if self.filename[-5:] != ".xlsx":
                self.filename = self.filename + ".xlsx"
                self.data = self.readin(self.filename, self.tabname)

        # subset of data to be used for Isotopomers
        self.sizecorrected = self.parseratios(self.data)

        self.ratiosscrambling = self.parseisotopomerinput(self.data)

    def readin(self, filename, tabname):
        # return Pandas DataFrame of all input data
        return pd.read_excel(filename, tabname, skiprows=1)

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
                [
                    "size corrected 31R",
                    "size corrected 45R",
                    "size corrected 46R",
                    "gamma",
                    "kappa",
                ]
            ].dropna()
        )

    def __repr__(self):
        return f"{self.sizecorrected}"


if __name__ == "__main__":
    print(Input(filename="00_excel_template.xlsx"))
