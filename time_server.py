from binance_client import client
import time
import pandas as pd
import threading
import tickers as tkr
import engulfing_2_ema_stgy as stgy
import filter_orders as fo

interval = [0, 15, 30, 45]


def server_tm():
    time_srv = client.get_server_time()
    time = pd.to_datetime(time_srv["serverTime"], unit = "ms")
    min_ = time.strftime("%M")
    min_ = int(min_)
    sec_ = time.strftime("%S")
    sec_ = int(sec_)
    for i in interval:
        if min_ == i and sec_ == 3:
            print("Searching for opportunities ...")
            # run strategy
            threading.Thread(target = stgy.engulfing_strgy, args = (tkr.list_1, 1)).start()
            threading.Thread(target = stgy.engulfing_strgy, args = (tkr.list_2, 2)).start()
            threading.Thread(target = stgy.engulfing_strgy, args = (tkr.list_3, 3)).start()
            threading.Thread(target = stgy.engulfing_strgy, args = (tkr.list_4, 4)).start()
            threading.Thread(target = stgy.engulfing_strgy, args = (tkr.list_5, 5)).start()
            threading.Thread(target = stgy.engulfing_strgy, args = (tkr.list_6, 6)).start()
            threading.Thread(target = fo.filter_order).start()
            time.sleep(5)
