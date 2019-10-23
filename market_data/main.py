from iexfinance.stocks import Stock
from iexfinance.iexdata import get_tops
import json
from threading import Thread, Lock
import time

from common_utils import Logger
import config as cfg
from consumer import Consumer
from publisher import Publisher

MD_SUBSCRIPTIONS = []
IEX_TOKEN = "Tpk_36614967265944c6b4b3e47be6b2b3ca"
MUTEX = Lock()
MD_BOOK = dict()


def on_callback(body):
    print("Received {}".format(body))
    body = json.loads(body)
    if 'symbol' not in body:
        print('Unexpected trade with no symbol')
    else:
        MUTEX.acquire()
        MD_SUBSCRIPTIONS.append(body['symbol'])
        MUTEX.release()



def start_main():
    consumer = Consumer(cfg.subcfg)
    with consumer:
        consumer.consume(on_callback)


def update_md_snaphots(tops):
    # Todo: Feature for only publishing if there is an update, else don't message
    tops = json.loads(tops)
    for update in tops:
        if update['symbol'] in MD_BOOK:
            update_ask_tob(update)
            update_bid_tob(update)
            update_last_trade(update)
        else:
            MD_BOOK[update['symbol']] = dict()
            MD_BOOK[update['symbol']]['bidPrice'] = None
            MD_BOOK[update['symbol']]['bidSize'] = None
            MD_BOOK[update['symbol']]['askPrice'] = None
            MD_BOOK[update['symbol']]['askSize'] = None
            MD_BOOK[update['symbol']]['lastSalePrice'] = None
            MD_BOOK[update['symbol']]['lastSaleSize'] = None
            update_ask_tob(update)
            update_bid_tob(update)
            update_last_trade(update)
    print('Market data book ------> ')
    print(MD_BOOK)


def update_ask_tob(update):
    MD_BOOK[update['symbol']]['askPrice'] = update['askPrice']
    MD_BOOK[update['symbol']]['askSize'] = update['askSize']


def update_bid_tob(update):
    MD_BOOK[update['symbol']]['bidPrice'] = update['bidPrice']
    MD_BOOK[update['symbol']]['bidSize'] = update['bidSize']


def update_last_trade(update):
    MD_BOOK[update['symbol']]['lastSalePrice'] = update['lastSalePrice']
    MD_BOOK[update['symbol']]['lastSaleSize'] = update['lastSaleSize']


def stream_quotes():
    if len(MD_SUBSCRIPTIONS) > 0:
        md_batch = Stock(MD_SUBSCRIPTIONS, token=IEX_TOKEN)
        prices = md_batch.get_price()
        tops = get_tops(MD_SUBSCRIPTIONS)
        update_md_snaphots(tops)
        pub = Publisher(cfg.pubcfg)
        pub.publish(prices)
        print('Publishing prices .. ----> \n')
        print(prices)
    else:
        print('No quotes to stream')
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
