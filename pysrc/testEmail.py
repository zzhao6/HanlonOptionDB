from HanlonEmail import *


dummyconf = {}
exec(open("../configure.conf").read(), dummyconf)

myemail = HanlonEmail(dummyconf)
myemail.setRegMsg("","","","","")
myemail.sendMsg()
