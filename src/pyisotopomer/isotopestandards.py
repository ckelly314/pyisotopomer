"""
File: isotopestandards.py
-------------------------------
Created on Thurs July 7th, 2021

Initialize and store isotope standards as adjustable parameters.

@author: Colette L. Kelly (clkelly@stanford.edu).
"""

class IsotopeStandards:
    """
    Return 15Ralpha and 15Rbeta for the two reference materials used to
    calibrate scrambling.

    USAGE: a, b, a2, b2 = constants('ATM', 'S2')

    INPUT:
        :param ref1:
        :type ref1:

    OUTPUT:
        :returns: 15Ralpha #1, 15Rbeta #1, 15Ralpha #2, 15Rbeta #2

    """

    def __init__(self,
        O17slope = None,
        O17excess = None,
        R15Air = None,
        R17VSMOW = None,
        R18VSMOW = None):

        if O17slope is None:
            self.O17slope = 0.516
        else:
            self.O17slope = O17slope
        
        if R15Air is None:
            self.R15Air = 0.0036765
        else:
            self.R15Air = R15Air
        
        if R17VSMOW is None:
            self.R17VSMOW = 0.0003799
        else: 
            self.R17VSMOW = R17VSMOW

        if R18VSMOW is None:
            self.R18VSMOW = 0.002052
        else:
            self.R18VSMOW = R18VSMOW

    def __repr__(self):
        return f"O17slope={self.O17slope}\nR15Air={self.R15Air}\nR17VSMOW={self.R17VSMOW}\nR18VSMOW={self.R18VSMOW}"
