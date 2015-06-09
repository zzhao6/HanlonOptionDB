import pandas as pd
import pymysql
from pandas_datareader import data, wb
from pandas_datareader.data import Options

class HanlonDownloader:
    """downloader class"""
    def __init__(self, filedir):
        self.isconnected = False
        self._readSymbols(filedir)

    def HanlonConn(self, hanlon_host, hanlon_user, hanlon_passwd, hanlon_dbname):
        try:
            self.conn = pymysql.connect(host = hanlon_host, user = hanlon_user, passwd = hanlon_passwd, db = hanlon_dbname) 
            self.host = hanlon_host
            self.user = hanlon_user
            self.passwd = hanlon_passwd
            self.dbname = hanlon_dbname
        except pymysql.err.OperationalError as err:
            print(err)
            return
        except pymysql.err.InternalError as err:
            print(err)
            return
        except Exception as e:
            print("Unhandled Exception!")
            print(e)
            return
        
        print("Connected to database: {}".format(self.dbname))
        self.cur = self.conn.cursor()
        self.isconnected = True
        #cur.execute("show columns from testoption1")

    def _readSymbols(self, filedir):
        try:
            tmpfile = pd.read_csv(filedir)
            self.symbols = tmpfile.Symbol
        except OSError as err:
            print("Error: {}".format(err))
            return
        print("{} symbols loaded".format(len(self.symbols)))
