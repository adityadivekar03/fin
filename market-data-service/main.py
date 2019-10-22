from consumer import Consumer
from iexfinance.stocks import Stock
import json
from threading import Thread, Lock
from publisher import Publisher
import time
import config as cfg

MD_SUBSCRIPTIONS = []
IEX_TOKEN = "Tpk_36614967265944c6b4b3e47be6b2b3ca"
MUTEX = Lock()


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


def update_md_snaphots(prices):
    pass


def stream_quotes():
    if len(MD_SUBSCRIPTIONS) > 0:
        md_batch = Stock(MD_SUBSCRIPTIONS, token=IEX_TOKEN)
        prices = md_batch.get_price()
        update_md_snaphots(prices)
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
