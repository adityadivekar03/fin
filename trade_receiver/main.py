from flask import Flask
from flask import flash, redirect, render_template, url_for
import random

from common_utils import Logger, settings
from config import cfg
from common_utils.publisher import Publisher
from forms import TradeInputForm

app = Flask(__name__)
app.config['SECRET_KEY'] = settings.SECRET_KEY


@app.route('/')
def home():
    return render_template('index.html', title='Trade Receiver')


@app.route('/new_trade', methods=['GET', 'POST'])
def new_trade():
    print('new trade')
    form = TradeInputForm()
    if form.validate_on_submit():
        print('form validated')
        trade_id = publish_trade(form.trader_id.data, form.symbol.data, form.qty.data, form.side.data)
        flash('Trade successfully entered - {} - {} - {} - {}. Trade ID is {}.'.format(form.symbol.data, form.qty.data, form.side.data,
                                                                form.trader_id.data, trade_id))
        return redirect(url_for('home'))
    return render_template('receive_trade.html', title='New Trade', form=form)


def publish_trade(trader_id, symbol, qty, side):
    trade = dict()
    trade['symbol'] = symbol
    trade['qty'] = qty
    trade['side'] = side
    trade['trader_id'] = trader_id

    trade_id = emit_trade(trade)
    return trade_id


def emit_trade(trade):
    pub = Publisher(cfg)
    pub.publish(trade)
    return random.randint(100001, 999999)
