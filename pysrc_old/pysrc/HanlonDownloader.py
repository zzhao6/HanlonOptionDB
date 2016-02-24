import pandas as pd
import pymysql
from pandas_datareader import data, wb
from pandas_datareader.data import Options

import pandas_datareader.data   # RemoteDataError

import logging
import pickle       # save expiry dicitonary to file
import getpass
import sys          # display percentage counter, also the error type
import numpy        # for data type checking
import datetime
import urllib       # for handeling exception urllib.error.URLError
from HanlonEmail import *
#from timeout import *       # self-created timeout handeller



#TODO: holidays and weekends
#TODO: log backup
#TODO: timeout
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
        self.emailer = HanlonEmail(confdir)

        # symbols/expir with incomplete requests
        self.RDEAllExpirLst = []    # remote data error while getting expiries
        self.remoteDataErrLst = []  # remote data error
        self.timeoutLst = []        # timeout error

        # err lists after second round requests
        self.remoteDataErrLst2 = []
        self.timeoutLst2 = []
        
        # all other errors
        self.errLst = []            

        # in every expiry and every symbol, how many rows have been changed in the database
        self.rowcnt = 0

        # request timeout
        self.req_timeout_1 = self.config["TIMEOUT_1ST_RND"]
        self.req_timeout_2 = self.config["TIMEOUT_2ND_RND"]

        # read symbol list from symbol file
        # 1. DJIA consituents
        # 2. Major ETFs
        # 3. VIX derivatives

        # dow 30 is included in S&P500
        self.sym_file_djia = self.config["SYMBOL_FILE_DJIA"]
        self.sym_file_etf = self.config["SYMBOL_FILE_ETF"]
        self.sym_file_vix = self.config["SYMBOL_FILE_VIX"]
        
        tmpsym_djia = pd.read_csv(self.sym_file_djia)
        tmpsym_etf = pd.read_csv(self.sym_file_etf)
        tmpsym_vix = pd.read_csv(self.sym_file_vix)
        
        # self.symbols = tmpsym_djia.Symbol
        # self.symbols = tmpsym_etf.Symbol
        # self.symbols = tmpsym_vix.Symbol
        self.symbols = pd.concat([tmpsym_djia.Symbol, tmpsym_etf.Symbol, tmpsym_vix.Symbol])

    def OpenConn(self):
        # read from config obj
        self.host_name = self.config["HOST_NAME"]
        self.user_name = self.config["USER_NAME"]
        self.dbname = self.config["DBNAME"]
        self.password = getpass.getpass("Enter password for DB user {}@{}: ".format(self.user_name, self.host_name))

        # connect to database
        self.conn = pymysql.connect(host = self.host_name , user = self.user_name, passwd = self.password, db = self.dbname) 
        self.cur = self.conn.cursor()
        logging.info("Top level: Connected to db: {}".format(self.dbname))

    def CloseConn(self):
        self.cur.close()
        self.conn.close()
        logging.info("Top level: Connection closed.")
        print("Top level: Connection closed.")
    
    # def _SendSummaryEmail():
        # # print("Top level: Sending summary email.")
        # # self.emailer.setSummaryMsg(start_time, end_time, spent_time, numSymRequested, numSymCompleted, numRemoteErr, numErrGenerated)
        # # self.emailer.sendMsg()
        # # logging.info("Top level: Summary email has been sent to {}".format(self.emailer.email_to))
        # # print("Top level: Summary email has been sent to {}".format(self.emailer.email_to))
        # '''
        # need to rewrite this function
        # '''
        # pass

    # def _SendErrorEmail(self, sym, expir, strike, err_type, err):
        # print("{} - {}: ERROR: sending error email.".format(sym, expir))
        # self.emailer.setErrMsg(sym, expir, strike, err_type, err)
        # self.emailer.sendMsg()

    # def _HandelingRaw(self, i, onerow):
        # try:
            # onerow.Quote_Time[i].date()
        # except:
            # logging.info("{} - {}: Error generated when reading date from column Quote_Time.".format(sym, expir, self.rowcnt))
            # print("{} - {}: Error generated when reading date from column Quote_Time.".format(sym, expir, self.rowcnt))
            # raise

    def _ProcessOne(self, sym, expir, time_out=None):
        """
        process one symbol, one expiry date, one strike
        time_out: maximum seconds waiting for the request
        """
        if time_out == None:
            time_out = self.req_timeout_1   # the default timeout length

        tmpOption = Options(sym, 'yahoo')

        logging.info("{} - {}: Requesting".format(sym, expir))
        # set timeout for single request
        with timeout(seconds = time_out):
            mydata = tmpOption.get_options_data(expiry = expir)
            
        logging.info("{} - {}: Finished request, insert to table...".format(sym, expir))
        mydata = mydata.reset_index()

        # within dataset "mydata", go through each row and insert to DB 
        for i in range(len(mydata.index)):
            onerow = mydate.iloc[[i]]
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
            self,_HandelingRaw(i, onerow)

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
                # exception while inserting to database
                print("Exception occured while inserting to database")
                print(insert_str)
                print(mydata.iloc[[i]])
                logging.error("Exception occured while inserting to database")
                logging.error(insert_str)
                logging.error(mydata.iloc[[i]])
                raise

            self.conn.commit()
            # end of for loop

        logging.info("{} - {}: Inserted to table, {} rows affected.".format(sym, expir, self.rowcnt))
        print("{} - {}: Inserted to table, {} rows affected.".format(sym, expir, self.rowcnt))
        self.rowcnt = 0
        # end function process one

    # # TODO: finish this function, and put this in the ProcessAll function
    # def _ProcessOtherErrLst(self):
        # """
        # if len(self.remoteDataErrLst) != 0:
            # logging.info("Top level: Processing RemoteDataError list: {}".format(self.remoteDataErrLst))
            # print("Top level: Processing RemoteDataError list: {}".format(self.remoteDataErrLst))
            # self.remoteDataErrLst = self._ProcessRDEList()
            
            # if (len(self.remoteDataErrLst) == 0):
                # logging.info("Top level: all remote data error has been processed")
            # else:
                # logging.error("Top level: Error: still have remote data error: {}".format(self.remoteDataErrLst))
                # self._SendErrorEmail(self.remoteDataErrLst, "none", "none", "RemoteDataError")
        # send request of symbols with other errors
        # """
        # pass


    # def _ProcessRDEList(self):
        # """
        # send request of the symbols which were generating RemoteDataError
        # """
        # logging.info("Top level: Second round: RDE symbols, {} in total".format(len(self.remoteDataErrLst)))   
        # print("Top level: Second round: RDE symbols, {} in total".format(len(self.remoteDataErrLst)))   
        # for sym, expir in self.remoteDataErrLst:
            # try:
                # self._ProcessOne(sym, expir)
            # # if have error again, add to 2nd round lists
            # except pandas_datareader.data.RemoteDataError:
                # logging.error("{} - {}: RemoteDataError".format(sym, expir))
                # print("{} - {}: RemoteDataError".format(sym, expir))
                # self.remoteDataErrLst2.append((sym, expir))
            # except (urllib.error.URLError, TimeoutError) as err:
                # print("{} - {}: {}".format(sym, expir, err))
                # logging.error("{} - {}: {}".format(sym, expir, err))
                # self.timeoutLst2.append((sym, expir))
            # except Exception as err:
                # self.errLst.append((sym, errStr))
                # raise

    # def _ProcessTimeoutLst(self):
        # """
        # send request of symbols with timeout error
        # """
        # logging.info("Top level: Second round: timeout symbols, {} in total".format(len(self.timeoutLst)))   
        # print("Top level: Second round: timeout symbols, {} in total".format(len(self.timeoutLst)))   
        # for sym, expir in self.timeoutLst:
            # try:
                # self._ProcessOne(sym, expir)
            # # if have error again, add to 2nd round lists
            # except pandas_datareader.data.RemoteDataError:
                # logging.error("{} - {}: RemoteDataError".format(sym, expir))
                # print("{} - {}: RemoteDataError".format(sym, expir))
                # self.remoteDataErrLst.append((sym, expir))
            # except (urllib.error.URLError, TimeoutError) as err:
                # print("{} - {}: {}".format(sym, expir, err))
                # logging.error("{} - {}: {}".format(sym, expir, err))
                # self.timeoutLst2.append((sym, expir))
            # except Exception as err:
                # self.errLst.append((sym, err))
                # raise

    # #TODO: first round and second round summary
    # def ProcessAll(self):
        # """
        # process all symbols in symbol list file
        # """
        # logging.info("Top level: First round Request Start: {} in total.".format(len(self.symbols)))
        # print("Top level: First round Request Start: {} in total.".format(len(self.symbols)))
        # self.emailer.setIdvMsg("Downloading started", "--")
        # self.emailer.sendMsg()

        # # some statistics for the summary email
        # numSymRequested = 0
        # numSymCompleted = 0
        
        # start_time = datetime.datetime.now() 
        # ### first round request ###
        # # start request
        # for sym in self.symbols:
            # tmpOptionObj = Options(sym, 'yahoo')
            
            # try:
                # tmpExpirList = tmpOptionObj.expiry_dates
            # except pandas_datareader.data.RemoteDataError:
                # self.RDEAllExpirLst.append(sym)                                     # error list 1
                # print("{} - {}: RemoteDataError for all expiries".format(sym, "AllExpir"))
                # logging.error("{} - {}: RemoteDataError for all expiries".format(sym, "AllExpir"))
                # # skip requesting for this symbol under such error  
                # continue        

            # for expir in tmpExpirList:
                # try:
                    # self._ProcessOne(sym, expir)
                # except pandas_datareader.data.RemoteDataError:
                    # self.remoteDataErrLst.append((sym, expir))                      # error list 2
                    # logging.error("{} - {}: RemoteDataError".format(sym, expir))
                    # print("{} - {}: RemoteDataError".format(sym, expir))
                    # continue
                # except (urllib.error.URLError, TimeoutError) as err:
                    # self.timeoutLst.append((sym, expir))                            # error list 3
                    # print("{} - {}: {}".format(sym, expir, err))
                    # logging.error("{} - {}: {}".format(sym, expir, err))
                    # continue
                # except pymysql.err.IntegrityError as err:
                    # # TODO: complete this exception handling: data duplicate error
                    # #logging.error("{} - {}: DuplicateKeyError, push to self err list".format(sym, expir))
                    # #print("{} - {}: DuplicateKeyError, push to self err list".format(sym, expir))
                    # #self.errLst.append(err)
                    # #continue
                    # pass
                # except Exception as err:
                    # self.errLst.append((sym, err))                               # error list 4

                    # exc_type, exc_obj, exc_tb = sys.exc_info()  # get err type
                    # errStr = "{} - {}: Error:Unhandled exception. {}: {}".format(sym, expir, exc_type, err) 
                    # logging.error(errStr)
                    # print(errStr)

                    # self.CloseConn()
                    # self._SendErrorEmail(sym, expir, "none", exc_type, err)
                    # input("Press any key to raise the exception.")
                    # raise

        # ### second round request ###
        # self._ProcessRDEList()
        # self._ProcessTimeoutLst()
        # self._ProcessOtherErrLst()

        # end_time = datetime.datetime.now()

        # start_time_str = "{:%b-%d-%Y %H:%M:%S}".format(start_time)  
        # end_time_str = "{:%b-%d-%Y %H:%M:%S}".format(end_time)
        # diff_time = end_time - start_time
        # diff_time_sec = diff_time.total_seconds()
        # diff_time_sec = round(diff_time_sec, 2)

        # # TODO: rewrite this part
        # self._SendSummaryEmail()
        # # TODO: get num of err generated, and put into summary email
