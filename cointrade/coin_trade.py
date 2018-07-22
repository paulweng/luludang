# -*- coding:utf-8 -*-

import base64
import datetime
import hashlib
import hmac
import json
import threading
import time
import urllib
import urllib.parse
import urllib.request
import requests

import logging


logger = logging.getLogger("trade")
logger.setLevel(logging.DEBUG)

#输出到屏幕
ch = logging.StreamHandler()
ch.setLevel(logging.WARNING)
#输出到文件
fh = logging.FileHandler("trade_error.log")
fh.setLevel(logging.INFO)
#设置日志格式
fomatter = logging.Formatter('%(asctime)s -%(name)s-%(levelname)s-%(module)s:%(message)s')
ch.setFormatter(fomatter)
fh.setFormatter(fomatter)
logger.addHandler(ch)
logger.addHandler(fh)

# TRADE_URL = "https://api.huobi.pro"
HUOBI_TRADE_URL = "https://api.huobi.br.com"

# fcoin 配置
FCOIN_SERVER = 'api.fcoin.com'
PORT = 80
HT = 'https://%s/v2/'
HTMRK = 'https://%s/v2/market/'
HTPBL = 'https://%s/v2/public/'
HTORD = 'https://%s/v2/orders/'
HTACT = 'https://%s/v2/accounts/'
WS = 'wss://%S/v2/ws/'

ST = 'server-time'
SYMBOLS = 'symbols'
CURRENCY = 'currencies'
TICKER = 'ticker/%s'

POST = 'POST'
GET = 'GET'

KDATA = 'candles/%s/%s'
KDATA_COLUMNS = ['id', 'open', 'high', 'low', 'close', 'count', 'base_vol', 'quote_vol', 'seq']
KDATA_REAL_COL = ['datetime', 'open', 'high', 'low', 'close', 'count', 'base_vol', 'quote_vol', 'seq']

# 已提交
STATE_SUBMITTED = 'submitted'
# 部分成交
STATE_PARTIAL_FILLED = 'partial_filled'
# 部分成交撤销
STATE_PARTIAL_CANCELED = 'partial_canceled'
# 完全成交
STATE_FILLED = 'filled'
# 已撤销
STATE_CANCELED = 'canceled'

ALL_STATES = 'submitted,partial_filled,canceled,filled,partial_canceled'


class CoinTrade:

    def __init__(self, access_key='', secret_key=''):
        self._access_key = access_key
        self._secret_key = secret_key
        self._account_id = self._get_account()


    def _get_account(self):
        '''
        获取账号信息

        :return:
        '''
        return ''

    def get_balance(self):
        '''
        获取可用余额

        :return: {'$symbol$':{'available':10.0,'frozen':0.0,'balance':10.0}}
        '''
        pass

    def place_order(self, symbol, amount, side, _type, price):
        '''
        下单

        :param symbol: 交易对
        :param amount: 委托数量
        :param side: 买卖方向 buy / sell
        :param _type: 类型 market / limit / ioc (火币专用)
        :param price: 委托价格
        :return:

         {
            'status' : '', // 执行结果 ok: 成功 error:失败

            'error_code' : '', // 错误代码

            'error_msg' : '',// 错误描述

            'order_id' : ''
        }
        '''

        pass

    def place_order_async(self, symbol, amount, side, _type, price):
        '''
        异步下单

        :param symbol: 交易对
        :param amount: 委托数量
        :param side: 买卖方向 buy / sell
        :param _type: 类型 market / limit / ioc (火币专用)
        :param price: 委托价格
        :return:



        '''

        pass

    def cancel_order(self, order_id):
        '''
        撤单

        :param order_id: 订单编号
        :return:
        '''
        pass

    def get_order(self, order_id):
        '''
        获取指定订单

        :param order_id: 订单编号
        :return:

        {
            "id": 59378, // 订单编号

            "symbol": "ethusdt", // 交易对

            "amount": "10.1000000000", //委托数量

            "price": "100.1000000000", // 委托价格

            "created_at": 1494901162595, // 创建时间

            "type": "limit", // 订单类型

            "side": "buy", // 买卖方向

            "field_amount": "10.1000000000", // 成交量

            "executed_value": "1011.0100000000", // 成交金额

            "fill_fees": "0.0202000000", // 手续费

            "finished_at": 1494901400468, // 成交时间 火币专属

            "state": "filled", // 订单状态， submitted - 已提交，partial_filled - 部分成交，partial_canceled - 部分撤单， filled - 全部成交，canceled - 已撤单，pending_cancel - 撤单已提交

            "canceled-at": 0 // 撤单时间 火币专属
        }

        '''

        pass

    def get_all_order(self, symbol=None, states=None):
        '''
        查询所有订单

        :param symbol: 交易对
        :param states: 状态，多个以逗号分隔
        :param order_id: 订单编号
        :return:

        {
            "id": 59378, // 订单编号

            "symbol": "ethusdt", // 交易对

            "amount": "10.1000000000", //委托数量

            "price": "100.1000000000", // 委托价格

            "created_at": 1494901162595, // 创建时间

            "type": "limit", // 订单类型

            "side": "buy", // 买卖方向

            "field_amount": "10.1000000000", // 成交量

            "executed_value": "1011.0100000000", // 成交金额

            "fill_fees": "0.0202000000", // 手续费

            "finished_at": 1494901400468, // 成交时间 火币专属

            "state": "filled", // 订单状态， submitted - 已提交，partial_filled - 部分成交，partial_canceled - 部分撤单， filled - 全部成交，canceled - 已撤单，pending_cancel - 撤单已提交

            "canceled-at": 0 // 撤单时间 火币专属
        }

        '''

        pass


'''
acct_id = '3984817'

url = "/v1/account/accounts/{0}/balance".format(acct_id)
params = {"account-id": acct_id}
print(api_key_get(params, url))

'''

class HuobiTrade(CoinTrade):

    def _get_account(self):
        path = "/v1/account/accounts"
        params = {}
        accounts = self._api_key_get(params, path)
        account_id = accounts['data'][0]['id']
        return account_id

    def get_balance(self):
        path = "/v1/account/accounts/{0}/balance".format(self._account_id)
        params = {}
        result = self._api_key_get(params, path)
        balanceDict = {}

        for balance in result['data']['list']:

            symbol = balance['currency']

            if symbol not in balanceDict:
                balanceDict[symbol] = {}

            if balance['type'] == 'trade':

                balanceDict[symbol]['available'] = float(balance['balance'])

            elif balance['type'] == 'frozen':

                balanceDict[symbol]['frozen'] = float(balance['balance'])

            if ('available' in balanceDict[symbol]) \
                    and ('frozen' in balanceDict[symbol]):

                balanceDict[symbol]['balance'] = balanceDict[symbol]['available'] + balanceDict[symbol]['frozen']


        return balanceDict

    def place_order(self, symbol, amount, side, _type, price):

        path = "/v1/order/orders/place"
        params = {
            'account-id': self._account_id,
            'amount': amount,
            'price': price,
            'symbol': symbol,
            'type': side + '-' + _type,
        }

        result = self._api_key_post(params, path)

        cresult = {}

        cresult['status'] = result['status']
        if 'err-code' in result:
            cresult['err_code'] = result['err-code']

        if 'err-msg' in result:
            cresult['err_msg'] = result['err-msg']

        cresult['order_id'] = result['data']

        return cresult


    def place_order_async (self, symbol, amount, side, _type, price):

        t = threading.Thread(target=self.place_order,
                             args=(symbol, amount, side, _type, price))
        t.start()

    def cancel_order(self, order_id):

        path = "/v1/order/orders/{0}/submitcancel".format(order_id)

        return self._api_key_post({}, path)


    def get_order(self, order_id):

        path = "/v1/order/orders/{0}".format(order_id)

        result = self._api_key_get({}, path)

        if result['status'] != 'ok':
            print(result)
        else:
            obj = result['data']

            return {
                    'id': obj['id'],
                    'symbol': obj['symbol'],
                    'amount': float(obj['amount']),
                    'price': float(obj['price']),
                    'type': obj['type'].split("-")[1],
                    'side': obj['type'].split("-")[0],
                    'created_at': obj['created-at'],
                    'field_amount': float(obj['field-amount']),
                    'executed_value': float(obj['field-cash-amount']),
                    'fill_fees': float(obj['field-fees']),
                    'finished_at': obj['finished-at'],
                    'state': obj['state'].replace("-", "_"),
                    'canceled_at': obj['canceled-at']

                }



    def get_all_order(self, symbol = None, states = ALL_STATES):

        path = "/v1/order/orders"
        params = {}

        if symbol is not None:
            params['symbol'] = symbol

        if states is not None:
            states = states.replace("_", "-")
            params['states'] = states

        result = self._api_key_get(params, path)

        if result['status'] != 'ok':
            print(result)
        else:
            list = []

            for obj in result['data']:
                list.append({
                    'id': obj['id'],
                    'symbol': obj['symbol'],
                    'amount': float(obj['amount']),
                    'price': float(obj['price']),
                    'type': obj['type'].split("-")[1],
                    'side': obj['type'].split("-")[0],
                    'created_at': obj['created-at'],
                    'field_amount': float(obj['field-amount']),
                    'executed_value': float(obj['field-cash-amount']),
                    'fill_fees': float(obj['field-fees']),
                    'finished_at': obj['finished-at'],
                    'state': obj['state'].replace("-", "_"),
                    'canceled_at': obj['canceled-at']

                })

            return list



    def _api_key_get(self, params, request_path):
        method = 'GET'
        timestamp = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')
        params.update({'AccessKeyId': self._access_key,
                       'SignatureMethod': 'HmacSHA256',
                       'SignatureVersion': '2',
                       'Timestamp': timestamp})

        host_url = HUOBI_TRADE_URL
        host_name = urllib.parse.urlparse(host_url).hostname
        host_name = host_name.lower()
        params['Signature'] = self._createSign(params, method, host_name, request_path, self._secret_key)

        url = host_url + request_path
        return self._http_get_request(url, params)

    def _http_get_request(self, url, params, add_to_headers=None):
        headers = {
            "Content-type": "application/x-www-form-urlencoded",
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36',
        }
        if add_to_headers:
            headers.update(add_to_headers)
        postdata = urllib.parse.urlencode(params)
        response = requests.get(url, postdata, headers=headers, timeout=5)
        try:

            if response.status_code == 200:
                return response.json()
            else:
                return
        except BaseException as e:
            print("httpGet failed, detail is:%s,%s" % (response.text, e))
            return

    def _http_post_request(self, url, params, add_to_headers=None):
        headers = {
            "Accept": "application/json",
            'Content-Type': 'application/json'
        }
        if add_to_headers:
            headers.update(add_to_headers)
        postdata = json.dumps(params)
        response = requests.post(url, postdata, headers=headers, timeout=10)
        try:

            if response.status_code == 200:
                return response.json()
            else:
                return
        except BaseException as e:
            print("httpPost failed, detail is:%s,%s" % (response.text, e))
            return

    def _api_key_post(self, params, request_path):
        method = 'POST'
        timestamp = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')
        params_to_sign = {'AccessKeyId': self._access_key,
                          'SignatureMethod': 'HmacSHA256',
                          'SignatureVersion': '2',
                          'Timestamp': timestamp}

        host_url = HUOBI_TRADE_URL
        host_name = urllib.parse.urlparse(host_url).hostname
        host_name = host_name.lower()
        params_to_sign['Signature'] = self._createSign(params_to_sign, method, host_name, request_path, self._secret_key)
        url = host_url + request_path + '?' + urllib.parse.urlencode(params_to_sign)
        return self._http_post_request(url, params)

    def _createSign(self, pParams, method, host_url, request_path, secret_key):
        sorted_params = sorted(pParams.items(), key=lambda d: d[0], reverse=False)
        encode_params = urllib.parse.urlencode(sorted_params)
        payload = [method, host_url, request_path, encode_params]
        payload = '\n'.join(payload)
        payload = payload.encode(encoding='UTF8')
        secret_key = secret_key.encode(encoding='UTF8')

        digest = hmac.new(secret_key, payload, digestmod=hashlib.sha256).digest()
        signature = base64.b64encode(digest)
        signature = signature.decode()
        return signature


class FCoinTrade(CoinTrade):

    def _get_account(self):
        return ''

    def get_balance(self):
        result = self._signed_request(GET, HTACT%FCOIN_SERVER + 'balance')

        balanceDict = {}

        for balance in result['data']:

            symbol = balance['currency']

            if symbol not in balanceDict:
                balanceDict[symbol] = {}

                balanceDict[symbol]['available'] = float(balance['available'])

                balanceDict[symbol]['frozen'] = float(balance['frozen'])

                balanceDict[symbol]['balance'] = float(balance['balance'])


        return balanceDict

    def place_order(self, symbol, amount, side, _type, price):

        params = {
            'amount': amount,
            'price': price,
            'symbol': symbol,
            'type': _type,
            'side': side
        }


        result = self._signed_request(POST,HTORD%FCOIN_SERVER , amount=amount,price=price,symbol=symbol,type=_type,side=side)

        cresult = {}

        cresult['status'] = result['status']

        if cresult['status'] == 0:
            cresult['order_id'] = result['data']
        else:
            logger.error(result)
        return cresult


    def place_order_async (self, symbol, amount, side, _type, price):

        t = threading.Thread(target=self.place_order,
                             args=(symbol, amount, side, _type, price))
        t.start()

    def cancel_order(self, order_id):

        path = "/v1/order/orders/{0}/submitcancel".format(order_id)

        return self._api_key_post({}, path)


    def get_order(self, order_id):


        result = self._signed_request(GET, HTORD % FCOIN_SERVER+ order_id)


        if result['status'] != 0:
            logger.error(result)
        else:
            obj = result['data']

            return {
                    'id': obj['id'],
                    'symbol': obj['symbol'],
                    'amount': float(obj['amount']),
                    'price': float(obj['price']),
                    'type': obj['type'],
                    'side': obj['side'],
                    'created_at': obj['created_at'],
                    'field_amount': float(obj['filled_amount']),
                    'executed_value': float(obj['executed_value']),
                    'fill_fees': float(obj['fill_fees']),
                    'state': obj['state'].replace("-", "_")

                }



    def get_all_order(self, symbol = None, states = ALL_STATES):

        result = self._signed_request(POST, HTORD % FCOIN_SERVER)

        print(result)
        if result['status'] != 'ok':
            print(result)
        else:
            list = []

            for obj in result['data']:
                list.append({
                    'id': obj['id'],
                    'symbol': obj['symbol'],
                    'amount': float(obj['amount']),
                    'price': float(obj['price']),
                    'type': obj['type'].split("-")[1],
                    'side': obj['type'].split("-")[0],
                    'created_at': obj['created-at'],
                    'field_amount': float(obj['field-amount']),
                    'executed_value': float(obj['field-cash-amount']),
                    'fill_fees': float(obj['field-fees']),
                    'state': obj['state'].replace("-", "_")

                })

            return list

    def _signed_request(self, method, url, **params):
        param = ''
        if params:
            sort_pay = list(params.keys())
            sort_pay.sort()
            for k in sort_pay:
                param += '&' + str(k) + '=' + str(params[k])
            param = param.lstrip('&')
        timestamp = str(int(time.time() * 1000))

        if method == GET:
            if param:
                url = url + '?' + param
            sig_str = method + url + timestamp
        elif method == POST:
            sig_str = method + url + timestamp + param

        signature = self._get_signed(sig_str)

        headers = {
            'FC-ACCESS-KEY': self._access_key,
            'FC-ACCESS-SIGNATURE': signature,
            'FC-ACCESS-TIMESTAMP': timestamp

        }

        try:
            r = requests.request(method, url, headers=headers, json=params)
            r.raise_for_status()
        except requests.exceptions.HTTPError as err:
            logger.error(err)
            logger.error(r.text)
        if r.status_code == 200:
            return r.json()

    def _public_request(self, method, url, **params):
        try:
            r = requests.request(method, url, params=params)
            r.raise_for_status()
        except requests.exceptions.HTTPError as err:
            logger.error(err)
        if r.status_code == 200:
            return r.json()

    def _get_signed(self, sig_str):
        sig_str = base64.b64encode(bytes(sig_str, 'utf-8'))
        signature = base64.b64encode(hmac.new(bytes(self._secret_key,'utf-8'), sig_str, digestmod=hashlib.sha1).digest())
        return signature

