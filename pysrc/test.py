from HanlonDownloader import *

if __name__ == "__main__":
    ctsh = Options('CTSH', 'yahoo')

    ins = HanlonDownloader("../configure.conf")
    ins.OpenConn()
    ins._ProcessOne('CTSH', ctsh.expiry_dates[8])
    ins.CloseConn()
