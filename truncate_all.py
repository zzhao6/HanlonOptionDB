# for testing only, should be disabled once finish the beta version
# truncate all tables
from hanlondb_conn import *
from pandas_datareader.data import Options
import pandas_datareader.data
import pandas as pd
import pymysql
import getpass

config = {}
exec(open("./configure.conf").read(), config)

dbconn = hanlondb_conn(config)
dbconn.connect()

symlist = list(dbconn.symbols)

for i in range(len(symlist)):
    tmpSym = symlist.pop()

    if tmpSym[0] == "^":
        tmpSym = tmpSym[1:]
    print(tmpSym) 

    if "." in tmpSym:
        tmpSym = tmpSym.replace('.', '_')

    # truncate table
    tmpstr = "Truncate table OPT_{};".format(tmpSym)
    tmpRowCnt = dbconn.cur.execute(tmpstr)
    dbconn.conn.commit()
    
dbconn.disconnect()
