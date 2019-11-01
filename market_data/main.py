from iexfinance.stocks import Stock
from iexfinance.iexdata import get_tops
import json
import logging
from threading import Thread, Lock
import time

from common_utils import Logger
from common_utils.publisher import Publisher
from common_utils.consumer import Consumer
from config import *

tops = get_tops(["AAPL"])

MD_SUBSCRIPTIONS = []
IEX_TOKEN = "Tpk_36614967265944c6b4b3e47be6b2b3ca"
MUTEX = Lock()
MD_BOOK = dict()

logger = Logger.Logger("market_data").get()
logger.setLevel(logging.DEBUG)


def on_callback(body):
    print("Received {}".format(body))
    body = json.loads(body)
    if 'symbol' not in body:
        logger.error('Unexpected trade with no symbol')
    else:
        MUTEX.acquire()
        MD_SUBSCRIPTIONS.append(body['symbol'])
        MUTEX.release()


def start_main():
    consumer = Consumer(subcfg)
    with consumer:
        consumer.consume(on_callback)


def update_md_snaphots(tops):
    # Todo: Feature for only publishing if there is an update, else don't message
    for data in tops:
        if data['symbol'] in MD_BOOK:
            update_ask_tob(data)
            update_bid_tob(data)
            update_last_trade(data)
        else:
            MD_BOOK[data['symbol']] = dict()
            MD_BOOK[data['symbol']]['bidPrice'] = None
            MD_BOOK[data['symbol']]['bidSize'] = None
            MD_BOOK[data['symbol']]['askPrice'] = None
            MD_BOOK[data['symbol']]['askSize'] = None
            MD_BOOK[data['symbol']]['lastSalePrice'] = None
            MD_BOOK[data['symbol']]['lastSaleSize'] = None
            update_ask_tob(data)
            update_bid_tob(data)
            update_last_trade(data)
    logger.debug("Updated market data snapshot")
    logger.debug("%s\n", MD_BOOK)


def update_ask_tob(data):
    MD_BOOK[data['symbol']]['askPrice'] = data['askPrice']
    MD_BOOK[data['symbol']]['askSize'] = data['askSize']


def update_bid_tob(data):
    MD_BOOK[data['symbol']]['bidPrice'] = data['bidPrice']
    MD_BOOK[data['symbol']]['bidSize'] = data['bidSize']


def update_last_trade(data):
    MD_BOOK[data['symbol']]['lastSalePrice'] = data['lastSalePrice']
    MD_BOOK[data['symbol']]['lastSaleSize'] = data['lastSaleSize']


def stream_quotes():
    if len(MD_SUBSCRIPTIONS) > 0:
        md_batch = Stock(MD_SUBSCRIPTIONS, token=IEX_TOKEN)
        prices = md_batch.get_price()
        tops = get_tops(MD_SUBSCRIPTIONS)
        update_md_snaphots(tops)
        pub = Publisher(pubcfg)
        pub.publish(prices)
        logger.info("Publishing prices")
        logger.info(prices)
    else:
        logger.info("No quotes to stream")
    time.sleep(5)
    stream_quotes()


if __name__ == "__main__":
    # Start quote streaming service
    print('Starting quote streaming service...')
    threads = []
    t = Thread(target=stream_quotes)
    threads.append(t)
    t.start()
    time.sleep(1)

    # Start listening to entered trades
    print('Starting market data service...')
    start_main()
