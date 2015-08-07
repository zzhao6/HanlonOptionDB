import pandas as pd
import pymysql
from pandas_datareader import data, wb
from pandas_datareader.data import Options

import pandas_datareader.data   # RemoteDataError

import logging
import pickle       # save expiry dicitonary to file
import getpass
import sys          # display percentage counter
import numpy        # for data type checking
import datetime
from HanlonEmail import *

#TODO: holidays and weekends
#TODO: log backup
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

        # remote data err list, as this err is common
        self.remoteDataErrLst = []

        # in every expiry and every symbol, how many rows have been changed in the database
        self.rowcnt = 0

        # read symbol list from symbol file
        # 1. DJIA consituents
        # 2. Major ETFs
        # 3. VIX derivatives

        # dow 30 is included in S&P500
        self.sym_file_djia = self.config["SYMBOL_FILE_DJIA"]
        self.sym_file_sp = self.config["SYMBOL_FILE_SP"]
        self.sym_file_etf = self.config["SYMBOL_FILE_ETF"]
        self.sym_file_vix = self.config["SYMBOL_FILE_VIX"]
        
        tmpsym_sp = pd.read_csv(self.sym_file_sp)
        tmpsym_djia = pd.read_csv(self.sym_file_djia)
        tmpsym_etf = pd.read_csv(self.sym_file_etf)
        tmpsym_vix = pd.read_csv(self.sym_file_vix)
        
        #self.symbols = tmpsym_sp.Symbol
        #self.symbols = tmpsym_etf.Symbol
        #self.symbols = tmpsym_vix.Symbol
        self.symbols = pd.concat([tmpsym_sp.Symbol, tmpsym_etf.Symbol, tmpsym_vix.Symbol])

    def OpenConn(self):
        # read from config obj
        self.host_name = self.config["HOST_NAME"]
        self.user_name = self.config["USER_NAME"]
        self.dbname = self.config["DBNAME"]

        self.password = self.config["PASSWORD"]
        #self.password = getpass.getpass("Enter password for DB {}: ".format(self.dbname))

        # connect to database
        self.conn = pymysql.connect(host = self.host_name , user = self.user_name, passwd = self.password, db = self.dbname) 
        self.cur = self.conn.cursor()
        logging.info("Top level: Connected to db: {}".format(self.dbname))


    def CloseConn(self):
        self.cur.close()
        self.conn.close()
        logging.info("Top level: Connection closed.")
        print("Top level: Connection closed.")

    
    def _SendSummaryEmail(self, start_time, end_time, spent_time, numSymRequested, numSymCompleted, numRemoteErr, numErrGenerated):
        print("Top level: Sending summary email.")
        self.emailer.setSummaryMsg(start_time, end_time, spent_time, numSymRequested, numSymCompleted, numRemoteErr, numErrGenerated)
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
        errStr = "{} - {}: Error:Unhandled exception. {}".format(sym, expir, err) 
        self.errlist.append(errStr)

        logging.error("{} - {}: Error:Unhandled exception. {}".format(sym, expir, err))


    def _ProcessOne(self, sym, expir):
        """
        process one symbol, one expiry date, one strike
        """
        tmpOption = Options(sym, 'yahoo')

        logging.info("{} - {}: Requesting".format(sym, expir))
        mydata = tmpOption.get_options_data(expiry = expir)
            
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

            # gen sql insert statement
            insert_str = """INSERT INTO OPT_{} (underlying_symbol, option_symbol,
            strike, expiry, option_type, quote_date, last, bid, ask, vol,
            open_int, IV, underlying_price) VALUES 
            ('{}', '{}', {}, '{}', '{}', '{}', {}, {}, {}, {}, {}, {}, {});""".format(tmpsym,\
                    onerow.Root[i], onerow.Symbol[i], onerow.Strike[i], \
                    str(onerow.Expiry[i].date()), onerow.Type[i], str(onerow.Quote_Time[i].date()),\
                    onerow.Last[i], tmpBid, tmpAsk,\
                    onerow.Vol[i], tmpOpenInt, float(onerow.IV[i].strip('%'))/100,\
                    onerow.Underlying_Price[i])
            # push into db
             
            try:
                self.rowcnt += self.cur.execute(insert_str) 
            except Exception as err:
                #print("--{}".format(onerow.Bid[i]))
                print(insert_str)
                print(mydata.iloc[[i]])
                self._PrintException(err)
                raise


            self.conn.commit()
            # end of for loop

        logging.info("{} - {}: Inserted to table, {} rows affected.".format(sym, expir, self.rowcnt))
        print("{} - {}: Inserted to table, {} rows affected.".format(sym, expir, self.rowcnt))
        self.rowcnt = 0
        # end function process one
    

    # TODO: finish this function, and put this in the ProcessAll function
    def _ProcessRDEList(self):
        """
        send request of the symbols which were generating RemoteDataError
        """
        tmpRDElist = [] 
        for sym in self.remoteDataErrLst:
            tmpOptionObj = Options(sym, 'yahoo')

            try:
                tmpExpirList = tmpOptionObj.expiry_dates
            except pandas_datareader.data.RemoteDataError:
                tmpRDElist.append(sym)
                logging.error("{} - {}: RemoteDataError again".format(sym, "None"))
                print("{} - {}: RemoteDataError again".format(sym, "None"))
                continue

        return tmpRDElist
    


    def ProcessAll(self):
        """
        process all symbols in symbol list file
        """
        logging.info("Start to process all symbols: {} in total.".format(len(self.symbols)))
        print("Start to process all symbols: {} in total.".format(len(self.symbols)))
        self.emailer.setIdvMsg("Downloading started", "--")
        self.emailer.sendMsg()

        # some statistics for the summary email
        start_time = datetime.datetime.now() 
        numSymRequested = 0
        numSymCompleted = 0
        numErrGenerated = 0

        # start request
        for sym in self.symbols:
            tmpOptionObj = Options(sym, 'yahoo')
            
            try:
                tmpExpirList = tmpOptionObj.expiry_dates
            except pandas_datareader.data.RemoteDataError:
                self.remoteDataErrLst.append(sym)
                logging.error("{} - {}: RemoteDataError, pushed to the list, will try again later".format(sym, "None"))
                print("{} - {}: RemoteDataError, pushed to the list, will try again later".format(sym, "None"))
                continue

            numSymRequested += 1

            for expir in tmpExpirList:
                try:
                    self._ProcessOne(sym, expir)
                except pandas_datareader.data.RemoteDataError:
                    self.remoteDataErrLst.append(sym)
                    logging.error("{} - {}: RemoteDataError, pushed to the list, will try again later".format(sym, "None"))
                    print("{} - {}: RemoteDataError, pushed to the list, will try again later".format(sym, "None"))
                    continue
                except pymysql.err.IntegrityError as err:
                    logging.error("{} - {}: DuplicateKeyError, push to self err list".format(sym, expir))
                    print("{} - {}: DuplicateKeyError, push to self err list".format(sym, expir))
                    self.errlist.append(err)
                    # TODO: complete this exception handling: data duplicate error
                    continue
                except Exception as err:
                    numErrGenerated += 1
                    self.errlist.append(err)
                    self._PrintException(err, sym, expir)
                    self.CloseConn()
                    self._SendErrorEmail(sym, expir, "none", err)
                    input("Press any key to raise the exception.")
                    raise

            numSymCompleted += 1

        # send request again for symbols with remote data error
        if len(self.remoteDataErrLst) != 0:
            logging.info("Top level: Processing RemoteDataError list: {}".format(self.remoteDataErrLst))
            print("Top level: Processing RemoteDataError list: {}".format(self.remoteDataErrLst))
            self.remoteDataErrLst = self._ProcessRDEList()
            
            if (len(self.remoteDataErrLst) == 0):
                logging.info("Top level: all remote data error has been processed")
            else:
                logging.error("Top level: Error: still have remote data error: {}".format(self.remoteDataErrLst))
                self._SendErrorEmail(self.remoteDataErrLst, "none", "none", "RemoteDataError")


        end_time = datetime.datetime.now()

        start_time_str = "{:%b-%d-%Y %H:%M:%S}".format(start_time)  
        end_time_str = "{:%b-%d-%Y %H:%M:%S}".format(end_time)
        diff_time = end_time - start_time
        diff_time_sec = diff_time.total_seconds()
        diff_time_sec = round(diff_time_sec, 2)

        self._SendSummaryEmail(start_time_str, end_time_str, diff_time_sec, \
                               numSymRequested, numSymCompleted, len(self.remoteDataErrLst), numErrGenerated)
        # TODO: get num of err generated, and put into summary email
