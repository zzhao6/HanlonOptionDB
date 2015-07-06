import pandas as pd
import pymysql
from pandas_datareader import data, wb
from pandas_datareader.data import Options

import logging
import pickle       # save expiry dicitonary to file

import sys          # display percentage counter

class HanlonDownloader:
    """downloader class"""
    def __init__(self, symfiledir, **kwargs):
        # TODO: config file
        self.isconnected = False
        # count how many rows affected 
        self.rowcnt = 0
        self.symExpiryDict = {}
        # set up the logger
        logging.basicConfig(filename='../log/mylog.log', level=logging.INFO, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S')
        self._readSymbols(symfiledir)
        # decide whether update the expiry dates or not
        # for all equity symbols
        self._expDateFileDir = '../pysrc/expDates.txt'
        self._expir_cnt = 0.0
        self.updateExp = kwargs.get('updateExp')
        self._readExpiry(self.updateExp)

    
    def HanlonConn(self, hanlon_host, hanlon_user, hanlon_passwd, hanlon_dbname):
        try:
            self.conn = pymysql.connect(host = hanlon_host, user = hanlon_user, passwd = hanlon_passwd, db = hanlon_dbname) 
            self.host = hanlon_host
            self.user = hanlon_user
            self.passwd = hanlon_passwd
            self.dbname = hanlon_dbname
        except pymysql.err.OperationalError as err:
            print(err)
            input("Press any key to raise the exception.")
            raise
        except pymysql.err.InternalError as err:
            print(err)
            input("Press any key to raise the exception.")
            raise
        except Exception as e:
            self._printException(err) 

        self.cur = self.conn.cursor()
        self.isconnected = True
        print("Connected to database:{}".format(self.dbname))
        logging.info("Connected to database: {}".format(self.dbname))
        
    def closeConn(self):
        """some thing todo before finish all day work"""
        self.cur.close()
        self.conn.close()
        print("Connection closed")
        logging.info("Connection closed, here is the summary")

    def _readSymbols(self, filedir):
        '''
        load all symbols and create a dictionary
        {sym, expiry_dates}
        '''
        try:
            tmpfile = pd.read_csv(filedir)
        except OSError as err:
            logging.error("Error: {}".format(err))
            print("Unknown Error occured.")
            input("Press any key to raise the exception.")
            raise

        self.symbols = tmpfile.Symbol
        print("{} symbols loaded".format(len(self.symbols)))
        logging.info("{} symbols loaded, ready to request data.".format(len(self.symbols))) 


    def _readExpiry(self, updateExpiryFlag):
        # load expiry dates from a file
        # the file will be overwrote when update the expiries

        if updateExpiryFlag:
            print("Updating expiry dates for all equities.")
            for sym in self.symbols:
                symOption = Options(sym, 'yahoo')
                try:
                    tmpSymExpiry = symOption.expiry_dates
                    print("Updated {} \t number of dates: {}".format(sym, len(symExpiry)))
                except Exception as err:
                    self._printException(err)

                self.symOptionDict[sym] = symOption
                self.symExpiryDict[sym] = symExpiry
            # update the file of expiry dates
            expDateFile = open(self._expDateFileDir, 'ab+')
            pickle.dump(self.symExpiryDict, expDateFile)
        else:
            print("User chooses not to update the expiry dates.")
            logging.info("User chooses not to update the expiry dates.")

       
        # load the dict file again
        try:
            tmpfile = open(self._expDateFileDir, 'rb')
            self.symExpiryDict = pickle.load(tmpfile)
        except Exception as err:
            self._printException(err)
        logging.info("Loaded all expiry dates")
        print("Loaded all expiry dates")

        for key, value in self.symExpiryDict.items():
            print("{} \t length {}".format(key, len(value)))
            self._expir_cnt += len(value)       # for display percentage count


    def _printException(self, err):
        '''
        print and logging some messages about unhandled exception
        '''
        print("Unhandled exception. {}".format(err))
        logging.exception("Unhandled exception. {}".format(err))
        input("Press any key to raise the exception.")
        raise

    def _processOne(self, sym, exp):
        '''
        process one result of API: one symbol, one expiry
        decomposite the dataframe and push to database
        '''
        print("Requesting {}, {}.".format(sym, exp))
        logging.info("Requesting {}, {}.".format(sym, exp))
        tmpOption = Options(sym, 'yahoo')
        try:
            # TODO: handle RemoteDataError exception. Sometime the yahoo server doesn't response
            mydata = tmpOption.get_options_data(expiry = exp)
        except Exception as err:
            self._printException(err)
        # start processing
        # first reset the multiindex in pandas dataframe
        print("Finished request, insert to table...")
        logging.info("Finished request, insert to table...")
        mydata = mydata.reset_index()

        for i in range(len(mydata.index)):
            onerow = mydata.iloc[[i]]
            # gen sql insert statement
            insert_str = """INSERT INTO {} (underlying_symbol, option_symbol,
            strike, expiry, option_type, quote_date, last, bid, ask, vol,
            open_int, IV, underlying_price) VALUES 
            ('{}', '{}', {}, '{}', '{}', '{}', {}, {}, {}, {}, {}, {}, {});""".format(sym,\
                    onerow.Root[i], onerow.Symbol[i], onerow.Strike[i], \
                    str(onerow.Expiry[i].date()), onerow.Type[i], str(onerow.Quote_Time[i].date()),\
                    onerow.Last[i], onerow.Bid[i], onerow.Ask[i],\
                    onerow.Vol[i], onerow.Open_Int[i], float(onerow.IV[i].strip('%'))/100,\
                    onerow.Underlying_Price[i])
            # push into db
            # TODO: this execute will return row count
             
            # replace missing value '-' with '0'
            insert_str = insert_str.replace(" -,", " 0,")

            try:
                self.rowcnt += self.cur.execute(insert_str) 
            except Exception as err:
                self._printException(err)

            self.conn.commit()
            # end of for loop

        print("Inserted to table {}, {} rows affected.".format(sym, self.rowcnt))
        logging.info("Inserted to table {}, {} rows affected.".format(sym, self.rowcnt))
        self.rowcnt = 0

    def processAll(self):
        '''
        download all symbols and push to database
        '''
        print('---------------------')
        # TODO: put logging here
        
        tmpPercentCount = 0.0
        for sym in self.symExpiryDict.keys():
            for exp in self.symExpiryDict[sym]:
                self._processOne(sym, exp)
                tmpPercentCount += 1
                tmpPercent = tmpPercentCount / self._expir_cnt * 100
                sys.stdout.write("\r%f%%\n" % tmpPercent)
                sys.stdout.flush()
