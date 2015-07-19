import time
import smtplib
from email.mime.text import MIMEText

class HanlonEmail():
    """
    send email through stevens server
    this class object is a member of HanlonDownloader
    two steps to use this class:
    1. setMsg()
    2. sendMsg()
   
    or just
    1. sendInvidErr()
    """

    def __init__(self):
        self.today_date = time.strftime("%m/%d/%Y")
        self.template_dir = "../SummaryTemplate.txt"

    def sendIndivErr(self):
        pass

    
    def setRegMsg(self, startTime, endTime, totalSym, compSym, errSym):

        try:
            templatefile = open(self.template_dir, 'r')
        except err as Exception:
            raise

        self.summary = summaryTemplate.format(self.today_date, startTime, endTime, "", 
                                              totalSym, compSym, errSym)
        self.msg = MIMEText(self.summary)
        self.msg['Subject'] = "Option Data Download Summary - {}".format(self.today_date)
        self.msg['From'] = "hanlonoptiondb@gmail.com"
        self.msg['To'] = "hanlonoptiondb@gmail.com"

    def sendMsg(self):

        self.s = smtplib.SMTP('smtp.gmail.com', port = 587)
         
        self.s.ehlo()
        self.s.starttls()
        self.s.ehlo
        try:
            tmpstr = self.s.login(user = 'hanlonoptiondb', password = "FErules2015!")
            print(tmpstr)
        except Exception as err:
            print(err)
            raise

        self.s.send_message(self.msg)
        self.s.quit()


    def regSend(self):
        pass

    def wrnSend(self):
        pass

    def errSend(self):
        pass

    def saveToLog():
        pass

