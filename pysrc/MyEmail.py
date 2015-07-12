import time
import smtplib
from email.mime.text import MIMEText

class MyEmail():
    """
    send email through stevens server
    this class object is a member of HanlonDownloader
    """

    def __init__(self):
        self.today_date = time.strftime("%m/%d/%Y")

    def setMsg(self, summary):
        self.msg = MIMEText(summary)
        self.msg['Subject'] = "Sent from python by Zhe - {}".format(self.today_date)
        self.msg['From'] = "hanlonoptiondb@gmail.com"
        self.msg['To'] = "hanlonoptiondb@gmail.com"

    def testSend(self):

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

