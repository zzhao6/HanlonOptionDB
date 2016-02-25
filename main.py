from option_downloader import *
if __name__ == "__main__":
    # vix = Options('^VIX', 'yahoo')
    # vix.expiry_dates
    # dates = vix.expiry_dates
    # downloader = option_downloader()
    # downloader._process_one('^VIX', dates[1])

    downloader = option_downloader()
    downloader.download_opt_data()
