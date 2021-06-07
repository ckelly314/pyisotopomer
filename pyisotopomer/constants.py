"""
File: constants.py
---------------------------
Created on Weds April 14th, 2021

Define alpha and beta values for the reference materials used for
the scrambling calibration.

@author: Colette L. Kelly (clkelly@stanford.edu).
"""

from collections import defaultdict
from collections import namedtuple

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
    
    # set up a dictionary of reference materials that returns [1,1]
    # if user tries to enter a key that has not yet been entered in constants.py
    def constant_factory(value):
        return lambda: value

    c = defaultdict(constant_factory([1,1]))
    
    # each reference material is defined as a named tuple for readability
    Ref_material = namedtuple('Ref_material',['R15alpha', 'R15beta'])

    ###############
    # USER INPUTS #
    ###############

    # Ensure this list contains both ref. materials used for the calibration
    # If it does not, add data in this format:
    # c['REFNAME'] = Ref_material(R15alpha = 0.003..., R15beta = 0.003...)
    c['ATM'] = Ref_material(R15alpha = 0.003734221050, R15beta = 0.003664367550) # atmosphere-equilibrated seawater
    c['S2'] = Ref_material(R15alpha = 0.003696905, R15beta = 0.003629183) # Toyoda Lab S2
    c['B6'] = Ref_material(R15alpha = 0.00367501482137193, R15beta = 0.00367595533009498) # Air Liquide B6
    c['S1'] = Ref_material(R15alpha = 0.00373422105, R15beta = 0.003664698435) # Toyoda Lab S1

    #####################################################
    # ACCESS VALUES - NO NEED TO MODIFY BELOW THIS LINE #
    #####################################################
    a, b = c[ref1]
    a2, b2 = c[ref2]

    if a==1 or b==1 or a2==1 or b2==1:
        print("<Error: reference material has not been added to constants.py>")

    return a, b, a2, b2
