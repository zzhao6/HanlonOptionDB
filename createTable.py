# for testing only, should be disabled once finish the beta version
# truncate all tables
from hanlondb_conn import *
from pandas_datareader.data import Options
import pandas_datareader.data
import pandas as pd
import pymysql
import getpass
import sys
config = {}
exec(open("./configure.conf").read(), config)

dbconn = hanlondb_conn(config)
dbconn.connect()

for sym in dbconn.symbols:
    #tmpOpt = Options(sym, 'yahoo')
        
    #try:
    #    tmpOpt.expiry_dates
    #    #print(sym)
    #except pandas_datareader.data.RemoteDataError:
    #    print("{} - RemoteDataError!!".format(sym))
    #except:
    #    raise

    # create table for all symbols here
    if sym[0] == "^":
        sym = sym[1:]
    
    if "." in sym:
        sym = sym.replace('.', '_')

    tmpstr = """
        CREATE TABLE `OPT_{}` (
          `underlying_symbol` varchar(10) NOT NULL,
          `option_symbol` varchar(50) NOT NULL,
          `strike` float NOT NULL,
          `expiry` date NOT NULL,
          `option_type` varchar(4) NOT NULL,
          `quote_date` date NOT NULL,
          `last` float NOT NULL,
          `bid` float NOT NULL,
          `ask` float NOT NULL,
          `vol` int(11) NOT NULL,
          `open_int` int(11) NOT NULL,
          `IV` float NOT NULL,
          `underlying_price` float NOT NULL
        );""".format(sym)
    try:
        dbconn.cur.execute(tmpstr)
        dbconn.conn.commit()
        tmpstr2 = "ALTER TABLE `OPT_{}` ADD PRIMARY KEY (`quote_date`, `option_symbol`)".format(sym)
        dbconn.cur.execute(tmpstr2)
        dbconn.conn.commit()
    except pymysql.err.InternalError as err:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        print(exc_value)

dbconn.disconnect()
