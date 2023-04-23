# -*- coding: utf-8 -*-
"""
Created on Sun Apr 23 10:23:54 2023

@author: Luiz
"""

# class TestIono:

#     def test_ion_ratio():
        
#         eff_mass = (2.66e-26 + 5.31e-26 + 4.99e-26) / 3
#         pro_mass = cs.proton_mass
#         assert (eff_mass / pro_mass) == 25.827713596325303



        
# (2.66e-26 + 5.31e-26 + 4.99e-26) / 3


from ionosphere import gyrofrequency,  conductivity

cond  = conductivity()

omega = gyrofrequency()

omega.ions()

