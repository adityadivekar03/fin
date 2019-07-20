from consumer import Consumer
from config import subcfg, pubcfg
from iexfinance.stocks import Stock
import threading
from publisher import Publisher
import time

MD_SUBSCRIPTIONS = []
MD_BATCH = Stock()


def on_callback(ch, method, properties, body):
    print("Received {}".format(body))


def create_md_subscription(symbol):
    MD_SUBSCRIPTIONS.append(symbol)
    MD_BATCH = Stock(MD_SUBSCRIPTIONS)


def on_trade():
    consumer = Consumer(subcfg)
    with consumer:
        consumer.consume(on_callback)


def stream_quotes():
    prices = MD_BATCH.get_price()
    # publish prices to stallone service
    pub = Publisher(pubcfg)
    pub.publish(prices)
    time.sleep(10)
    t = threading.Thread(target=stream_quotes)
    t.start()


if __name__ == "__main__":
    # start quote streaming service
    threads = []
    t = threading.Thread(target=stream_quotes)
    threads.append(t)
    t.start()
    time.sleep(5)
    # start listening to entered trades
    on_trade()
