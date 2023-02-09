# -*- coding: utf-8 -*-
"""
Created on Mon Jun  6 10:16:48 2022

@author: Beni

Cut down on big crypto csv files to sync them and extract closing price
"""
import numpy as np

def read(file, row_start):
    # reading only seventh column starting on specified row + 2
    return np.loadtxt(file, delimiter = ',', skiprows = (2+row_start), usecols = 6)

def convert(fname):
    # reading all the dates
    date = np.loadtxt(fname, dtype=str, delimiter = ',', skiprows = 2, usecols = 1)
    pos = np.where(date == "2022-03-10 23:59:00")[0][0] # finding row with date
    close_raw = read(fname, pos) # only reading file starting at date
    close = np.flip(close_raw[:525600])
    new_name = "cut_" + fname # making new name
    np.savetxt(new_name, close, fmt='%1.2f') # saving closing price with dble prec.
    

convert("Binance_ETHUSDT_minute.csv")
convert("Binance_BTCUSDT_minute.csv")
convert("Binance_LTCUSDT_minute.csv")
convert("Binance_DASHUSDT_minute.csv")