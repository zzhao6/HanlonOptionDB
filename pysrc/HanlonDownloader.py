import pandas as pd
import pymysql
from pandas_datareader import data, wb
from pandas_datareader.data import Options

import logging
import pickle       # save expiry dicitonary to file

import sys          # display percentage counter
import numpy        # for data type checking
import datetime
from HanlonEmail import *


class HanlonDownloader:
    """


    """
    def __init__(self, confdir):
        """
        initialized most fields by config file
        """
        self.config = {}
        exec(open(confdir).read(), self.config)

        # config logger
        logging.basicConfig(filename = self.config["LOG_FILE"], level=logging.INFO, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S')

        # config emailer
        self.emailer = HanlonEmail(self.config)

        # err message list, will put in summary
        self.errlist = []

        # in every expiry and every symbol, how many rows have been changed in the database
        self.rowcnt = 0

        # read symbol list from symbol file
        self.sym_file = self.config["SYMBOL_FILE"]
        tmpfile = pd.read_csv(self.sym_file)
        self.symbols = tmpfile.Symbol 


    def OpenConn(self):
        # read from config obj
        self.host_name = self.config["HOST_NAME"]
        self.user_name = self.config["USER_NAME"]
        self.password = self.config["PASSWORD"]
        self.dbname = self.config["DBNAME"]

        # connect to database
        self.conn = pymysql.connect(host = self.host_name , user = self.user_name, passwd = self.password, db = self.dbname) 
        self.cur = self.conn.cursor()
        logging.info("Top level: Connected to db: {}".format(self.dbname))


    def CloseConn(self):
        self.cur.close()
        self.conn.close()
        logging.info("Top level: Connection closed!")
        print("Top level: Connection closed!")

    
    def _SendSummaryEmail(self, start_time, end_time, spent_time, numSymRequested, numSymCompleted):
        self.emailer.setRegMsg(start_time, end_time, spent_time, numSymRequested, numSymCompleted, "")
        self.emailer.sendMsg()
        logging.info("Top level: Summary email has been sent to {}".format(self.emailer.email_to))
        print("Top level: Summary email has been sent to {}".format(self.emailer.email_to))


    def _SendErrorEmail(self, sym, expir, strike, err):
        print("{} - {}: ERROR: sending error email.".format(sym, expir))
        self.emailer.setErrMsg(sym, expir, strike, err)
        self.emailer.sendMsg()


    def _PrintException(self, err, sym = "", expir = ""):
        """ 
        print and logging some messages about unhandled exception
        """ 
        errStr = "{} - {}: Unhandled exception. {}".format(sym, expir, err) 
        self.errlist.append(errStr)

        logging.exception("{} - {}: Unhandled exception. {}".format(sym, expir, err))


    def _ProcessOne(self, sym, expir):
        """
        process one symbol, one expiry date, one strike
        """
        tmpOption = Options(sym, 'yahoo')

        try:
            # TODO: handle RemoteDataError exception. Sometime the yahoo server doesn't response
            logging.info("{} - {}: Requesting".format(sym, expir))
            mydata = tmpOption.get_options_data(expiry = expir)
        except Exception as err:
            self._PrintException(err, sym, expir)
            self.CloseConn()
            self._SendErrorEmail(sym, expir, "none", err)
            input("Press any key to raise the exception.")
            raise
            
        logging.info("{} - {}: Finished request, insert to table...".format(sym, expir))
        mydata = mydata.reset_index()

        # within dataset "mydata", go through each row and insert to DB 
        for i in range(len(mydata.index)):
            onerow = mydata.iloc[[i]]
            
            # clean data, sometime bid and ask contains strange values
            tmpBid = onerow.Bid[i]
            tmpAsk = onerow.Ask[i]
            if type(onerow.Bid[i]) is not numpy.float64:
                tmpBid = 0.0
            if type(onerow.Ask[i]) is not numpy.float64:
                tmpAsk = 0.0
            
            # gen sql insert statement
            insert_str = """INSERT INTO {} (underlying_symbol, option_symbol,
            strike, expiry, option_type, quote_date, last, bid, ask, vol,
            open_int, IV, underlying_price) VALUES 
            ('{}', '{}', {}, '{}', '{}', '{}', {}, {}, {}, {}, {}, {}, {});""".format(sym,\
                    onerow.Root[i], onerow.Symbol[i], onerow.Strike[i], \
                    str(onerow.Expiry[i].date()), onerow.Type[i], str(onerow.Quote_Time[i].date()),\
                    onerow.Last[i], tmpBid, tmpAsk,\
                    onerow.Vol[i], onerow.Open_Int[i], float(onerow.IV[i].strip('%'))/100,\
                    onerow.Underlying_Price[i])
            # push into db
            # TODO: this execute will return row count
             
            # replace missing value '-' with '0'
            # insert_str = insert_str.replace('NaT', '0')
            # insert_str = insert_str.replace(' -,', ' 0,')

            try:
                self.rowcnt += self.cur.execute(insert_str) 
            except Exception as err:
                print(type(onerow.Bid[i]))
                self._printException(err)

            self.conn.commit()
            # end of for loop

        logging.info("{} - {}: Inserted to table, {} rows affected.".format(sym, expir, self.rowcnt))
        print("{} - {}: Inserted to table, {} rows affected.".format(sym, expir, self.rowcnt))
        self.rowcnt = 0
        # end function process one
    

    def ProcessAll(self):
        """
        process all symbols in symbol list file
        """
        logging.info("Start to process all symbols: {} in total.".format(len(self.symbols)))
        print("Start to process all symbols: {} in total.".format(len(self.symbols)))
        
        # some statistics for the summary email
        start_time = datetime.datetime.now() 
        numSymRequested = 0
        numSymCompleted = 0

        # start request
        for sym in self.symbols:
            tmpOptionObj = Options(sym, 'yahoo')
            tmpExpirList = tmpOptionObj.expiry_dates

            for expir in tmpExpirList:
                
                numSymRequested += 1
                self._ProcessOne(sym, expir)
                numSymCompleted += 1

        end_time = datetime.datetime.now()

        start_time_str = "{:%b-%d-%Y %H:%M:%S}".format(start_time)  
        end_time_str = "{:%b-%d-%Y %H:%M:%S}".format(end_time)
        diff_time = end_time - start_time
        diff_time_sec = diff_time.total_seconds()
        diff_time_sec = round(diff_time_sec, 2)

        self._SendSummaryEmail(start_time_str, end_time_str, diff_time_sec, \
                               numSymRequested, numSymCompleted)
        # TODO: get num of err generated, and put into summary email
