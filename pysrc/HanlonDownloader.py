import pandas as pd
import pymysql
from pandas_datareader import data, wb
from pandas_datareader.data import Options

class HanlonDownloader:
    """downloader class"""
    def __init__(self, filedir):
        self.isconnected = False
        print("Downloader created")
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
        self.cur.execute("show columns from AAPL;")

    def _readSymbols(self, filedir):
        try:
            tmpfile = pd.read_csv(filedir)
            self.symbols = tmpfile.Symbol
        except OSError as err:
            print("Error: {}".format(err))
            return
        print("{} symbols loaded".format(len(self.symbols)))
 
    def _processOne(self, sym):
        '''
        process one result of API: one symbol, one expiry
        decomposite the dataframe and push to database
        '''
        oneSymbol = Options(sym, 'yahoo')
        print("Requesting {}".format(sym))
        mydata = oneSymbol.get_call_data()

        # start processing
        for i in range(len(mydata.index)):
            onerow = mydata.iloc[[i]].reset_index()
            # gen sql insert statement
            insert_str = """INSERT INTO {} (underlying_symbol, option_symbol,
            strike, expiry, option_type, quote_date, last, bid, ask, vol,
            open_int, IV, underlying_price) VALUES 
            ('{}', '{}', {}, '{}', '{}', '{}', {}, {}, {}, {}, {}, {}, {})""".format(sym,\
                    onerow.Root[0], onerow.Symbol[0], onerow.Strike[0], \
                    str(onerow.Expiry[0].date()), onerow.Type[0], str(onerow.Quote_Time[0].date()),\
                    onerow.Last[0], onerow.Bid[0], onerow.Ask[0],\
                    onerow.Vol[0], onerow.Open_Int[0], float(onerow.IV[0].strip('%'))/100,\
                    onerow.Underlying_Price[0])
            # push into db
            # self.cur.execute(insert_str) 
            self.cur = self.conn.cursor()
            self.cur.execute("select * from AAPL")
            break
        print("Inserted to table {}".format(sym))
        # end function






















