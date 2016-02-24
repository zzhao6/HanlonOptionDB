import getpass
import time
import smtplib
from email.mime.text import MIMEText

class email_sender:
    """
    Send emails to a preset email account. Used as a monitor of this downloader.
    Provided methods:
        set_regular()
        set_summary()
        set_error()
        send_email()
    
    Usage:
        First use the set methods to set different kind of messages
        Then send the email by function send_email()
    """
    def __init__(self, conf):
        self.config = conf 
        self.email_from = self.config["EMAIL_FROM"]
        self.email_to = self.config["EMAIL_TO"]
        self.email_passwd = self.config["EMAIL_PASSWD"]
        # self.email_passwd = getpass.getpass("Please enter password for email address: {}: ".format(self.email_from))

        self.email_temp_dir = self.config["EMAIL_TEMPLATE_DIR"]
        self.email_err_temp_dir = self.config["EMAIL_ERR_TEMP_DIR"]
    
        self.today_date = time.strftime("%m/%d/%Y")

    def send_email(self):
        self.msg['From'] = self.email_from
        self.msg['To'] = self.email_to

        self.s = smtplib.SMTP('smtp.gmail.com', port = 587)
         
        self.s.ehlo()
        self.s.starttls()
        self.s.ehlo
        
        tmpstr = self.s.login(user = self.email_from, password = self.email_passwd)
        print(tmpstr)
        
        self.s.send_message(self.msg)
        self.s.quit()

    def set_regular(self, title, msg_str):
        self.msg = MIMEText(msg_str)
        self.msg['Subject'] = "{} - {}".format(title, self.today_date)

    def set_summary(self, summaryEmailObj):
        summaryTemplate = open(self.email_temp_dir, 'r').read()
        self.summary = summaryTemplate.format(\
                self.today_date,\
                summaryEmailObj.starttime,\
                summaryEmailObj.endtime,\
                summaryEmailObj.spenttime,\
                
                summaryEmailObj.RDE1st,\
                summaryEmailObj.RDE2nd,\
                summaryEmailObj.Timeout1st,\
                summaryEmailObj.Timeout2nd,\

                summaryEmailObj.RDELst,\
                summaryEmailObj.TimeoutLst,\
                
                summaryEmailObj.numReq,\
                summaryEmailObj.numComp,\
                summaryEmailObj.numError)
                
        self.msg = MIMEText(self.summary)
        self.msg['Subject'] = "Option Data Download Summary - {}".format(self.today_date)

    def set_error(self, sym, expir, strike, err_type, err_msg):
        errTemplate = open(self.email_err_temp_dir, 'r').read()
        self.errEmail = errTemplate.format(self.today_date, "time", sym, expir, strike, err_type, err_msg)
        
        self.msg = MIMEText(self.errEmail)
        self.msg['Subject'] = "Error Occured - Option Data Download"
    
class SummaryEmailStruct():
    def __init__(self):
        self.starttime = None
        self.endtime = None
        self.spenttime = None

        self.RDE1st = None      # number of RDE symbols
        self.RDE2nd = None 
        self.Timeout1st = None  # number of Timeout symbols
        self.Timeout2nd = None

        self.RDELst = []        # RDE symbol list
        self.TimeoutLst = []    # Timeout symbol list
        
        self.numReq = None
        self.numComp = None
        self.numError = None
