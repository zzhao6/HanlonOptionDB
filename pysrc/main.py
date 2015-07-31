from HanlonDownloader import *

if __name__ == "__main__":
    
    ins = HanlonDownloader("../configure.conf")
    ins.OpenConn()
    ins.ProcessAll()
    ins.CloseConn()
