"""
File: concentrations.py
---------------------------
Created on Mon May 3rd, 2021

Functions to convert mass 44 peak area to N2O concentration,
and use 45/44 and 46/44 ratios to calculate concentrations of heavy
isotopocules.

@author: Colette L. Kelly (clkelly@stanford.edu).
"""


from collections import namedtuple
import pandas as pd


def concentration44(peakarea44, sampleweight, conversionslope, conversionint=None):

    ### DEFINE CONSTANTS ###
    if conversionint is None:
        conversionint = 0
    m, b = conversionslope, conversionint  # nmol per Vs of 44 peak area
    ref_density = 1.026  # seawater kg/L
    liter_kg = 1 / ref_density  # seawater L/kg = 1/density
    liter_g = liter_kg / 1000.0  # seawater L/g = L/kg/1000

    ### CALCULATE CONCENTRATION ###
    sample_vol = sampleweight * liter_g  # sample volume (L) = weight (g)*(L/g)
    nmol_N2O = peakarea44 * m + b  # nmol N2O
    concentration_N2O = nmol_N2O / sample_vol  # nmol/L

    return nmol_N2O, concentration_N2O


def concentrations(
    peakarea44, sampleweight, conversionslope, isotoperatios, conversionint=None
):

    ### OBTAIN CONCENTRATIONS OF MASSES 44m 45alpha, 45beta, and 46N2O
    n, c = concentration44(peakarea44, sampleweight, conversionslope, conversionint)

    allconcentrations = isotoperatios * c
    allconcentrations["44N2O"] = c

    return allconcentrations


if __name__ == "__main__":
    print(
        concentrations(
            peakarea44=10,
            sampleweight=153,
            conversionslope=0.48,
            isotoperatios=pd.DataFrame([[1, 2, 3, 4]]),
        )
    )
