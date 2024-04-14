# -*- coding: utf-8 -*-
"""
Created on Sun Apr 14 21:56:41 2024

@author: Vetle
"""

import numpy as np
import simulation
from matplotlib import pyplot as plt


stock = simulation.Stock(36000,30494,-7994,3900,24672,9345,7303, 1300, 2300, 470)
sim = simulation.Simulation(11,stock,0.04,0.09,0.04, 0.04)
            
#plt.plot(sim.opex)
#plt.plot(sim.revenues)
#plt.plot(sim.fcf)

N = 20000

values = np.zeros(N)

for n in range(N):
    
    sim = simulation.Simulation(11,stock,0.04,0.09,0.04, 0.04)
    values[n] = sim.value
    
    
plt.hist(values, bins = 100)