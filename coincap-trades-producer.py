# Databricks notebook source
# MAGIC %md
# MAGIC 
# MAGIC # use websocket-client-py3
# MAGIC 
# MAGIC https://pypi.org/project/websocket-client-py3/

# COMMAND ----------

import websocket
import json
from kafka import KafkaProducer

kafka_brokers = "b-1.detrainingmsk.66lq6h.c10.kafka.us-east-1.amazonaws.com:9092"
producer = KafkaProducer(bootstrap_servers=kafka_brokers, api_version=(2, 8, 1))

topic = 'coin_data'

def on_open(ws):
    print('Connection opened')
    # Subscribe to the Bitcoin/USD trading pair
    ws.send(json.dumps({
        "type": "subscribe",
        "exchange": "Coinbase",
        "market": "BTC/USD",
        "channel": "trades"
    }).encode('utf-8'))
    print('Connection initialized')


def on_message(ws, message):
    data = json.loads(message)
    #print(type(data))
    #print(data)
    #print(type(message))
    print(message)
 #  
#     base = data['base']
#     if base == 'bitcoin' or base == 'ethereum':
#         producer.send(topic, value=message.encode('utf-8'))
    producer.send(topic, value=message.encode('utf-8'))

def on_error(ws, error):
    print("Error: {}".format(error))

def on_close(ws):
    print("WebSocket closed")


# trade: "wss://ws.coincap.io/trades/binance"
# price: wss://ws.coincap.io/prices?assets=bitcoin,ethereum,monero,litecoin,  wss://ws.coincap.io/prices?assets=ALL
trade_wss = 'wss://ws.coincap.io/trades/binance'
#price_wss = 'wss://ws.coincap.io/prices?assets=bitcoin'

ws = websocket.WebSocketApp(
    trade_wss,
    on_open=on_open,
    on_message=on_message,
    on_close=on_close,
    on_error=on_error
)
ws.run_forever()


# COMMAND ----------

# MAGIC %md
# MAGIC #END
