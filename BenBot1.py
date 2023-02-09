from framework.Bot import *
import numpy as np


class BenBot1(Bot):

    #sample_parameter: Annotated[int, Param] = 5
    erp: Annotated[int, Param] = 10*20 # erp = efficiency ratio für 10 Perioden
    fema: Annotated[int, Param] = 2*20 # fast exponential mov. avg. 2 P
    sema: Annotated[int, Param] = 30*19 # slow exponential mov. avg. 30 P 
    # (alle drei im 10, 2, 30 Verhältnis, daher das *20 um das Verhältnis zu sehen)
    # sema mit kleiner Abweichung auf *19 nach Gefühl eine Spur besser
    fperc: Annotated[int, Param] = 0.2 # failsafe percentage is how much KAMA can differ from current price
    
    def __init__(self):
        # alle drei KAMAwerte initialisieren, Platz zum zwischenspeichern
        self.prior_KAMA = None
        self.prior_KAMA2 = None
        self.prior_KAMA3 = None
        #self.sample_parameter = 5
        # fast and slow smoothing constant von Perioden abhängig (nicht wie SC unten)
        self.fSC = 2/(fema+1)
        self.sSC = 2/(sema+1)
        pass
    # kama function rechnet nur als Zwischenschritt die Smoothing Constant aus
    def kama(erp, fema, sema, data):
        p1 = data[(sema*2-erp*2):sema*2] #
        change = abs(p1[-1] - p1[0])
        p1_start = p1[::2]
        p1_end = p1[1::2]
        
       #short_p1 = p1 #p3[(sema*2-erp):sema*2]
        
        summ = np.sum(np.abs(p1_end - p1_start)) # volatility sum
        
        if(summ == 0): # zur Sicherheit falls summ nahe an 0 ist
            summ = 0.1
        # Efficiency Ratio von 0 bis 1, instabil -> viel Veränderung im Kurs -> 1, no change -> 0
        ER = change/summ 

        SC = (ER * (self.fSC - self.sSC) + self.sSC)**2
        #short_SC = (short_ER * (2/((fema/2)+1) - sSC) + sSC)**2
        return SC

    def assess(self, symbol: str) -> float:
        """
         * returns a value representing the bots recommendation to either buy or sell
         *  negative value -> sell
         *  positive value -> buy
         * high absolute values -> high confidence
        """
        #self.last = 5

        #k = self._market.get_kline(symbol, 60)
        
        # sema Perioden brauchen sema*2 Zeitpunkte
        p3 = self._market.get_kline(symbol, sema*2) #sema*2 an Zeitpunkten abfragen
        SC = kama(erp, fema, sema, p3) # Smoothing Constant
        SC2 = kama(int(erp/2), int(fema/2), int(sema/2), p3) # Änderung der Perioden hier
        SC3 = kama(int(erp/2), int(fema/1.5), int(sema/2), p3) # Extra KAMA linien zeigen Trends
        
        if self.prior_KAMA == None:
            # rechnet voll über sema KAMAwerte für einen neuen aktuellen KAMA
            # volles array mit allen Werten für sema zeitpunkte
            pn = self._market.get_kline(symbol, sema*3) 
            # erster Wert als SMA
            self.prior_KAMA, self.prior_KAMA2, self.prior_KAMA3 = np.average(pn[:sema*2])
            for i in sema: 
                p4 = pn[i:(sema*2 + i)]
                nSC = kama(erp, fema, sema, p4)
                nSC2 = kama(int(erp/2), int(fema/2), int(sema/2), p4)
                nSC3 = kama(int(erp/2), int(fema/1.5), int(sema/2), p4)
                nKAMA = self.prior_KAMA + nSC*(p4[-1] - self.prior_KAMA)
                nKAMA2 = self.prior_KAMA2 + nSC2*(p4[-1] - self.prior_KAMA2)
                nKAMA3 = self.prior_KAMA3 + nSC3*(p4[-1] - self.prior_KAMA3)
                
                # failsafe for big fluctuations / anomalies
                if(abs(abs(nKAMA) - p4[-1]) > p4[-1]*fperc):
                     nKAMA = np.average(p4)
                if(abs(abs(nKAMA2) - p4[-1]) > p4[-1]*fperc):
                     nKAMA2 = np.average(p4[sema:])
                if(abs(abs(nKAMA3) - p4[-1]) > p4[-1]*fperc):
                     nKAMA3 = np.average(p4[sema:])
                self.prior_KAMA = nKAMA
                self.prior_KAMA2 = nKAMA2
                self.prior_KAMA3 = nKAMA3
            
            
            
            
        KAMA = self.prior_KAMA + SC*(p3[-1] - prior_KAMA)
        KAMA2 = self.prior_KAMA2 + SC2*(p3[-1] - prior_KAMA2)
        KAMA3 = self.prior_KAMA3 + SC3*(p3[-1] - prior_KAMA3)
         
        # failsafe for big fluctuations / anomalies
        # Zu große Abweichungen vom Kurs werden so gebremst
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
        
        # Wert für nächsten Zyklus gespeichert
        self.prior_KAMA = KAMA
        self.prior_KAMA2 = KAMA2
        self.prior_KAMA3 = KAMA3
        
        return res

    def propose_actions(self) -> list[BrokerAction]:
        """
         * returns a list of proposed BrokerActions
        """
        return []
