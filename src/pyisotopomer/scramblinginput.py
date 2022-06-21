"""
File: scramblinginput.py
------------------------------
Created on Weds June 2nd, 2021

Functions and Input class to read in and parse data
from excel template.

@author: Colette L. Kelly (clkelly@stanford.edu).
"""


import pandas as pd
import numpy as np
from itertools import combinations
from .calculate_17R import calculate_17R


class ScramblingInput:
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

        try:
            # full contents of excel template, first tab
            self.data = self.readin(self.filename)
        except FileNotFoundError:
            if self.filename[-5:] != ".xlsx":
                self.filename = self.filename + ".xlsx"
                self.data = self.readin(self.filename)

        # subset of data to be used for Isotopomers
        self.sizecorrected = self.parseratios(self.data)

        # calculate 17R from 45R and 46R and add to self.data
        r17array = calculate_17R(self.sizecorrected)
        self.data["15Rbulk"] = r17array[:, 0]
        self.data["17R"] = r17array[:, 1]

        # subset of data to be used for Scrambling
        self.pairings, self.scrambleinput = self.parsescrambling(self.data, **Refs)

    def readin(self, filename):
        # return Pandas DataFrame of all input data
        data = pd.read_excel(filename, "size_correction", skiprows=1)
        data["ref_tag"] = data["ref_tag"].astype("string")
        data = data.dropna(thresh=10)  # need to drop rows of NaNs
        return data

    def parseratios(self, data):
        # return just the size-corrected isotope ratios in a numpy array
        # for input to calcSPmain
        return np.array(
            data[
                ["size corrected 31R", "size corrected 45R", "size corrected 46R"]
            ].dropna()
        )

    def parsescrambling(self, data, **Refs):
        # if no ref materials are specified, infer from ref_tag column
        if len(Refs.values()) == 0:
            Refs = list(data.ref_tag.dropna().drop_duplicates())
        else:
            Refs = Refs.values()
        # convert all reference names to strings in case they are input as numbers
        Refs = [str(r) for r in Refs]
        # return n arrays of paired reference materials,
        # where n = the number of possible combinations of reference materials
        pairings = list(combinations(Refs, 2))

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
                        "15Rbulk",
                        "17R",
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
                        "15Rbulk",
                        "17R",
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
                            "size corrected 31R_1",
                            "size corrected 45R_1",
                            "size corrected 46R_1",
                            "15Rbulk_1",
                            "17R_1",
                            "size corrected 31R_2",
                            "size corrected 45R_2",
                            "size corrected 46R_2",
                            "15Rbulk_2",
                            "17R_2",
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
