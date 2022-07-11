"""
File: calcdeltaSP.py
---------------------------
Created on Weds April 14th, 2021

Functions to solve for N2O isotopocule delta values, given
a set of IRMS scrambling coefficients (see pyScramble.py for
scripts to obtain scrambling coefficients).

@author: Cara Manning (cama@pml.ac.uk),
python version by Colette L. Kelly (clkelly@stanford.edu).
"""

import numpy as np
import pandas as pd


def calcdeltaSP(isol, isotopestandards):
    """
    USAGE: deltaVals = calcdeltaSP(isol)

    DESCRIPTION:
        Uses values of 15Ralpha, 15Rbeta, 17R and 18R to calculate delta
        values in per mil notation referenced to AIR (for N) and VSMOW (for O).

    INPUT:
        :param isol: pandas DataFrame with dimensions n x 45where n is the number of measurements.
        The five columns are 15Ralpha, 15Rbeta, 17R, 18R, and D17O.
        :type isol: Pandas DataFrame
        :param IsotopeStandards: IsotopeStandards class from isotopestandards.py,
        containing 15RAir, 18RVSMOW, 17RVSMOW, and beta for the 18O/17O relation.
        :type isotopestandards: Class

    OUTPUT:
       deltaVals = array with dimensions n x 6 where n is the number of
       measurements.  The six columns are d15Nalpha, d15Nbeta, 15N site pref,
       d15Nbulk, d17O and d18O from left to right.
    """

    R15Air = isotopestandards.R15Air
    R17VSMOW = isotopestandards.R17VSMOW
    R18VSMOW = isotopestandards.R18VSMOW

    # Calculate delta values of 15Nalpha and 15Nbeta referenced to AIR
    d15NalphaAir = 1000 * (isol["15Ralpha"] / R15Air - 1)
    d15NbetaAir = 1000 * (isol["15Rbeta"] / R15Air - 1)

    # Calculate 15N site preference referenced to AIR
    SP = d15NalphaAir - d15NbetaAir

    # Calculate bulk 15N value from site preference values
    d15Nbulk = (d15NalphaAir + d15NbetaAir) / 2

    # Calculate d17O and d18O referenced to VSMOW
    d17O = 1000 * (isol["17R"] / R17VSMOW - 1)
    d18O = 1000 * (isol["18R"] / R18VSMOW - 1)

    # Create array of isotope data and return
    deltaVals = np.array([d15NalphaAir, d15NbetaAir, SP, d15Nbulk, d17O, d18O]).T
    deltaVals = pd.DataFrame(
        deltaVals, columns=["d15Na", "d15Nb", "SP", "d15Nbulk", "d17O", "d18O"]
    )

    return deltaVals
