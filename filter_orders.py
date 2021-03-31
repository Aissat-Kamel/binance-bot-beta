from database import Signals
import numpy
import place_orders as po

def filter_order():
    data = []
    prev_data = [] # ["End_1", "BTCUSDT", "End_2", "ADAUSDT", "End_3", "End_4" , "End_5", "End_6"]
    all_lists = ["End_1", "End_2", "End_3", "End_4", "End_5", "End_6"]
    x = 0
    all_tickers = {}
    while x < 6:
        x = 0
        data = Signals.find_all(collection = "Signals") # [{"End_1":0}, {"BTCUSDT":66548654}, {"End_2":0}, {"ADAUSDT":6546548}, {"End_3":0}, {"End_4":0}, {"End_5":0}, {"End_6":0}]
        tickers = list(data.keys()) # ["End_1", "BTCUSDT", "End_2", "ADAUSDT", "End_3", "End_4" , "End_5", "End_6"]
        if tickers != prev_data:
            for ticker in tickers:
                if ticker not in prev_data and "USDT" in ticker:
                    all_tickers[ticker] = data[ticker] #{"BTCUSDT":66548654, "ADAUSDT":6546548}
                if ticker in all_lists:
                    x = x+1 #1, 2, 3, 4, 5, 6
        prev_data = tickers

    sorted_tickers = sorted(all_tickers.items(), key = lambda x: x[1], reverse = True)
    if sorted_tickers:
        selected_ticker = sorted_tickers[0][0] #"BTCUSDT"
        pct_change = (sorted_tickers[0][1][1] * -1) # 3.5
        if selected_ticker != None and pct_change != None:
            balance = po.get_usdt_balance()
            if balance >= 20:
                print("Entry amount :", balance, "USDT")
                tkr, avgPrice, id = po.buy_market(symbol = selected_ticker, amount = balance)
                po.oco_order_sell(symbol = tkr, avg_price = avgPrice, pct_sl = pct_change)
                avg_price = round(float(avgPrice), 5)
                print("Place order for :", selected_ticker, "Entry price :", str(avg_price))
            else :
                print("Insuffiant balance!")
    else:
        print("No order placed!")
    print("---------------------------------------------------")

    Signals.clear_all(collection = "Signals")
