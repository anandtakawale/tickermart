#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 12 20:49:12 2021

@author: anand
"""

import yfinance as yf
import pandas as pd
from math import floor
from datetime import date
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tickermart.settings')

import django
django.setup()
from pnf.models import Breakout_stock

def getBuySellList(stocks, period ="3mo", interval = "1d"):
    buydf = pd.DataFrame(columns = ["stock_name", "close", "boxsize", "sl"])
    selldf = pd.DataFrame(columns = ["stock_name", "close", "boxsize", "sl"])
    for stock in stocks:
        print(stock)
        stock = stock + ".NS"
        df = yf.download(stock, period = period, interval = interval)
        df.dropna(inplace = True)
        df["datetime"] = df.index
        if len(df) == 0:
            continue
        boxSize = round(df["Close"].iloc[-1] * 0.01)
        if boxSize < 1:
            boxSize = 1
        pnf = pd.DataFrame(columns = ["datetime", "close", "boxsize", "boxnumber", 
                                        "col", "status", 
                                        "last1O", "last2O", "last3O", 
                                        "last1X", "last2X", "last3X",
                                        "signal", "boxVal", "last1OVal",
                                        "last1XVal", "SL"])
        #checking to start with x or o
        boxInit = floor(df["Close"].iloc[0]/boxSize)
        for i in range(len(df)):
            boxnum = floor(df["Close"].iloc[i]/boxSize)
            if boxnum > boxInit:
                pnf.loc[0] = [df["datetime"].iloc[i], df["Close"].iloc[i], 
                                boxSize,
                                boxnum, 0, "X", 
                                "", "", "",
                                "", "", "",
                                "", "", "", "", ""]
                startfrom= i
                break
            elif boxnum < boxInit:
                pnf.loc[0] = [df["datetime"].iloc[i], df["Close"].iloc[i],
                                boxSize,
                                boxnum, 0, "O", 
                                "", "", "",
                                "", "", "",
                                "", "", "", "", ""]
                startfrom = i
                break
            else:
                continue
        for i in range(startfrom+1, len(df)):
            boxnum = floor(df["Close"].iloc[i]/boxSize)
            #previous is X
            if pnf["status"].iloc[-1] == "X": 
                if boxnum > pnf["boxnumber"].iloc[-1]:
                    #continue in upward direction
                    if pnf["last1X"].iloc[-1] and boxnum > pnf["last1X"].iloc[-1]:
                        signal = "buy"
                        last3X = pnf["last2X"].iloc[-1]
                        last2X = pnf["last1X"].iloc[-1]
                        last1X = None
                        sl = (pnf["last1OVal"].iloc[-1] - boxSize) if pnf["last1OVal"].iloc[-1] else None
                    else:
                        signal = ""
                        last3X = pnf["last3X"].iloc[-1]
                        last2X = pnf["last2X"].iloc[-1]
                        last1X = pnf["last1X"].iloc[-1]
                        sl = pnf["SL"].iloc[-1]
                    last3O = pnf["last3O"].iloc[-1]
                    last2O = pnf["last2O"].iloc[-1]
                    last1O = pnf["last1O"].iloc[-1]
                    last1OVal = (last1O * boxSize) if last1O else None
                    last1XVal = (last1X * boxSize) if last1X else None
                    pnf.loc[len(pnf)] = [df["datetime"].iloc[i], df["Close"].iloc[i],
                                         boxSize,
                                         boxnum, pnf["col"].iloc[-1], "X",
                                         last1O, last2O, last3O,
                                         last1X, last2X, last3X,
                                         signal, boxnum * boxSize, last1OVal,
                                         last1XVal, sl]
                                        
                elif boxnum < (pnf["boxnumber"].iloc[-1] - 3):
                    #reversal
                    #reversal crosses last low
                    if pnf["last1O"].iloc[-1] and boxnum < pnf["last1O"].iloc[-1]:
                        signal = "sell"
                        last3O = pnf["last2O"].iloc[-1]
                        last2O = pnf["last1O"].iloc[-1]
                        last1O = None
                        sl = (pnf["last1XVal"].iloc[-1] + boxSize) if pnf["last1XVal"].iloc[-1] else None
                    else:
                        signal = ""
                        last3O = pnf["last3O"].iloc[-1]
                        last2O = pnf["last2O"].iloc[-1]
                        last1O = pnf["last1O"].iloc[-1]
                        sl = pnf["SL"].iloc[-1]
                    last3X = pnf["last2X"].iloc[-1]
                    last2X = pnf["last1X"].iloc[-1]
                    last1X = pnf["boxnumber"].iloc[-1]
                    last1OVal = (last1O * boxSize) if last1O else None
                    last1XVal = (last1X * boxSize) if last1X else None
                    pnf.loc[len(pnf)] = [df["datetime"].iloc[i], df["Close"].iloc[i],
                                         boxSize,
                                         boxnum, pnf["col"].iloc[-1] + 1, "O",
                                         last1O, last2O, last3O,
                                         last1X, last2X, last3X,
                                         signal, boxnum * boxSize, last1OVal,
                                         last1XVal, sl]
                else:
                    continue
            else:
                #previous is O
                if boxnum < pnf["boxnumber"].iloc[-1]:
                    #continue in downward direction
                    if pnf["last1O"].iloc[-1] and boxnum < pnf["last1O"].iloc[-1]:
                        signal = "sell"
                        last3O = pnf["last2O"].iloc[-1]
                        last2O = pnf["last1O"].iloc[-1]
                        last1O = None
                        sl = (pnf["last1XVal"].iloc[-1] + boxSize) if pnf["last1XVal"].iloc[-1] else None
                    else:
                        signal = ""
                        last3O = pnf["last3O"].iloc[-1]
                        last2O = pnf["last2O"].iloc[-1]
                        last1O = pnf["last1O"].iloc[-1]
                        sl = pnf["SL"].iloc[-1]
                    last3X = pnf["last3X"].iloc[-1]
                    last2X = pnf["last2X"].iloc[-1]
                    last1X = pnf["last1X"].iloc[-1]
                    last1OVal = (last1O * boxSize) if last1O else None
                    last1XVal = (last1X * boxSize) if last1X else None
                    pnf.loc[len(pnf)] = [df["datetime"].iloc[i], df["Close"].iloc[i],
                                         boxSize,
                                         boxnum, pnf["col"].iloc[-1], "O",
                                         last1O, last2O, last3O,
                                         last1X, last2X, last3X,
                                         signal, boxnum * boxSize, last1OVal,
                                         last1XVal, sl]
                elif boxnum >= (pnf["boxnumber"].iloc[-1] + 3):
                    #reversal
                    #continue in upward direction
                    if pnf["last1X"].iloc[-1] and boxnum > pnf["last1X"].iloc[-1]:
                        signal = "buy"
                        last3X = pnf["last2X"].iloc[-1]
                        last2X = pnf["last1X"].iloc[-1]
                        last1X = None
                        sl = (pnf["last1OVal"].iloc[-1] - boxSize) if pnf["last1OVal"].iloc[-1] else None
                    else:
                        signal = ""
                        last3X = pnf["last3X"].iloc[-1]
                        last2X = pnf["last2X"].iloc[-1]
                        last1X = pnf["last1X"].iloc[-1]
                        sl = pnf["SL"].iloc[-1]
                    last3O = pnf["last2O"].iloc[-1]
                    last2O = pnf["last1O"].iloc[-1]
                    last1O = pnf["boxnumber"].iloc[-1]
                    last1OVal = (last1O * boxSize) if last1O else None
                    last1XVal = (last1X * boxSize) if last1X else None
                    pnf.loc[len(pnf)] = [df["datetime"].iloc[i], df["Close"].iloc[i],
                                         boxSize,
                                         boxnum, pnf["col"].iloc[-1] + 1, "X",
                                         last1O, last2O, last3O,
                                         last1X, last2X, last3X,
                                         signal, boxnum * boxSize, last1OVal,
                                         last1XVal, sl]
                else:
                    continue
        if pnf["signal"].iloc[-1] == "buy":
            buydf_temp = {"stock_name":stock[:-3].replace("&", "_").replace("-", "_"), 
                          "close": df["Close"].iloc[-1],
                          "boxsize":boxSize,
                          "sl": pnf["last1OVal"].iloc[-1] - boxSize
                          }
            buydf = buydf.append(buydf_temp, ignore_index = True)
        elif pnf["signal"].iloc[-1] == "sell":
            selldf_temp = {"stock_name":stock[:-3].replace("&", "_").replace("-", "_"), 
                          "close": df["Close"].iloc[-1],
                          "boxsize":boxSize,
                          "sl": pnf["last1XVal"].iloc[-1] + boxSize
                          }
            selldf = selldf.append(selldf_temp, ignore_index = True)
    return buydf, selldf

if __name__ == "__main__":
    data = pd.read_csv("./ind_nifty500list.csv", header = 0)
    nifty500 = list(data["Symbol"])
    buydf, selldf = getBuySellList(nifty500, "3mo", "1d")
    buydf = buydf.fillna(0)
    for i in buydf.index:
        sl = round(float(buydf.loc[i].sl), 2)
        stock = Breakout_stock.objects.get_or_create(
            date = date.today(),
            stock_name = buydf.loc[i].stock_name,
            close = round(buydf.loc[i].close, 2),
            boxsize = round(float(buydf.loc[i].boxsize), 2),
            sl = round(float(sl), 2),
            breakout = True
        )[0]
        stock.save()
        print("Created ", buydf.loc[i].stock_name, " on ", date.today(), " for buy")
    selldf = selldf.fillna(0)
    for i in selldf.index:
        sl = round(float(selldf.loc[i].sl), 2)
        stock = Breakout_stock.objects.get_or_create(
            date = date.today(),
            stock_name = selldf.loc[i].stock_name,
            close = round(selldf.loc[i].close, 2),
            boxsize = round(float(selldf.loc[i].boxsize), 2),
            sl = sl,
            breakout = False
        )[0]
        stock.save()
        print("Created ", selldf.loc[i].stock_name, " on ", date.today(), " for sell")