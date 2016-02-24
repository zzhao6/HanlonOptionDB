from HanlonDownloader import *


if __name__ == "__main__":
    h = HanlonDownloader("../configure.conf")
    h.OpenConn()
    h.CloseConn()

