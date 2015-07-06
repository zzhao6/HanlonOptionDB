# for testing only, should be disabled once finish the beta version
# truncate all tables
from pandas import read_csv
import pymysql
# TODO: config file
conn = pymysql.connect(host = "127.0.0.1", user = "root", passwd = "FErules2014!", db = "testoption")
cur = conn.cursor()
symbols = read_csv('../symbols/DJIA.csv') 
symlist = list(symbols.Symbol)

for i in range(len(symlist)):
    tmpSym = symlist.pop()
    # truncate table
    tmpstr = "Truncate table {};".format(tmpSym)
    print("{}".format(tmpstr))
    tmpRowCnt = cur.execute(tmpstr)
    print("{} row affected in table {}".format(tmpRowCnt, tmpSym))
    # confirm the tables are blank
    tmpstr = "select count(*) from {};".format(tmpSym)
    cur.execute(tmpstr)
    tmptuple = cur.fetchone()
    print("{} row left in table{}", tmptuple[0], tmpSym)
    
    conn.commit()
    
conn.close()
