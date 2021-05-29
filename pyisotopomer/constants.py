"""
File: constants.py
---------------------------
Created on Weds April 14th, 2021

Define alpha and beta values for the reference materials used for
the scrambling calibration.

@author: Colette L. Kelly (clkelly@stanford.edu).
"""

def constants(ref1, ref2):
    '''
    Return 15Ralpha and 15Rbeta for the two reference materials used to
    calibrate scrambling.

    USAGE: a, b, a2, b2 = constants('ATM', 'S2')

    INPUT:
        :param ref1: name of first reference material used for scrambling calibration
        :type ref1: string
        :param ref2: name of second reference material used for scrambling calibration
        :type ref2: string

    OUTPUT:
        :returns: 15Ralpha #1, 15Rbeta #1, 15Ralpha #2, 15Rbeta #2

    '''

    ###############
    # USER INPUTS #
    ###############

    # Ensure this dictionary contains both ref. materials used for the calibration
    # If it does not, add data in this format:
    # 'REFNAME': [15Ralpha, 15Rbeta]
    c = { 
    'ATM':[0.003734221050, 0.003664367550], # atmosphere-equilibrated seawater
    'S2':[0.003696905, 0.003629183], # Toyoda Lab S2
    'B6':[0.00367501482137193, 0.00367595533009498], # Air Liquide B6
    'S1':[0.00373422105, 0.003664698435] # Toyoda Lab S1
    }

    #####################################################
    # ACCESS VALUES - NO NEED TO MODIFY BELOW THIS LINE #
    #####################################################
    a, b = c[ref1]
    a2, b2 = c[ref2]

    return a, b, a2, b2
