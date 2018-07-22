# -*- coding:utf-8 -*-

import sys
sys.path.append(r"../coindata")
sys.path.append(r"../cointrade")

from coin_data import *
from coin_trade import *
import time
import logging


logger = logging.getLogger("test")
logger.setLevel(logging.DEBUG)

#输出到屏幕
ch = logging.StreamHandler()
ch.setLevel(logging.WARNING)
#输出到文件
fh = logging.FileHandler("mylog.log")
fh.setLevel(logging.INFO)
#设置日志格式
fomatter = logging.Formatter('%(asctime)s -%(name)s-%(levelname)s-%(module)s:%(message)s')
ch.setFormatter(fomatter)
fh.setFormatter(fomatter)
logger.addHandler(ch)
logger.addHandler(fh)

# 超过1的次数
over_base = 0

BALANCEDICT = {}

fee = 0

amountLimit = {
    'ethusdt': 0.0001,
    'ftusdt' : 0.01,
    'fteth' : 0.01
}

basket = [
    {'symbols': ['ethusdt', 'ftusdt', 'fteth'],
     'trading': False
     }
]

coinTrade = FCoinTrade(access_key='d7761296a6ed41d58ca7cbd1f9e1459a',
                           secret_key='1f996e44131f4f5198819e50c3c12225')


BALANCEDICT = coinTrade.get_balance()

logger.info("start success. usdt begin at {}".format(BALANCEDICT['usdt']['available']))

# 订阅处理
def ticker_handler(ticker):

     # print(ticker, ticker.get_last_price())
     global over_base
     for item in range(len(basket)):
         obj = basket[item]
         symbols = obj['symbols']
         if ticker.get_symbol() == symbols[0]:
             v1 = coinData.get_last_ticker(symbols[0])
             v2 = coinData.get_last_ticker(symbols[1])
             v3 = coinData.get_last_ticker(symbols[2])

             usdt_avail = BALANCEDICT['usdt']['available']

             if v1 != None and v2 != None and v3 != None:

                 v = v2.get_bid_price() / v1.get_ask_price() / v3.get_ask_price()

                 logger.info("concurrent sign is {}".format(v))

                 if v > 1.0:
                     over_base += 1
                 else :
                     over_base = 0

                 if v > 1 and over_base == 2 and usdt_avail > 100\
                         and not obj['trading']:

                     logger.warning("find sign, v : {}, usdt_avail : {}".format(v, usdt_avail))
                     # 第二步判断成交量够不够

                     amount1 = usdt_avail / v1.get_ask_price()
                     amount3 = amount1 / v3.get_ask_price()
                     amount2 = amount3 * v2.get_bid_price()

                     logger.warning("hope price is {}:{},{}:{},{}:{}".format(
                         symbols[0],v1.get_ask_price(),symbols[2], v3.get_ask_price(), symbols[1], v2.get_bid_price()))

                     logger.warning("amount required,{}:{:.4f}, {}:{:.4f}, {}:{:.4f}".
                                 format(symbols[0],amount1,symbols[2], amount3, symbols[1], amount2))

                     if amount1 > v1.get_ask_volume() and amount2 > v2.get_bid_volume() \
                         and amount3 > v3.get_ask_volume():

                         logger.warning("amount enough!!,begin trading.")
                         # 下交易指定
                         obj['trading'] = True
                         threading.Thread(target=doTrade, args=(item,)).start()

def holdFilled (order_id) :
    time.sleep(0.01)
    count = 0
    while True:

        count += 1

        if count > 10:
            logger.error("unfilled over 10,stop!!!!")
            return [False, None]

        order = coinTrade.get_order(order_id)

        if order['state'] == 'filled':
            return [True, order]
        else:
            time.sleep(0.1)

def doTrade(index) :
    # print("begin trade")
    obj = basket[index]
    global BALANCEDICT
    # 1. 以市价单交易 ethusdt
    usdt_amount = BALANCEDICT['usdt']['available']
    eth_amount = BALANCEDICT['eth']['available']
    ft_amount = BALANCEDICT['ft']['available']

    logger.info("buy ethusdt, amount : {}".format(usdt_amount))

    orderResult = coinTrade.place_order('ethusdt',getAvailableAmount(usdt_amount,2), "buy", "market", 0)

    logger.info("orderResult:{}".format(orderResult))

    order_id = orderResult['order_id']

    # 2. 查询是否成交
    r = holdFilled(order_id)

    if r[0] == False:
        return
    else:
        logger.info("filled order result:{}".format(str(r[1])))
    # 3. 更新资产

    # 4. 买入fteth

    eth_amount = eth_amount + r[1]['field_amount'] - r[1]['fill_fees']

    logger.info("buy fteth, amount : {}".format(eth_amount))

    orderResult = coinTrade.place_order('fteth', getAvailableAmount(eth_amount,8), "buy", "market", 0)

    logger.info("orderResult:{}".format(orderResult))

    order_id = orderResult['order_id']

    # 5. 查询是否成交
    r = holdFilled(order_id)

    if r[0] == False:
        return
    else:
        logger.info("filled order result:{}".format(str(r[1])))

    # 6. 更新资产

    # 7. 卖出ft
    ft_amount = ft_amount + r[1]['field_amount'] - r[1]['fill_fees']


    logger.info("sell ftusdt, amount : {}".format(ft_amount))

    orderResult = coinTrade.place_order('ftusdt', getAvailableAmount(ft_amount,2), "sell", "market", 0)

    logger.info("orderResult:{}".format(orderResult))

    order_id = orderResult['order_id']

    # 8. 查询是否成交
    r = holdFilled(order_id)

    if r[0] == False:
        return
    else:
        logger.info("filled order result:{}".format(str(r[1])))

    BALANCEDICT = coinTrade.get_balance()
    usdt_amount = BALANCEDICT['usdt']['available']
    logger.info("this trading is completed. usdt left:{}".format(usdt_amount))

    obj['trading'] = False


    # print(ticker.symbol, 20, ticker.last_price)
    # print(ticker)

def getAvailableAmount(amount, number):
    array = str(amount).split(".")

    if (number < len(array[1])):
        v = array[0] + '.' + array[1][0:number]
    else:
        return amount

    return v


subList = []

for obj in basket:
    for subObj in obj['symbols']:
        subList.append(subObj)


coinData = CoinData(subList, 20, ticker_handler, FCOIN_WS_SERVER)
coinData.connectSync()
