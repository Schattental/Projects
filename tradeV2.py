# -*- coding: utf-8 -*-
"""
Created on Mon Sep  5 01:07:27 2022

@author: Schattental

Python code to make crypto currency buy / sell decisions.
"""

import numpy as np
import matplotlib.pyplot as plt

erp = 10*20 # 10
fema = 2*20 # 2
sema = 30*19 # 30

fSC = 2/(fema+1)
sSC = 2/(sema+1)

long_K = np.array([])

fperc = 0.2 # failsafe percentage is how much KAMA can differ from current price

def kama(erp, fema, sema, data):
    fSC = 2/(fema+1)
    sSC = 2/(sema+1)
    
    #p = data
    p1 = data[(sema*2-erp*2):sema*2]
    change = abs(p1[-1] - p1[0])
    p1_start = p1[::2]
    p1_end = p1[1::2]
    
   # short_p1 = p1 #p3[(sema*2-erp):sema*2]
    
    summ = np.sum(np.abs(p1_end - p1_start))
    
    if(summ == 0):
        summ = 0.1
    ER = change/summ

    SC = (ER * (fSC - sSC) + sSC)**2
    #short_SC = (short_ER * (2/((fema/2)+1) - sSC) + sSC)**2
    return SC

def read(file):
    return np.loadtxt(file, skiprows = 0)

def cyc():
    p3 = # sema*2 länge an Zeitpunkten abfragen
    SC = kama(erp, fema, sema, p3)
    SC2 = kama(int(erp/2), int(fema/2), int(sema/2), p3)
    SC3 = kama(int(erp/2), int(fema/1.5), int(sema/2), p3)
    
    hist = read("log.txt")
    
    if (hist == ""):
        prior_KAMA = np.average(p3)
        prior_KAMA2 = np.average(p3)
        prior_KAMA3 = np.average(p3)
        
        #TODO Hier log.txt prior_KAMAs eintragen, elif machen, um Zeitpunkt zu kontrollieren, falls crash (Zeitlücke) -> reset mit avg
    
    #TODO Je nachdem wie log.txt formatiert ist muss es hier eingefügt werden um korrekt gelesen zu werden
    prior_KAMA = hist[:]
    prior_KAMA2 = hist[:]
    prior_KAMA3 = hist[:]
        
    KAMA = prior_KAMA + SC*(p3[-1] - prior_KAMA)
    KAMA2 = prior_KAMA2 + SC2*(p3[-1] - prior_KAMA2)
    KAMA3 = prior_KAMA3 + SC3*(p3[-1] - prior_KAMA3)
     
    # failsafe for big fluctuations / anomalies
    if(abs(abs(KAMA) - p3[-1]) > p3[-1]*fperc):
         KAMA = np.average(p3)
    if(abs(abs(KAMA2) - p3[-1]) > p3[-1]*fperc):
         KAMA2 = np.average(p3[sema:])
    if(abs(abs(KAMA3) - p3[-1]) > p3[-1]*fperc):
         KAMA3 = np.average(p3[sema:])
         
    # 1 is buy, -1 is sell, 0 is do nothing
    if((p3[-2] < prior_KAMA) and (p3[-1] >= KAMA)):
        res = 1 #buysell.append(1) # buy
        
    elif((p3[-2] > prior_KAMA) and (p3[-1] <= KAMA)):
        res = -1 #buysell.append(-1) # sell
    else:
        res = 0 #buysell.append(0) # nothing
        
    prior_KAMA = KAMA
    prior_KAMA2 = KAMA2
    prior_KAMA3 = KAMA3
    
    #TODO Hier log.txt prior_KAMAs eintragen
    
    return res
        
        
        
        
     