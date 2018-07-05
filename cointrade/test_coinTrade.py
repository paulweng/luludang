from unittest import TestCase
from cointrade.coin_trade import *

class TestCoinTrade(TestCase):

    coinTrade = HuobiTrade(access_key='0d15d760-6e29b03f-9244bf47-d1e0b',
                           secret_key='ffbe2844-e65a752c-3c80cd9c-fc3f1')

    def test_get_balance(self):
        print(self.coinTrade.get_balance()['usdt'])

    def test_place_order(self):
        print(self.coinTrade.place_order('btcusdt', 0.001, 'buy', 'limit', 0.06))

    def test_place_order_async(self):
        print(self.coinTrade.place_order_async('ethbtc', 1, 'buy', 'limit', 0.06))

    def test_cancel_order(self):
        self.coinTrade.cancel_order(7173114288)

    def test_get_order(self):
        print(self.coinTrade.get_order(7173114288))

    def test_get_all_order(self):
        print(self.coinTrade.get_all_order(symbol='btcusdt'))
