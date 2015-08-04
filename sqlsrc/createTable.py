# for testing only, should be disabled once finish the beta version
# truncate all tables
import pandas as pd
import pymysql

config = {}
exec(open("../configure.conf").read(), config)


host_name = config["HOST_NAME"]
user_name = config["USER_NAME"]
password = config["PASSWORD"]
dbname = config["DBNAME"]



sym_file_djia = config["SYMBOL_FILE_DJIA"]
sym_file_sp = config["SYMBOL_FILE_SP"]
sym_file_etf = config["SYMBOL_FILE_ETF"]
sym_file_vix = config["SYMBOL_FILE_VIX"]
        
tmpsym_djia = pd.read_csv(sym_file_djia)
tmpsym_sp = pd.read_csv(sym_file_sp)
tmpsym_etf = pd.read_csv(sym_file_etf)
tmpsym_vix = pd.read_csv(sym_file_vix)

#symbols = tmpsym_djia.Symbol
#symbols = tmpsym_etf.Symbol
#symbols = tmpsym_vix.Symbol
symbols = pd.concat([tmpsym_sp.Symbol, tmpsym_etf.Symbol, tmpsym_vix.Symbol])


conn = pymysql.connect(host = host_name, user = user_name, passwd = password, db = dbname)
cur = conn.cursor()

from pandas_datareader.data import Options
import pandas_datareader.data


for sym in symbols:
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
    
    tmpstr = """
        CREATE TABLE `{}` (
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
    cur.execute(tmpstr)
    conn.commit()

cur.close()
conn.close()

