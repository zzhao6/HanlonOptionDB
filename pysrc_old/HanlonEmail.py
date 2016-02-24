import time
import smtplib
from email.mime.text import MIMEText


class HanlonEmail():
    """
    send email through Gmail server
    
    contains three methods of send emails:
        1. Regular summary email
        2. Individual error email
        3. Warning Email (TODO)

    usage:
        1. set msg (reg, err or wrn)
        2. send msg (no parameter)
    """

    def __init__(self, dnlr_config):
        # receive config obj from HanlonDownloader and init this class
        self.email_from = dnlr_config["EMAIL_FROM"]
        self.email_passwd = dnlr_config["EMAIL_PASSWD"]
        self.email_to = dnlr_config["EMAIL_TO"]

        self.email_temp_dir = dnlr_config["EMAIL_TEMPLATE_DIR"]
        self.email_err_temp_dir = dnlr_config["EMAIL_ERR_TEMP_DIR"]
    
        self.today_date = time.strftime("%m/%d/%Y")


    def setSummaryMsg(self, summaryEmailObj):
        summaryTemplate = open(self.email_temp_dir, 'r').read()
        self.summary = summaryTemplate.format(\
                summaryEmailObj.date,\
                summaryEmailObj.starttime,\
                summaryEmailObj.endtime,\
                summaryEmailObj.RDE1st,\
                summaryEmailObj.RDE2nd,\
                summaryEmailObj.Timeout1st,\
                summaryEmailObj.Timeout2nd,\

                summaryEmailObj.RDELst,\
                summaryEmailObj.TimeoutLst,\
                summaryEmailObj.numReq,\
                summaryEmailObj.numComp)
                
        self.msg = MIMEText(self.summary)
        self.msg['Subject'] = "Option Data Download Summary - {}".format(self.today_date)
        # end set message
        # next step is send out the email
    

    def setIdvMsg(self, title, msg_str):
        self.msg = MIMEText(msg_str)
        self.msg['Subject'] = "{} - {}".format(title, self.today_date)


    def setErrMsg(self, sym, expir, strike, err_type, err):
        errTemplate = open(self.email_err_temp_dir, 'r').read()
        self.errEmail = errTemplate.format(self.today_date, "time", sym, expir, strike, err_type, err)
        
        self.msg = MIMEText(self.errEmail)
        self.msg['Subject'] = "Error Occured - Option Data Download"

    def setWrnMsg(self):
        # TODO
        pass


    def sendMsg(self):
        self.msg['From'] = self.email_from
        self.msg['To'] = self.email_to

        self.s = smtplib.SMTP('smtp.gmail.com', port = 587)
         
        self.s.ehlo()
        self.s.starttls()
        self.s.ehlo
        
        tmpstr = self.s.login(user = 'hanlonoptiondb', password = "FErules2015!")
        print(tmpstr)
        
        self.s.send_message(self.msg)
        self.s.quit()


class SummaryEmailStruct():
    def __init__(self)
        self.date = None
        self.starttime = None
        self.endtime = None

        self.numReq = None
        self.numComp = None
        self.numError = None

        self.RDE1st = None      # number of RDE symbols
        self.RDE2nd = None 
        self.Timeout1st = None  # number of Timeout symbols
        self.Timeout2nd = None

        self.RDELst = []        # RDE symbol list
        self.TimeoutLst = []    # Timeout symbol list

