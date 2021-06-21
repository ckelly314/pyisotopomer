"""
File: vary_ref_scrambling.py
---------------------------
Created on Weds April 14th, 2021

Test the effect of assumed scrambling for direct reference injection
on calculated scrambling coefficients.

@author: Colette L. Kelly (clkelly@stanford.edu).
"""

# import utils
import sys
sys.path.append("/Users/colette/Box Sync/N2O Research/Spec calibration files/N2O_isotopocule_data_corrections/pyisotopomer/pyisotopomer")

from pyisotopomer import Scrambling, Isotopomers
import pandas as pd
import matplotlib.pyplot as plt

### DATA ANALYSIS ###
# read in input spreadsheet and calculate scrambling
gk = Scrambling(inputfile="00_vary_ref_scrambling.xlsx",
    outputfile="00_vary_ref_scrambling_output.xlsx",
    ref1='ATM', ref2='S2', ref3='B6')

inputdata = pd.read_excel("00_vary_ref_scrambling.xlsx",
    "size_correction", skiprows=1)

ref_scrambling = inputdata[inputdata.ref_tag=="ATM"][['series','gamma_ref','kappa_ref']]

sample_scrambling = gk.outputs[2][['gamma','kappa']]


### PLOTTING ###
fig, axes = plt.subplots(1,2, figsize=(7,3))

ax = axes[0]

x = ref_scrambling.gamma_ref
y = sample_scrambling.gamma

ax.scatter(x, y, c=ref_scrambling.series, edgecolor='k', cmap="binary")
ax.plot(x,y, color='k', zorder=0)
ax.set_xlabel("Ref. injection $\gamma$")
ax.set_ylabel("Calculated sample $\gamma$")

ax = axes[1]

x = ref_scrambling.kappa_ref
y = sample_scrambling.kappa

ax.scatter(x, y, c=ref_scrambling.series, edgecolor='k', cmap="binary")
ax.plot(x,y, color='k', zorder=0)

ax.set_xlabel("Ref. injection $\kappa$")
ax.set_ylabel("Calculated sample $\kappa$")

fig.suptitle(gk.pairings[2])

plt.tight_layout()
plt.savefig("Figures/vary_ref_scrambling.pdf")
plt.show()
