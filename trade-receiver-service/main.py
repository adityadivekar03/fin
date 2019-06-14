from flask import Flask
from flask import jsonify
import pika
import json
import random

app = Flask(__name__)

EXCHANGE_NAME = 'trade_updates'
ROUTING_KEY = 'trade.new_trade'

@app.route('/trades/<symbol>/<qty>/<side>', methods=['POST'])
def new_trade(symbol, qty, side):
    trade = dict()
    trade['symbol'] = symbol
    trade['qty'] = qty
    trade['side'] = side

    trade_id = emit_trade(trade)

    return jsonify({'trade_id': trade_id}), 201


def emit_trade(trade):

    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq-server'))
    channel = connection.channel()

    channel.exchange_declare(exchange=EXCHANGE_NAME, exchange_type='topic', durable=True)

    channel.basic_publish(exchange=EXCHANGE_NAME,
                          routing_key=ROUTING_KEY,
                          body=json.dumps(trade),
                          properties=pika.BasicProperties(
                              delivery_mode=2,
                          ))

    print("Successfully sent the data {} to the exchange {} with the routing key {}".format(trade, EXCHANGE_NAME,
                                                                                            ROUTING_KEY))
    connection.close()
    return random.randint(100000, 999999)
