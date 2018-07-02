# -*- coding:utf-8 -*-
import _thread
import json
import sys
import gzip
import threading

from coindata.model_def import Ticker
import websocket

# fcoin websocket地址
FCOIN_WS_SERVER = 'wss://api.fcoin.com/v2/ws'

# huobi websocket地址
HUOBI_WS_SERVER = "wss://api.huobi.br.com/ws"

class CoinData:

    """
    symbols : [] 交易对列表
    ticker_size : 存储的ticker数据长度
    hander : ticker推送回调函数
    """
    def __init__(self, symbols, ticker_size, handler, ws_server):
        self._symbols = symbols
        self._handler = handler
        self._ticker_size = ticker_size
        self._ws_server = ws_server
        self._ticker_dict = {}

    def _on_message(self, ws, message):
        # print(type(message)
        msg = json.loads(message)

        if 'type' in msg:
            if msg['type'] == 'hello':
                print('welcome：', message)
            elif msg['type'].startswith('ticker'):
                # print('ticker数据：', message)

                symbol = msg['type'][7:]
                last_price = msg['ticker'][0]
                last_volume = msg['ticker'][1]
                bid_price = msg['ticker'][2]
                bid_volume = msg['ticker'][3]
                ask_price = msg['ticker'][4]
                ask_volume = msg['ticker'][5]

                ticker = Ticker(symbol, last_price, last_volume, bid_price, bid_volume, ask_price, ask_volume)

                self._handle_tick(ticker)

    # 处理tick数据
    def _handle_tick(self, ticker):

        if ticker.get_symbol() in self._ticker_dict:

            ticker_list = self._ticker_dict[ticker.get_symbol()]

            if len(ticker_list) < self._ticker_size:
                ticker_list.append(ticker)
            else:
                del ticker_list[0]
                ticker_list.append(ticker)
        else:
            self._ticker_dict[ticker.get_symbol()] = [ticker]

        self._handler(ticker)

    def _on_error(self, ws, error):
        print(error)

    def _on_close(self, ws):
        print("### closed ###")

    def _on_open(self, ws):
        print("### opened ###")

        for symbol in self._symbols:
            print('{"cmd":"sub","args":["ticker.' + symbol + '"],"id":"zjf"}')
            ws.send('{"cmd":"sub","args":["ticker.' + symbol + '"],"id":"zjf"}')

    def _run(self):
        self._ws.run_forever()

    def connect(self):
        self._ws = websocket.WebSocketApp(self._ws_server,
                                           on_message=self._on_message,
                                           on_error=self._on_error,
                                           on_close=self._on_close)
        self._ws.on_open = self._on_open
        try:
            t = threading.Thread(target=self._run, args=())
            t.start()
            # t.join()
        except:
            print("Unexpected error:", sys.exc_info()[0])

    def connectSync(self):
        self._ws = websocket.WebSocketApp(self._ws_server,
                                           on_message=self._on_message,
                                           on_error=self._on_error,
                                           on_close=self._on_close)
        self._ws.on_open = self._on_open
        self._ws.run_forever()

    # 获取最新ticker
    def get_last_ticker(self, symbol):
        # print(self._ticker_dict)
        if symbol in self._ticker_dict:
            ticker_list = self._ticker_dict[symbol]
            return ticker_list[len(ticker_list) - 1]

    # 获取所有ticker
    def get_all_tickers(self, symbol):
        if symbol in self._ticker_dict:
            return self._ticker_dict[symbol]
        else:
            return []


class HuobiData(CoinData):

    __last_trade = {}

    def _on_open(self, ws):
        print("### opened ###")

        for symbol in self._symbols:

            sub = '{"sub": "market.'+symbol+'.depth.step5"}'
            print(sub)
            ws.send(sub)

            sub = '{"sub": "market.' + symbol + '.trade.detail"}'
            print(sub)
            ws.send(sub)



    def _on_message(self, ws, message):
        msg = json.loads(gzip.decompress(message))

        if 'ping' in msg:
            print(msg)
            ws.send("{'pong':'+msg['ping']+'}")

        elif 'ch' in msg:
            ch = msg['ch']
            ch_list = ch.split('.')

            symbol = ch_list[1]
            if (ch_list[2] == 'depth') and (symbol in self.__last_trade):
                # 解析
                data = msg['tick']
                last_trade = self.__last_trade[symbol]

                ticker = Ticker(symbol, last_trade['price'],
                                last_trade['amount'], data['bids'][0][0], data['bids'][0][1],
                                data['asks'][0][0], data['asks'][0][1], data['bids'], data['asks'])

                self._handle_tick(ticker)

            elif ch_list[2] == 'trade':
                # 解析
                data = msg['tick']['data']
                last_trade = data[len(data)-1]
                self.__last_trade[symbol] = last_trade

