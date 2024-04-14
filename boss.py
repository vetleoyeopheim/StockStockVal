# -*- coding: utf-8 -*-
"""
Created on Sun Apr 14 21:55:09 2024

@author: Vetle
"""

import numpy as np
import simulation
from matplotlib import pyplot as plt


stock = simulation.Stock(4089,3695,1310,168,1300,1193,1591, 250, 300, 50)
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
