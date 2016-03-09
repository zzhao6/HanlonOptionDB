from option_downloader import *
if __name__ == "__main__":
    # vix = Options('^VIX', 'yahoo')
    # vix.expiry_dates
    # dates = vix.expiry_dates
    # downloader = option_downloader()
    # downloader._process_one('^VIX', dates[1])

    downloader = option_downloader()
    # downloader.download_opt_data()
    rowcnt = downloader.db_conn.get_count("VIX", "2016-03-16", downloader.email_sender.today_date)
    print(rowcnt)
