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


def calcdeltaSP(isol):
    """
    USAGE: deltaVals = calcdeltaSP(isol)

    DESCRIPTION:
        Uses values of 15Ralpha, 15Rbeta, 17R and 18R to calculate delta
        values in per mil notation referenced to AIR (for N) and VSMOW (for O).

    INPUT:
        isol = array with dimensions n x 4 where n is the number of
        measurements.  The three columns are 15Ralpha, 15Rbeta, 17R and 18R
        from left to right.

    OUTPUT:
        deltaVals = array with dimensions n x 6 where n is the number of
       measurements.  The six columns are d15Nalpha, d15Nbeta, 15N site pref,
       d15Nbulk, d17O and d18O from left to right.
    """

    # Calculate delta values of 15Nalpha and 15Nbeta referenced to the
    # Casciotti lab standard
    d15NalphaStd = 1000 * (isol[0]/0.003677014710 - 1)
    d15NbetaStd = 1000 * (isol[1]/0.003676389705 - 1)

    # Convert delta values of 15N so that they are referenced to AIR instead of 
    # the Casciotti lab standard; **is this necessary or advisable?**
    d15NalphaAir = d15NalphaStd + 0.14 + d15NalphaStd * (0.14/1000)
    d15NbetaAir = d15NbetaStd - 0.03 + d15NbetaStd * (-0.03/1000)

    # Calculate 15N site preference referenced to AIR
    SP = d15NalphaAir - d15NbetaAir;

    # Calculate bulk 15N value from site preference values
    d15Nbulk = (d15NalphaAir + d15NbetaAir)/2

    # Calculate d17O and d18O referenced to VSMOW
    d17O = 1000*(isol[2]/0.0003799 - 1)
    d18O = 1000*(isol[3]/0.0020052 - 1)

    # Create array of isotope data and return
    deltaVals = np.array([d15NalphaAir, d15NbetaAir, SP, d15Nbulk,  d17O, d18O]).T
    deltaVals = pd.DataFrame(deltaVals, columns = ['d15Na', 'd15Nb', 'SP', 'd15Nbulk', 'd17O', 'd18O'])

    return deltaVals
