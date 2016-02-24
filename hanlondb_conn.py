import pandas as pd
import pymysql
import getpass
import numpy
import pandas
import logging

class hanlondb_conn:
    """
    An interface between the database and this downloader.
    Provided methods:
        connect()
        disconnect()
        save_to_db() TODO
        _read_symbol_list()
    """
    def __init__(self, conf_obj):
        self.config = conf_obj
        self.host_name = self.config["HOST_NAME"]
        self.db_name = self.config["DBNAME"]
        self.user_name = self.config["USER_NAME"]
        self._read_symbol_list()

    def __del__(self):
        try:
            self.cur.close()
            self.conn.close()
        except pymysql.err.Error as err:
            pass

    def connect(self):
        # user_passwd = getpass.getpass("""
# host: {}
# database: {}
# user name: {}
# Please enter your password:
# """.format(self.host_name, self.db_name, self.user_name))
        user_passwd = self.config["USER_PASSWD"]
        try:
            self.conn = pymysql.connect(host = self.host_name, user = self.user_name, passwd = user_passwd, db = self.db_name)
        except:
            print("Cannot connect to database {}".format(self.db_name))
            raise

        self.cur = self.conn.cursor()
        print("Connected to database {}".format(self.db_name))

    def disconnect(self):
        try:
            self.cur.close()
            self.conn.close()
        except pymysql.err.Error as err:
            return
        print("Connection closed")
    
    def save_to_db(self, sym, mydata):
        """save one symbol to database"""
        mydata = mydata.reset_index()

        # within dataset "mydata", go through each row and insert to DB 
        # in every expiry and every symbol, how many rows have been changed in the database
        rowcnt = 0
        for i in range(len(mydata.index)):
            onerow = mydata.iloc[[i]]
            # clean data, sometime bid and ask contains strange values
            tmpBid = onerow.Bid[i]
            tmpAsk = onerow.Ask[i]
            if type(onerow.Bid[i]) is not numpy.float64:
                tmpBid = 0.0
            if type(onerow.Ask[i]) is not numpy.float64:
                tmpAsk = 0.0
            
            # clean data, sometime open_interest is not a number
            tmpOpenInt = onerow.Open_Int[i]
            if onerow.Open_Int[i] == '-':
                tmpOpenInt = 0                
            # replace missing value '-' with '0'
            # insert_str = insert_str.replace('NaT', '0')
            # insert_str = insert_str.replace(' -,', ' 0,')


            # for index symbols (^VIX ==> VIX)
            tmpsym = sym
            if tmpsym[0] == "^":
                tmpsym = tmpsym[1:]

            # Raw exception handeling function
            self._HandelingRaw(i, onerow)

            # gen sql insert statement
            insert_str = """INSERT INTO OPT_{} (underlying_symbol, option_symbol,
            strike, expiry, option_type, quote_date, last, bid, ask, vol,
            open_int, IV, underlying_price) VALUES 
            ('{}', '{}', {}, '{}', '{}', '{}', {}, {}, {}, {}, {}, {}, {});""".format(tmpsym,\
                    onerow.Root[i], onerow.Symbol[i], onerow.Strike[i], \
                    str(onerow.Expiry[i].date()), onerow.Type[i], str(onerow.Quote_Time[i].date()),\
                    onerow.Last[i], tmpBid, tmpAsk,\
                    onerow.Vol[i], tmpOpenInt, onerow.IV[i],\
                    onerow.Underlying_Price[i])
            # push into db
             
            rowcnt += self.cur.execute(insert_str) 

            self.conn.commit()
        return rowcnt

    def _read_symbol_list(self):
        """Determine which list of symbols to download. The list is set up in the config file"""
        tmpList = ["SYMBOL_FILE_SP", "SYMBOL_FILE_DJIA", "SYMBOL_FILE_ETF", "SYMBOL_FILE_VIX"]
        self.symbols = []
        for k in tmpList:
            if k in self.config:
                tmp_sym_file = pd.read_csv(self.config[k])
                self.symbols = self.symbols + tmp_sym_file.Symbol.tolist()
            else:
                pass

    def _HandelingRaw(self, i, onerow):
        try:
            onerow.Quote_Time[i].date()
        except:
            logging.info("{} - {}: Error generated when reading date from column Quote_Time.".format(sym, expir))
            print("{} - {}: Error generated when reading date from column Quote_Time.".format(sym, expir))
            raise
