# -*- coding: utf-8 -*-
"""
Created on Thu Jun  2 11:55:35 2022

@author: Schattental

Python code to make crypto currency buy / sell decisions.
"""

import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['figure.dpi'] = 300

# reading in data
# in this case csv files for testing
def read(file):
    return np.loadtxt(file, skiprows = 0)

data = read("cut_Binance_BTCUSDT_minute.csv")
#data2  = read("cut_Binance_BTCUSDT_minute.csv")
xs = np.arange(0, len(data))


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
    
    p = data
    p1 = p[(sema*2-erp*2):sema*2]
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


def cycle():
    first = True
    kamal = []
    kamal2 = []
    kamal3 = []
    buysell = []
    for n in range(0, (len(data)-sema*2)):
        p3 = data[n:(n+sema*2)]
        SC = kama(erp, fema, sema, p3)
        SC2 = kama(int(erp/4), int(fema/4), int(sema/4), p3)
        SC3 = kama(int(erp/2), int(fema/2), int(sema/2), p3)
         
        if first:
            prior_KAMA = np.average(p3)
            prior_KAMA2 = np.average(p3)
            prior_KAMA3 = np.average(p3)
            first = False
        
        KAMA = prior_KAMA + SC*(p3[-1] - prior_KAMA)
        KAMA2 = prior_KAMA2 + SC2*(p3[-1] - prior_KAMA2)
        KAMA3 = prior_KAMA3 + SC3*(p3[-1] - prior_KAMA3)
        
        # failsafe for big fluctuations / anomalies
        if(abs(abs(KAMA) - p3[-1]) > p3[-1]*fperc):
            KAMA = np.average(p3)
#        if(abs(abs(KAMA2) - p3[-1]) > p3[-1]*fperc):
#            KAMA2 = np.average(p3[sema:])
#        if(abs(abs(KAMA3) - p3[-1]) > p3[-1]*fperc):
#            KAMA3 = np.average(p3[sema:])
        
        kamal.append(KAMA)
        kamal2.append(KAMA2)
        kamal3.append(KAMA3)
        
        # 1 is buy, -1 is sell, 0 is do nothing
        if((p3[-2] < prior_KAMA) and (p3[-1] >= KAMA)):
            #if(prior_KAMA2 - KAMA2 < 0) and ((prior_KAMA2 - KAMA2) < prior_KAMA3 - KAMA3):
            buysell.append(1) # buy
            
        elif((p3[-2] > prior_KAMA) and (p3[-1] <= KAMA)):
           # if(prior_KAMA2 - KAMA2 > 0) and (prior_KAMA2 - KAMA2 > prior_KAMA3 - KAMA3):
            buysell.append(-1) # sell
        else:
            buysell.append(0) # nothing
        
        # Idee : buy/sell linie zu einer der Vergleichslinien machen und kürzeste Perioden als buy/sell
        # Dann mit den zwei längeren drosseln um schlechte Entscheidungen abzufangen
        
        prior_KAMA = KAMA
        prior_KAMA2 = KAMA2
        prior_KAMA3 = KAMA3
            
            
    return {'K': np.array(kamal), 
            'K2': np.array(kamal2),
            'K3': np.array(kamal3),
            'bs': np.array(buysell)}

cyc = cycle()

#plt.plot(xs, data, color="purple")
plt.plot(xs[sema*2:], cyc['K']/data[0], color ="blue", label="buysell")

#plt.ylim(45000, 55000)
#plt.ylim(35000, 40000)
#plt.xlim(0, 1000)
#plt.xlim(525540, 525600)
#plt.xlim(157600, 157969)


def sim(kline, buy, sell, fee=0.001):    
    
    sell[-1] = True
    
    holding = False
    wealth = np.ones(kline.size + 1)
    wealth[0] = 1
    for i, (b, s) in enumerate(zip(buy, sell)):
        if holding:
            wealth[i+1] = wealth[i] * (kline[i] / kline[i-1])
        else:
            wealth[i+1] = wealth[i] #wealth[i+1] = wealth[i] * (kline[i-1] / kline[i])
        
        buy[i] = sell[i] = False
        if b and not holding:
            buy[i] = True
            holding = True
            wealth[i+1] *= (1-fee)
        if s and holding:
            sell[i] = True
            holding = False
            wealth[i+1] *= (1-fee)
    
    print(holding)
    
    buy = np.where(buy)[0]
    sell = np.where(sell)[0]
    
    bought = kline[buy]
    sold = kline[sell]
    
    plt.plot(kline/data[0], color='grey', marker="^", markevery=buy, markeredgecolor='green', markerfacecolor='green', markersize=5)
    plt.plot(kline/data[0], ls='', marker="v", markevery=sell, markeredgecolor='red', markerfacecolor='red', markersize=5)
    
    plt.plot(wealth, color='orange')
    
    
    return (np.product(sold / bought) * ((1-fee) ** (bought.size * 2)), bought.size * 2)



bs = cyc['bs']
print(len(bs))
pad = np.zeros(60)
bs = np.concatenate((pad, bs))
print(len(bs))
buy = bs > 0
sell = bs < 0
res = sim(data, buy, sell)

plt.plot(xs[sema*2:], cyc['K2']/data[0], color ="lime", label="fast")
plt.plot(xs[sema*2:], cyc['K3']/data[0], color ="purple", label="slow")
plt.xlabel("Minuten"); plt.ylabel("BTCUSDT")
plt.legend(loc = 'upper left')
plt.grid()

#plt.ylim(1, 1.2)
#plt.ylim(1.00, 3)
#plt.xlim(250000, 270000)
print(res)