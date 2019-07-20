from flask import Flask
from flask import jsonify
import random

from publisher import Publisher
from config import cfg

app = Flask(__name__)


@app.route('/trades/<symbol>/<qty>/<side>', methods=['POST'])
def new_trade(symbol, qty, side):
    trade = dict()
    trade['symbol'] = symbol
    trade['qty'] = qty
    trade['side'] = side

    trade_id = emit_trade(trade)

    return jsonify({'trade_id': trade_id}), 201


def emit_trade(trade):
    pub = Publisher(cfg)
    pub.publish(trade)
    return random.randint(100001, 999999)