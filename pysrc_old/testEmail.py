from MyEmail import *

myemail = MyEmail()
myemail.setRegMsg("Hello")
myemail.testSend()

# import smtplib
#  
# to = 'zhaozhe0122@gmail.com'
# gmail_user = 'zhaozhe0122@gmail.com'
# gmail_pwd = 'Perprince0122'
# smtpserver = smtplib.SMTP("smtp.gmail.com",587)
# smtpserver.ehlo()
# smtpserver.starttls()
# smtpserver.ehlo
# smtpserver.login(gmail_user, gmail_pwd)
# msg = "Hello!"
# smtpserver.sendmail(gmail_user, to, msg)
# smtpserver.close()
