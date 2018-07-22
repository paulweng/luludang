import json
import time

import requests
import websocket


def _on_message( ws, message):
    # print(type(message)
    msg = json.loads(message)
    print(msg)


def _on_error( ws, error):
    print(error)


def _on_close( ws):
    print("### closed ###")


def _on_open(ws):
    print("### opened ###")
    t = int(1000 * time.time())

    ws.send('{"cmd":"ping","args":['+str(t)+']}')



# def connectSync(self):
_ws = websocket.WebSocketApp('wss://api.fcoin.com/v2/ws',
                                  on_message=_on_message,
                                  on_error=_on_error,
                                  on_close=_on_close)
_ws.on_open = _on_open
print('connecting...')
_ws.run_forever()




"""request public url"""
