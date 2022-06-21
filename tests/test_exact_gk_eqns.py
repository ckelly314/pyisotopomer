import pandas as pd
import numpy as np
import pyisotopomer as iso

R = pd.read_csv("test_exact_gk_input.csv", header=None)

gk = iso.exact_gk_eqns(R, "ATM", "S2")

gk.to_csv("test_exact_gk_output.csv")

print(gk)