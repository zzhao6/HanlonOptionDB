import pymysql
import pandas as pd
from pandas_datareader import data, wb
from pandas_datareader.data import Options
aapl = Options('aapl', 'yahoo')

# test get data from api
# dow = pd.read_csv("../symbols/DJIA.csv")
# for sym in dow.Symbol:
#     tmpOpt = Options(sym, 'yahoo')
#     print("Requesting {}".format(sym))
#     print(tmpOpt.get_call_data())


# import pymysql
# conn = pymysql.connect(host = '127.0.0.1', user = 'root', passwd = 'root', db = 'testoption')
# cur = conn.cursor()
# cur.execute("show columns from testoption1")
# 
# for i in cur:
#     print(i)

# mydata = aapl.get_call_data()
# print(mydata.head(1))

from HanlonDownloader import *

ins = HanlonDownloader("../symbols/DJIA.csv", updateExp=False)
ins.HanlonConn(hanlon_host = "127.0.0.1", hanlon_user = "root", hanlon_passwd = "FErules2014!", hanlon_dbname = "testoption")
#ins._processOne('AAPL', ins.symExpiryDict['AAPL'][9])
ins.processAll()
ins.closeConn()
