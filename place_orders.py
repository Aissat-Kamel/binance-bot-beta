from binance_client import client
import math
from database import Orders


def precision(symbol):
    info = client.get_symbol_info(symbol)
    precision_qty = float(info["filters"][2]['stepSize']) #0.00100000 = 3
    precision_qty = round(-math.log(precision_qty, 10), 0) #3.0
    precision_qty = int(precision_qty) #3
    precision_price = float(info["filters"][0]['minPrice']) #0.000100000 = 4
    precision_price = round(-math.log(precision_price, 10), 0) #4.0
    precision_price = int(precision_price) #4
    return precision_qty, precision_price

def get_usdt_balance():
    balance = client.get_asset_balance(asset = "USDT")
    free_balance = float(balance["free"])
    free_balance = round(free_balance * 0.1, 2)   # 100 ---- 100*0.1 = 10
    return free_balance

def get_balance(symbol):
    asset = symbol.replace("USDT", "") # "BNBUSDT" --- "BNB"
    balance = client.get_asset_balance(asset = asset)
    free_balance = float(balance["free"])
    prec_qty, prec_prc = precision(symbol = symbol)
    free_balance = round(free_balance, prec_qty)
    return free_balance

def quantity(symbol, amount):
    prec_qty, prec_prc = precision(symbol = symbol)
    avg_price = client.get_avg_price(symbol = symbol)
    avg_price = float(avg_price["price"])
    quantity = (amount / avg_price)
    quantity = round(quantity, prec_qty)
    return quantity


def buy_market(symbol, amount):
    ticker = symbol
    qty = quantity(symbol = ticker, amount = amount)
    detail = client.order_market_buy(symbol = ticker, quantity = qty)
    avg_price_buy = float(detail['cummulativeQuoteQty']) / float(detail['origQty'])
    #save order in database
    detail = Orders.save_buy_order(collection = "Buy_orders", symbol = detail["symbol"],
                                    orderId = detail["orderId"], origQty = detail["origQty"],
                                    cummulativeQuoteQty = detail["cummulativeQuoteQty"], avgPrice = avg_price_buy)
    return ticker, avg_price_buy, detail


def risk_calculator(symbol, avg_price, pct_sl):
    prec_qty, prec_prc = precision(symbol = symbol)
    prec = "%."+str(prec_prc)+"f" # "%.xf"
    sl_price = avg_price - ((avg_price * pct_sl)/100) # 97usdt
    sl_price = prec % sl_price
    trigger_sl = avg_price - ((avg_price * (pct_sl - 0.05))/100) # 97.25usdt
    trigger_sl = prec % trigger_sl
    tp_price = avg_price + ((avg_price * (pct_sl * 2))/100) # 106
    tp_price = prec % tp_price

    return str(tp_price), str(trigger_sl), str(sl_price)

def oco_order_sell(symbol, avg_price, pct_sl):
    quantity = get_balance(symbol = symbol)
    tp, trigger, sl = risk_calculator(symbol = symbol, avg_price = avg_price, pct_sl = pct_sl)
    detail = client.create_oco_order( symbol = symbol, side = "SELL",
                            stopLimitTimeInForce = "GTC",
                            quantity = quantity,
                            stopPrice = trigger,
                            stopLimitPrice  = sl,
                            price = tp )
    # save order in database
    detail = Orders.save_oco_order(collection = "OCO_orders", symbol = detail["orderReports"][0]["symbol"] ,
                                    orderId = detail["orderReports"][0]["orderId"],
                                    origQty = detail["orderReports"][0]["origQty"],
                                    take_profit = tp, stop_limit = sl, trigger_price = trigger)
    return detail
