"""
File: pyisotopomer.py
---------------------------
Created on Mon May 3rd, 2021

Scrambling and Isotopomers classes designed to
simplify IRMS scrambling and isotopomer calculations.

@author: Colette L. Kelly (clkelly@stanford.edu).
"""
import numpy as np
import pandas as pd
import datetime as dt
from .calcSPmain import calcSPmain
from .calcdeltaSP import calcdeltaSP
from .concentrations import concentrations
from .parseinput import Input
from .parseoutput import parseoutput


class Scrambling:
    """
    Read in input spreadsheet of reference materials & calculate scrambling coefficients.

    USAGE: gk = Scrambling(inputfile="00_Python_template.xlsx", ref1='ATM', ref2='S2', ref3='B6')

    DESCRIPTION:
        Takes an input spreadsheet of size-corrected reference materials,
        following the format of the template "00_Python_template.xlsx".
        Generates all possible pairings of reference materials.
        Uses paired reference materials to calculate IRMS
        scrambling coefficients.

    INPUT:
        :param inputfile: Spreadsheet of size-corrected reference materials,
        following the format of "00_Python_template.xlsx".
        :type inputfile: .xlsx file
        :param **Refs: Reference materials included in input spreadsheet:
        e.g., ref1="NAME", ref2="NAME", ref3="NAME"
        :type **Refs: Variadic kwargs
        :param saveout: If True, save output .xlsx file of scrambling results.
        :type saveout: Bool
        :param outputfile: Output filename. If None and saveout=True, default to
            "{date}_scrambling_output.xlsx"
        :type outputfile: String
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
        :param inputobj: Input class from parseinput.py
        :type inputobj: Class
        :param outputs: Tables of scrambling coefficients for each pairing of ref. materials.
        :type outputs: List of Pandas DataFrames
        :param pairings: List of ref. material pairings generated from parseinputs
        :type pairings: List of tuples
        :param alloutputs: One table of all scrambling coefficients for all pairings.
        :type alloutputs: Pandas DataFrame
        :param scrambling: All scrambling coefficients calculated for all pairings.
        :type scrambling: Pandas Series
        :param scrambling_mean: Pandas DataFrame object with mean of gamma and kappa values.
        :type scrambling_mean: Pandas Series
        :param scrambling_std: Pandas DataFrame object with standard dev. of gamma and kappa values.
        :type scrambling_std: Pandas Series

    @author: Colette L. Kelly (clkelly@stanford.edu).
    """

    def __init__(
        self,
        inputfile,
        saveout=True,
        outputfile=None,
        initialguess=None,
        lowerbounds=None,
        upperbounds=None,
        **Refs,
    ):

        # default arguments
        if outputfile is None:
            today = dt.datetime.now().strftime("%y%m%d")
            outputfile = f"{today}_scrambling_output.xlsx"
        else:
            outputfile = outputfile

        self.outputfile = outputfile

        self.inputobj = Input(inputfile, **Refs)
        self.outputs, self.pairings, self.alloutputs = parseoutput(
            self.inputobj,
            initialguess=initialguess,
            lowerbounds=lowerbounds,
            upperbounds=upperbounds,
        )

        self.scrambling = self.alloutputs[["gamma", "kappa"]]
        self.scrambling_mean = self.scrambling.mean()
        self.scrambling_std = self.scrambling.std()

        if saveout == True:
            self.saveoutput(self.outputfile)
        else:
            pass

    def saveoutput(self, outputfilename):

        # Create an excel file containing the output data
        with pd.ExcelWriter(outputfilename) as writer:
            self.alloutputs.to_excel(
                writer, sheet_name="all"
            )  # save out main dataframe to one sheet
            for df, name in zip(self.outputs, self.pairings):
                # write each output dataframe to a separate sheet in the output spreadsheet
                df.to_excel(writer, sheet_name=name)

    def __repr__(self):
        return f"<Gamma: {self.scrambling_mean[0]:.4}, Kappa: {self.scrambling_mean[1]:.4}>"


class Isotopomers:
    """
    Read in the isotopomers template spreadsheet and calculate isotopomers.

    USAGE: deltavals = Isotopomers(inputfile = "00_Python_template.xlsx", scrambling=[0.17, 0.08])

    DESCRIPTION:
        Uses values of 31R, 45R and 46R to calculate 15Ralpha, 15R beta, 17R
        and 18R.

    INPUT:
        :param inputfile: Spreadsheet of size-corrected reference materials,
        following the format of "00_Python_template.xlsx".
        :type inputfile: .xlsx file
        :param scrambling: Scrambling coefficients to use to correct this sample set.
        :type scrambling: List or Numpy array.
        :param saveout: If True, save output .xlsx file of scrambling results.
        :type saveout: Bool
        :param outputfile: Output filename. If None and saveout=True, default to
            "{date}__isotopeoutput.csv"
        :type outputfile: String

    OUTPUT:
        :param scrambling: Scrambling coefficients to use to correct this sample set.
        :type scrambling: Numpy array.
        :param R: Size-corrected 31R, 45R, and 46R from which to calculate delta vals.
        :type R: Numpy array.
        :param isotoperatios: Pandas DataFrame object with  dimensions n x 4,
            where n is the number of measurements.  The four columns are
            15Ralpha, 15Rbeta, 17R and 18R from left to right.
        :type isotoperatios: Pandas DataFrame
        :param deltavals: Pandas DataFrame object with dimensions n x 6,
            where n is the number of measurements.  The six columns are d15Nalpha,
            d15Nbeta, site preference, d15Nbulk, d17O and d18O from left to right.
        :type deltavals: Pandas DataFrame

    @author: Colette L. Kelly (clkelly@stanford.edu).
    """

    def __init__(self, inputfile, scrambling, saveout=True, outputfile=None):

        # default arguments
        if outputfile is None:
            today = dt.datetime.now().strftime("%y%m%d")
            outputfile = f"{today}_isotopeoutput.csv"
        else:
            outputfile = outputfile

        self.scrambling = self.check_scrambling(scrambling)
        self.R = Input(inputfile).sizecorrected
        self.isotoperatios = calcSPmain(self.R, scrambling=self.scrambling)
        self.deltavals = calcdeltaSP(self.isotoperatios)

        if saveout == True:
            self.saveoutput(self.deltavals, outputfile)
        else:
            pass

    def check_scrambling(self, scrambling):
        try:
            scrambling = np.array(scrambling, dtype=float)
        except ValueError:
            print("Please enter valid scrambling coefficients.")

        return scrambling

    def saveoutput(self, deltavals, outputfile):
        # Create a commma delimited text file containing the output data
        # The columns from left to right are gamma and kappa
        deltavals.to_csv(path_or_buf=f"{outputfile}", header=True, index=False)

    def get_concentrations(
        self, peakarea44, sampleweight, conversionslope, conversionint=None
    ):
        # obtain concentrations of masses 44, 45alpha, 45beta, and 46N2O
        allconcentrations = concentrations(
            peakarea44,
            sampleweight,
            conversionslope,
            conversionint,
            isotoperatios=self.isol,
        )

        keys = {
            "15Ralpha": "45N2Oalpha",
            "15Rbeta": "45N2Obeta",
            "17R": "N217O",
            "18R": "46N2O",
        }
        allconcentrations = allconcentrations.rename(columns=keys)

        return allconcentrations

    def __repr__(self):

        return f"""< First row:
d15Na: {self.deltavals.d15Na[0]:.4}
d15Nb: {self.deltavals.d15Nb[0]:.4}
d15Nbulk: {self.deltavals.d15Nbulk[0]:.4}
SP: {self.deltavals.SP[0]:.4}
d18O: {self.deltavals.d18O[0]:.4}>
                """
