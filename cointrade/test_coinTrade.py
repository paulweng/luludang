from unittest import TestCase
from coin_trade import *

class TestCoinTrade(TestCase):

    coinTrade = FCoinTrade(access_key='d7761296a6ed41d58ca7cbd1f9e1459a',
                           secret_key='1f996e44131f4f5198819e50c3c12225')

    def test_get_balance(self):
        print(self.coinTrade.get_balance()['usdt'])

    def test_place_order(self):
        balanceDict = self.coinTrade.get_balance()
        usdt_amount = balanceDict['eth']['available']

        array = str(usdt_amount).split(".")

        v = array[0]+'.'+array[1][0:8]
        print(v)

        print(self.coinTrade.place_order('ftusdt', 3, 'buy', 'limit', 0.214788 ))

    def test_place_order_async(self):
        print(self.coinTrade.place_order_async('ethbtc', 1, 'buy', 'limit', 0.06))

    def test_cancel_order(self):
        self.coinTrade.cancel_order(7173114288)

    def test_get_order(self):
        print(str(self.coinTrade.get_order('Z8Abuk5Jz6dbswBuskdYv62aXN9qeN2nrFM50byrIas=')))

    def test_get_all_order(self):
        print(self.coinTrade.get_all_order('ftusdt'))
