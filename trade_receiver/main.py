from flask import Flask
from flask import jsonify
import random

from common_utils import Logger
from config import cfg
from common_utils.publisher import Publisher

app = Flask(__name__)


@app.route('/')
def hello():
    return 'Hello! Welcome to Fin.!\n'


@app.route('/trades/<trader_id>/<symbol>/<qty>/<side>', methods=['POST'])
def new_trade(trader_id, symbol, qty, side):
    trade = dict()
    trade['symbol'] = symbol
    trade['qty'] = qty
    trade['side'] = side
    trade['trader_id'] = trader_id

    trade_id = emit_trade(trade)

    return jsonify({'trade_id': trade_id}), 201


def emit_trade(trade):
    pub = Publisher(cfg)
    pub.publish(trade)
    return random.randint(100001, 999999)
