# -*- coding:utf-8 -*-
import time

from coindata.coin_data import *

print(1)
# 订阅处理
def ticker_handler(ticker):
     pass
    # print(ticker.symbol, 20, ticker.last_price)
    # print(ticker)


coinData = CoinData(['btcusdt', 'ethusdt'], 20, ticker_handler, FCOIN_WS_SERVER)
coinData.connect()

print(111)
time.sleep(3)

print('sleep end')
# 获取最新数据
print(coinData.get_last_ticker('btcusdt').get_bid_price())
# 获取交易对最近N笔数据
print(coinData.get_all_tickers('btcusdt'))

"""
def on_message(ws, message):
    # print(type(message)
    msg = json.loads(message)

    if 'type' in msg:
        if msg['type'] == 'hello':
            print('欢迎语句：', message)
        elif msg['type'].startswith('ticker'):
            # print('ticker数据：', message)
            ticker = Ticker()
            ticker.symbol = msg['type'][7:]
            ticker.last_price = msg['ticker'][0]
            ticker.last_volume = msg['ticker'][1]
            ticker.bid_price = msg['ticker'][2]
            ticker.bid_volume = msg['ticker'][3]
            ticker.ask_price = msg['ticker'][4]
            ticker.ask_volume = msg['ticker'][5]


def on_error(ws, error):
    print(error)

def on_close(ws):
    print("### closed ###")

def on_open(ws):
    print("### opened ###")
    ws.send('{"cmd":"sub","args":["ticker.btcusdt"],"id":"zjf"}')

ws = websocket.WebSocketApp("wss://api.fcoin.com/v2/ws",
                            on_message=on_message,
                            on_error=on_error,
                            on_close=on_close)
ws.on_open = on_open
ws.run_forever()
"""