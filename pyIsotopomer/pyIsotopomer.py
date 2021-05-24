"""
File: pyIsotopomer.py
---------------------------
Created on Mon May 3rd, 2021

Scrambling and Isotopomers classes designed to
simplify IRMS scrambling and isotopomer calculations.

@author: Colette L. Kelly (clkelly@stanford.edu).
"""
import numpy as np
import pandas as pd
import datetime as dt
import automate_gk_solver as scramblingsolver
import calcSPmain
import calcdeltaSP


class Scrambling:
    """
    DESCRIPTION:
        Uses paired reference materials to calculate IRMS
        scrambling coefficients.
    
    EXAMPLE:
    gk = Scrambling(inputfile='test_cases/2012_atm_s2.csv', ref1='ATM', ref2='S2', saveout=False)

    INPUT:
        -   inputfile: .csv file with dimensions n x 6 where n is the number of
            measurements.  The three columns are 31R, 45R and 46R from
            left to right for the first reference material, then 31R,
            45R and 46R from left to right for the first reference material.
            inputfile.csv should have no headers or index.
        -   saveout: If True, save scrambling coefficients to output .csv file.
            Default = True.
        -   outputfile: Output filename. If None and saveout=True, default to
            "{date}_output.csv"
        -   initialguess: Initial guess for gamma and kappa. If None, default to
            [0.17, 0.08].
        -   lowerbounds: Lower bounds for the solver. If None, default to [0.0, 0.0]
        -   upperbounds: Upper bounds for the solver. If None, default to [1.0, 1.0]

    OUTPUT:
        -   Scrambling.R: Array of input data, read in from inputfile.
        -   Scrambling.scrambling: Pandas DataFrame object with dimensions
            n x 2, where n is the number of measurements. The two columns are
            gamma and kappa from left to right.
        -   Scrambling.scrambling_mean: Pandas DataFrame object with mean of
            gamma and kappa values.
        -   Scrambling.scrambling_std: Pandas DataFrame object with standard deviation of
            gamma and kappa values.
    """

    def __init__(self, inputfile, ref1, ref2, saveout=True, outputfile=None,
        initialguess=None, lowerbounds=None, upperbounds=None):

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

        if outputfile is None:
            today = dt.datetime.now().strftime('%y%m%d')
            outputfile = f'{today}_scramblingoutput.csv'
        else:
            outputfile = outputfile

        self.R = self.readin(inputfile)
        self.scrambling = self.computescrambling(self.R, initialguess,
            lowerbounds, upperbounds, ref1, ref2)
        self.scrambling_mean = self.scrambling.mean()
        self.scrambling_std = self.scrambling.std()

        self.inputfile = inputfile
        self.outputfile = outputfile
        self.initialguess = initialguess
        self.lowerbounds = lowerbounds
        self.upperbounds = upperbounds
        
        if saveout==True:
            self.saveoutput(self.scrambling, outputfile)
        else:
            pass

    def readin(self, inputfile):
        # import data and set inputs
        R = np.array(pd.read_csv(inputfile, header=None))
        return R

    def computescrambling(self, R, initialguess, lowerbounds, upperbounds, ref1, ref2):
        # Run function that iteratively solves for gamma and kappa
        scrambling = scramblingsolver.automate_gk_solver(R,x0=initialguess,
            lb=lowerbounds,ub=upperbounds,ref1=ref1, ref2=ref2)

        return scrambling

    def saveoutput(self, gk, outputfile):

        # Create a commma delimited text file containing the output data
        # The columns from left to right are gamma and kappa
        gk.to_csv(path_or_buf=f"{outputfile}", header=True, index=False)

    def __repr__(self):
        return f"<Gamma: {self.scrambling_mean[0]:.4}, Kappa: {self.scrambling_mean[1]:.4}>"

class Isotopomers:
    """
    DESCRIPTION:
        Uses values of 31R, 45R and 46R to calculate 15Ralpha, 15R beta, 17R
        and 18R.

    EXAMPLE:
    deltavals = Isotopomers(inputfile = 'py_atm.csv',
    scrambling=gk.scrambling.scrambling_mean, saveout=False)

    INPUT:
        -   inputfile: .csv file ith dimensions n x 3 where n is the number of
            measurements.  The three columns are 31R, 45R and 46R from left to
            right. 
            inputfile.csv should have no headers or index.
        -   Scrambling: Scrambling coefficients gamma and kappa for calculating
            isotopomer values. Scrambling coefficients can be calculated from
            paired reference materials using the Scrambling module.
        -   saveout: If True, save isotopocule values to output .csv file.
            Default = True.
        -   outputfile: Output filename. If None and saveout=True, default to
            "{date}_output.csv"

    OUTPUT:
        -   Isotopomers.R: Array of input data, read in from inputfile.
        -   Isotopomers.scrambling: Numpy array of scrambling coefficients.
        -   Isotopomers.isol: Pandas DataFrame object with  dimensions n x 4,
            where n is the number of measurements.  The four columns are
            15Ralpha, 15Rbeta, 17R and 18R from left to right.
        -   Isotopomers.deltavals: Pandas DataFrame object with dimensions n x 6,
            where n is the number of measurements.  The six columns are d15Nalpha,
            d15Nbeta, site preference, d15Nbulk, d17O and d18O from left to right.
        -   Scrambling.scrambling_std: Pandas DataFrame object with standard deviation of
            gamma and kappa values.
    """
    def __init__(self, inputfile, scrambling, saveout=True, outputfile=None):

        # default arguments
        if outputfile is None:
            today = dt.datetime.now().strftime('%y%m%d')
            outputfile = f'{today}_isotopeoutput.csv'
        else:
            outputfile = outputfile

        self.inputfile = inputfile
        self.scrambling = self.check_scrambling(scrambling)
        self.outputfile = outputfile
        self.R = self.readin(inputfile)
        self.isol = self.computeisotopomers(self.R, self.scrambling)
        self.deltavals = self.computedeltavals(self.isol)

        if saveout==True:
            self.saveoutput(self.deltavals, outputfile)
        else:
            pass

    def readin(self, inputfile):
        # import data and set inputs
        R = np.array(pd.read_csv(inputfile, header=None))
        return R
    
    def check_scrambling(self, scrambling):
        try:
            scrambling = np.array(scrambling, dtype=float)
        except ValueError:
            print("Please enter valid scrambling coefficients.")
        
        return scrambling

    def computeisotopomers(self, R, scrambling):
        # Run function that iteratively solves for 15Ralpha and 15Rbeta (a and b) 
        # and then calculates 17R and 18R (c and d) by substitution
        isol = calcSPmain.calcSPmain(R, scrambling=scrambling)

        return isol

    def computedeltavals(self, isol):
        # Run function that converts the data above to per mil notation referenced
        # to AIR (for N) and VSMOW (for O).
        deltaVals = calcdeltaSP.calcdeltaSP(isol)

        return deltaVals

    def saveoutput(self, deltavals, outputfile):
        # Create a commma delimited text file containing the output data
        # The columns from left to right are gamma and kappa
        deltavals.to_csv(path_or_buf=f"{outputfile}", header=True, index=False)

    def __repr__(self):
        
        return f'''< First row:
d15Na: {self.deltavals.d15Na[0]:.4}
d15Nb: {self.deltavals.d15Nb[0]:.4}
d15Nbulk: {self.deltavals.d15Nbulk[0]:.4}
SP: {self.deltavals.SP[0]:.4}
d18O: {self.deltavals.d18O[0]:.4}>
                '''
