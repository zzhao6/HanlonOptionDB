from hanlondb_conn import *
from email_sender import *
from timeout import *
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
import time

class option_downloader:
    """
    The main downloader. Contains one email_sender obj and one hanlondb_conn obj.
    """
    def __init__(self):
        self.conf = {}
        exec(open("./configure.conf").read(), self.conf)
        self.db_conn = hanlondb_conn(self.conf)     # db connector and email sender
        self.email_sender = email_sender(self.conf)
        # logger init 
        logging.basicConfig(filename = self.conf["LOG_FILE"], level=logging.INFO, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S')
        # config timeout setting, for timeout error 
        self.req_timeout_1 = self.conf["TIMEOUT_1ST_RND"]
        self.req_timeout_2 = self.conf["TIMEOUT_2ND_RND"]
        # read symbols list from db connector
        self.symbols = self.db_conn.symbols
        print("{} symbols read.".format(len(self.symbols)))

        # lists containing error symbols and expiries
        self.RDEAllExpirLst = []    # list of strings, cannot retrieve expiries for this symbol
        self.TimeoutLst1 = []       # list of tuples, sym and expir
        self.TimeoutLst2 = []
        self.RDELst1 = []           # list of tuples, sym and expir
        self.RDELst2 = []

        self.db_conn.connect()
    
    def __del__(self):
        self.db_conn.disconnect()

    def _process_one(self, sym, expir, time_out=None):
        """
        process one symbol, one expiry date, one strike
        time_out: maximum seconds waiting for the request
        """
        if time_out == None:
            time_out = self.req_timeout_1   # the default timeout length

        tmpOption = Options(sym, 'yahoo')

        logging.info("{} - {}: Requesting".format(sym, expir))
        # set timeout for single request
        mydata = tmpOption.get_options_data(expiry = expir)
            
        logging.info("{} - {}: Finished request, insert to table...".format(sym, expir))
        
        # ===========================================
        # save to database use another object
        # ===========================================
        try:
            rowcnt = self.db_conn.save_to_db(sym, mydata)     
        except Exception as err:
            # exception while inserting to database
            print("Exception occured while inserting to database")
            # print(insert_str)
            # print(mydata.iloc[[i]])
            logging.error("Exception occured while inserting to database")
            # logging.error(insert_str)
            # logging.error(mydata.iloc[[i]])
            raise
        # ===========================================
        # ===========================================

        logging.info("{} - {}: Inserted to table, {} rows affected.".format(sym, expir, rowcnt))
        print("{} - {}: Inserted to table, {} rows affected.".format(sym, expir, rowcnt))
        rowcnt = 0

    def process_all(self):
        for sym in self.symbols:
            print(sym)
            tmpOptionObj = Options(sym, 'yahoo')
            try:
                tmpExpirList = tmpOptionObj.expiry_dates
            except pandas_datareader.data.RemoteDataError:
                self.RDEAllExpirLst.append(sym)   # cannot retrive expiry of this symbol
                print("{} - {}: RemoteDataError for all expiries".format(sym, "AllExpir"))
                logging.error("{} - {}: RemoteDataError for all expiries".format(sym, "AllExpir"))
                # skip requesting for this symbol under such error  
                continue        
            except:
                exc_type, exc_value, exc_traceback = sys.exc_info()
                # TODO:
                pass

            for expir in tmpExpirList:
                with timeout(seconds = self.req_timeout_1):
                    try:
                        self._process_one(sym, expir) 
                    # except pandas_datareader.data.RemoteDataError:
                        # self.RDELst1.append((sym, expir))
                    except TimeoutError as err:
                        self.TimeoutLst1.append((sym, expir))
                    except requests.exceptions.ConnectionError:
                        print("test error type")
                    except:
                        print("Unknown Error!")
                        exc_type, exc_value, exc_traceback = sys.exc_info()
                        self.email_sender.set_error(sym, expir, "unknown strike", str(exc_type), str(exc_value))
                        self.email_sender.send_email()
                        raise
