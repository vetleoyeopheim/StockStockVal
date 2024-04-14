# -*- coding: utf-8 -*-
"""
Created on Thu Apr 11 21:31:10 2024

@author: Vetle
"""

import numpy as np
import pandas as pd

from matplotlib import pyplot as plt

class Stock:
    
    
    
    def __init__(self, revenue, opex, equity, cash, debt, 
                 curr_lia, curr_assets, depr, capex, int_cost):
        
        self.revenue = revenue
        self.opex = opex
        self.equity = equity
        self.cash = cash
        self.debt = debt
        self.curr_lia = curr_lia
        self.curr_assets = curr_assets
        self.depr = depr
        self.capex = capex
        self.int_cost = int_cost
        
        self.calc_working_capital()
        self.calc_net_capex()
        
    def calc_working_capital(self):
        
        self.working_capital = self.curr_assets - self.curr_lia
        
    def calc_net_capex(self):
        
        self.net_capex = self.capex - self.depr
        
        
class Simulation:
    
    
    def __init__(self, T, stock, rfr, disc_rate, perp_g, cap_g):
        
        self.T = T
        self.stock = stock
        self.cap_g = cap_g
        self.rfr = rfr
        self.disc_rate = disc_rate
        self.perp_g = perp_g
        
        self.simulate_ebit()
        self.calc_taxes()
        self.calc_net_int_cost()
        self.calc_net_capex()
        self.calc_fcf()
        self.calc_terminal_value()
        self.calc_npv()
        self.calc_value()
        
    def simulate_ebit(self, rev_distrib = ['normal', 0.08, 0.06], 
                      opxm_distrib = ['triangle', 0.1,0.15,0.19]):
        
        self.revenues = np.zeros(self.T)
        self.r_g = np.zeros(self.T)
        self.opex = np.zeros(self.T)
        self.opxm = np.zeros(self.T)
        
        #Set initial revenue as current revenue on the stock
        self.revenues[0] = self.stock.revenue
        self.opex[0] = self.stock.opex
        self.opxm[0] = (self.revenues[0] - self.opex[0]) / self.revenues[0]
        
        for t in range(1,self.T):
            
            #Check for distribution of revenue growth
            if rev_distrib[0] == 'normal':
                self.r_g[t] = np.random.normal(rev_distrib[1], rev_distrib[2])
            
            if opxm_distrib[0] == 'triangle':
                self.opxm[t] = np.random.triangular(opxm_distrib[1], opxm_distrib[2], opxm_distrib[3])
            
            self.revenues[t] = self.revenues[t - 1] * (1 + self.r_g[t])
            self.opex[t] = (1 - self.opxm[t]) * self.revenues[t]
            
        self.ebit = self.revenues - self.opex
        
    def calc_net_capex(self):
        
        self.net_capex = np.zeros(self.T)
        self.net_capex[0] = self.stock.net_capex
        
        
        for t in range(1, self.T):
            self.net_capex[t] = self.net_capex[t - 1] * (1 + self.cap_g)    
            
    def calc_taxes(self, tax_rate = 0.22):
        
        self.taxes = self.ebit * tax_rate
        
    def calc_fcf(self):
        
        self.fcf = np.zeros(self.T)
        
        for t in range(1, self.T):
            self.fcf[t] = self.ebit[t] - self.taxes[t] - self.net_capex[t] - self.int_cost[t]
            
    def calc_terminal_value(self):
        
        self.terminal_val = self.fcf[self.T - 1] * (1 + self.perp_g) / (self.disc_rate - self.perp_g)
        self.terminal_npv = self.terminal_val / (1 + self.disc_rate) ** (self.T + 1)
            
    def calc_npv(self):
        
        self.npv = np.zeros(self.T)
        
        for t in range(1, self.T):
            self.npv[t] = self.fcf[t] / (1 + self.disc_rate) ** (t)
            
    def calc_net_int_cost(self):
        
        self.int_cost = np.zeros(self.T)
        self.int_cost[0] = self.stock.int_cost
        
        for t in range(1,self.T):
            self.int_cost[t] = self.int_cost[t - 1] * (1 + self.cap_g)
            
    def calc_value(self):
        
        self.value = np.sum(self.npv) + self.terminal_npv + self.stock.cash - self.stock.debt
        self.value = max(self.value, 0)
        
    
