#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 10 13:33:10 2016

@author: derek
"""

import numpy as np
import cantera as ct
import pandas as pd

from flowprojectfunc import Fuel_Oxidizer_Cals
from flowprojectfunc import Calc_Props
from flowprojectfunc import Mix_rho
from flowprojectfunc import m_dot
from flowprojectfunc import A_orf
from flowprojectfunc import APu_prod
from flowprojectfunc import conv_in_m
from flowprojectfunc import find_closest

fuel = 'C3H8'
ox = 'N2O'
phi = 1.0
F_O = Fuel_Oxidizer_Cals(phi, fuel, ox)
T = 298
P = 101325
P_guess = 750000
L = 2
D_tube = 0.0762
Op_freq = 1
P_poss = np.linspace(350000, 1.380E6, num=200)
Orifices = np.array(conv_in_m([0.040, 0.047, 0.063, 0.142]))
Areas = A_orf(Orifices)

# Create an array of lists for the possible combinations of the pressures and
# orifice diameters
APu_poss = pd.DataFrame(np.einsum('i,j-> ji', Areas, P_poss),
                        index=P_poss, columns=Orifices)

[rho_fuel, k_fuel, MW_fuel] = Calc_Props(fuel, T, P)
[rho_ox, k_ox, MW_ox] = Calc_Props(ox, T, P)

rho_mix = Mix_rho(fuel, ox, F_O, T, ct.one_atm)
m_dot_tube = A_orf(D_tube)*L*rho_mix*Op_freq
print(str(m_dot_tube) + ' (kg/s)')

m_dot_ox = m_dot_tube / (1 + F_O)
m_dot_fuel = F_O * m_dot_ox

APu_fuel = APu_prod(m_dot_fuel, T, fuel, P_guess)


index = APu_poss.sub(APu_fuel).abs().min().idxmin()
value = APu_poss.sub(APu_fuel).abs().min(axis=1).idxmin()
APu_poss[index][value]
print(index, value)
