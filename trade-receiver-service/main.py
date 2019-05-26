from flask import Flask
from flask import jsonify

from services.emit_trade import emit_trade

app = Flask(__name__)


@app.route('/trades/<symbol>/<qty>/<side>', methods=['POST'])
def new_trade(symbol, qty, side):
    trade = dict()
    trade['symbol'] = symbol
    trade['qty'] = qty
    trade['side'] = side

    trade_id = emit_trade(trade)

    return jsonify({'trade_id': trade_id}), 201
