"""
File: parseinput.py
---------------------------
Created on Weds June 2nd, 2021

Functions and Input class to read in and parse data
from excel template.

@author: Colette L. Kelly (clkelly@stanford.edu).
"""


import pandas as pd
import numpy as np
from itertools import combinations


class Input:
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
        :param *Refs: reference materials contained in the spreadsheet, e.g. "ATM", "S2", "B6"
        :type *Refs: string

    OUTPUT:
        :returns: dict with {key: [ref1, ref2, R, df]} for each reference material pairing.
        R is a Numpy array of size-corrected values to be input to automate_gk_solver.py.
        df is a Pandas DataFrame of dates, size-corrected values, and ref tags.

    @author: Colette L. Kelly (clkelly@stanford.edu).
    """

    def __init__(self, filename, **Refs):

        self.filename = filename

        # full contents of excel template, first tab
        self.data = self.readin(filename)

        # subset of data to be used for Isotopomers
        self.sizecorrected = self.parseratios(self.data)

        # subset of data to be used for Scrambling
        self.pairings, self.scrambleinput = self.parsescrambling(self.data, **Refs)

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

    def parsescrambling(self, data, **Refs):
        # return n arrays of paired reference materials,
        # where n = the number of possible combinations of reference materials
        pairings = list(combinations(Refs.values(), 2))

        # set up an output dictionary of ref pairings,
        # such that each key is the string representation of the pairing,
        # and the value is the Numpy array of paired size-corrected values
        outputdict = {}

        for c in pairings:
            # pull out data for left-hand side ref. material
            LHS = data[data.ref_tag == c[0]]
            # index on run date to utilize Pandas "join" operator
            LHS = (
                LHS[
                    [
                        "run_date",
                        "ref_tag",
                        "size corrected 31R",  # only need a subset of columns
                        "size corrected 45R",
                        "size corrected 46R",
                    ]
                ]
                .dropna()
                .set_index("run_date")
            )  # need to drop NaN's

            # pull out data for right-hand side ref. material
            RHS = data[data.ref_tag == c[1]]
            RHS = (
                RHS[
                    [
                        "run_date",
                        "ref_tag",
                        "size corrected 31R",
                        "size corrected 45R",
                        "size corrected 46R",
                    ]
                ]
                .dropna()
                .set_index("run_date")
            )

            # the Pandas "join" function merges the left-hand and right-hand DataFrames on date
            # it automatically generates the maximum number of pairings possibble for each date
            output = LHS.join(RHS, lsuffix="_1", rsuffix="_2").dropna()

            # check if output is empty
            if len(output) == 0:
                print(f"No matching dates for reference materials {c[0]} & {c[1]}")

            elif len(output) > 0:
                # dictionary key is the ref. pairing, e.g. "ATM-S2"
                key = f"{c[0]}-{c[1]}"

                # store names of ref materials in dict
                ref1 = c[0]
                ref2 = c[1]
                # store input array for automate_gk_solver, no index or header
                R = np.array(
                    output[
                        [
                            f"size corrected 31R_1",  # use f-strings to obtain column names
                            f"size corrected 45R_1",
                            f"size corrected 46R_1",
                            f"size corrected 31R_2",
                            f"size corrected 45R_2",
                            f"size corrected 46R_2",
                        ]
                    ]
                )

                # store pandas dataframe
                df = output

                outputdict[key] = [ref1, ref2, R, df]  # add data to output dictionary

        return pairings, outputdict

    def __repr__(self):
        return f"{self.pairings}"


if __name__ == "__main__":
    print(Input(filename="00_excel_template.xlsx"))
