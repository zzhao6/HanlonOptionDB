import time         # get today's date
import smtplib      # email required
from email.mime.text import MIMEText
#from sumEmail.py import *

class HanlonEmail():
    """
    send email through Gmail server

    contains three methods of sending emails:
        1. Regular summary email
        2. Individual error email
        3. TODO: Warning Email

    usage:
        1. set msg
        2. send msg
    """

    def __init__(self, confdir):
        '''
        confdir: the config file path 
        '''
        self.config = {}
        exec(open(confdir).read(), self.config)

        self.email_from = self.config["EMAIL_FROM"]
        self.email_passwd = self.config["EMAIL_PASSWD"]
        self.email_to = self.config["EMAIL_TO"]

        self.email_temp_dir = self.config["EMAIL_TEMPLATE_DIR"]
        self.email_err_temp_dir = self.config["EMAIL_ERR_TEMP_DIR"]

        self.today_date = time.strftime("%m/%d/%Y")
        

    # def setSummaryMsg(self, summaryEmailObj):
        # summaryTemplate = open(self.email_temp_dir, 'r').read()
        # self.summary = summaryTemplate.format(\
                        # summaryEmailObj.date,\
                        # summaryEmailObj.starttime,\
                        # summaryEmailObj.endtime,\
                        # summaryEmailObj.spenttime,\
                        # summaryEmailObj.RDERoundLst,\
                        # summaryEmailObj.TimeoutLst,\
                        # summaryEmailObj.numReq,\
                        # summaryEmailObj.numComp,\
                        # summaryEmailObj.numErr,\
                        # summaryEmailObj.errLst)
        # self.msg = MIMEText(self.summary)
        # self.msg['Subject'] = "Option Data Download Summary - {}".format(self.today_date)


    # def setIdvMsg(self, title, msg_str):
        # self.msg = MIMEText(msg_str)
        # self.msg['Subject'] = "{} - {}".format(title, self.today_date)

 
