"""
File: isotopestandards.py
-------------------------------
Created on Thurs July 7th, 2021

Initialize and store isotope standards as adjustable parameters.

@author: Colette L. Kelly (clkelly@stanford.edu).
"""


class IsotopeStandards:
    """
    Initialize and store isotope standards as adjustable parameters.

    USAGE: IsotopeStandards = IsotopeStandards(O17beta = O17beta,
                    R15Air = R15Air,
                    R17VSMOW = R17VSMOW,
                    R18VSMOW = R18VSMOW)

    INPUT:
        :param O17beta: adjustable beta parameter for 17O/18O mass-dependent relation.
        :type O17beta: float
        :param R15Air: adjustable 15/14R of Air.
        :type R15Air: float
        :param R17VSMOW: adjustable 17/16R of VSMOW.
        :type R17VSMOW: float
        :param R18VSMOW: adjustable 18/16R of VSMOW.
        :type R18VSMOW: float

    OUTPUT:
        :param IsotopeStandards: IsotopeStandards class from isotopestandards.py,
        containing 15RAir, 18RVSMOW, 17RVSMOW, and beta for the 18O/17O relation.
        :type isotopestandards: Class

    """

    def __init__(self, O17beta=None, R15Air=None, R17VSMOW=None, R18VSMOW=None):

        if O17beta is None:
            self.O17beta = 0.516
        else:
            self.O17beta = O17beta

        if R15Air is None:
            self.R15Air = 0.0036765  # [De Bièvre et al., 1996]
        else:
            self.R15Air = R15Air

        if R17VSMOW is None:
            self.R17VSMOW = 0.0003799  #  [Li et al., 1988]
        else:
            self.R17VSMOW = R17VSMOW

        if R18VSMOW is None:
            self.R18VSMOW = 0.0020052  # [Baertschi, 1976]
        else:
            self.R18VSMOW = R18VSMOW

    def __repr__(self):
        return f"O17beta={self.O17beta}\nR15Air={self.R15Air}\nR17VSMOW={self.R17VSMOW}\nR18VSMOW={self.R18VSMOW}"
