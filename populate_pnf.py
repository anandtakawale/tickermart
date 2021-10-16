import os
from django.db.models import fields
import pandas as pd
from datetime import datetime
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tickermart.settings')

import django
django.setup()

from pnf.models import Breakout_stock

def find_csv_filepaths( path_to_dir, suffix=".csv" ):
    filenames = os.listdir(path_to_dir)
    return [ os.path.join(path_to_dir, filename) for filename in filenames if filename.endswith( suffix ) ]

if __name__ == "__main__":
    folderpath = r"/media/anand/Study/stockMarket/pointsAndFIgures/stocksData/yfinance/pnfData"
    filePaths = find_csv_filepaths(folderpath)
    for filePath in filePaths:
        basename = os.path.basename(filePath)
        stockname = basename[:-11]
        stockname = stockname.replace("&", "_")
        stockname = stockname.replace("-", "_")
        df = pd.read_csv(filePath, index_col = 0)
        buydf = df[df.signal == "buy"]
        buydf = buydf.fillna(0)
        for i in buydf.index:
            d = buydf.loc[i].datetime
            sl = round(buydf.loc[i].SL, 2)
            stock = Breakout_stock.objects.get_or_create(
                date = datetime.strptime(d, '%Y-%m-%d').date(),
                stock_name = stockname,
                close = round(buydf.loc[i].close, 2),
                boxsize = round(float(buydf.loc[i].boxsize), 2),
                sl = sl,
                breakout = True
            )[0]
            stock.save()
            print("Created ", stockname, " on ", d, " for buy")

        selldf = df[df.signal == "sell"]
        selldf = selldf.fillna(0)
        for i in selldf.index:
            d = selldf.loc[i].datetime
            stock = Breakout_stock.objects.get_or_create(
                date = datetime.strptime(d, '%Y-%m-%d').date(),
                stock_name = stockname,
                close = round(selldf.loc[i].close, 2),
                boxsize = round(float(selldf.loc[i].boxsize), 2),
                sl = round(float(selldf.loc[i].SL), 2),
                breakout = False
            )[0]
            stock.save()
            print("Created ", stockname, " on ", d, " for sell")