# for testing only, should be disabled once finish the beta version
# truncate all tables
import pandas as pd
from pandas import read_csv
import pymysql

config = {}
exec(open("../configure.conf").read(), config)

host_name = config["HOST_NAME"]
user_name = config["USER_NAME"]
password = config["PASSWORD"]
dbname = config["DBNAME"]

conn = pymysql.connect(host = host_name, user = user_name, passwd = password, db = dbname)
cur = conn.cursor()

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

symlist = list(symbols)

for i in range(len(symlist)):
    tmpSym = symlist.pop()

    if tmpSym[0] == "^":
        tmpSym = tmpSym[1:]
    print(tmpSym) 

    if "." in tmpSym:
        tmpSym = tmpSym.replace('.', '_')

    # truncate table
    tmpstr = "Truncate table OPT_{};".format(tmpSym)
    print("{}".format(tmpstr))
    tmpRowCnt = cur.execute(tmpstr)
    #print("{} row affected in table OPT_{}".format(tmpRowCnt, tmpSym))
    ## confirm the tables are blank
    #tmpstr = "select count(*) from OPT_{};".format(tmpSym)
    #cur.execute(tmpstr)
    #tmptuple = cur.fetchone()
    #print("{} row left in table OPT_{}", tmptuple[0], tmpSym)
    
    conn.commit()
    
conn.close()
