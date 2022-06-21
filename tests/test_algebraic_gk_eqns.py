import pandas as pd
import numpy as np
import pyisotopomer as iso

R = pd.read_csv("test_algebraic_gk_input.csv", header=None)

gk = iso.algebraic_gk_eqns(R, "ATM", "S2")

gk.to_csv("test_algebraic_gk_output.csv")

print(gk)