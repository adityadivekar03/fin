import logging
from threading import Thread
import time

from common_utils import Logger
from common_utils.consumer import Consumer
from config import *

logger = Logger.Logger("market_data").get()
logger.setLevel(logging.DEBUG)


def on_trades_callback(body):
    print('Received trade ----> {}'.format(body))


def on_quotes_callback(body):
    print('Received quote -----> {}'.format(body))


def start_listening_trades():
    consumer = Consumer(subcfg_trades)
    with consumer:
        consumer.consume(on_trades_callback)


def start_listening_quotes():
    consumer = Consumer(subcfg_quotes)
    with consumer:
        consumer.consume(on_quotes_callback)


if __name__ == "__main__":
    # Start listening to entered trades & entered quotes
    print('Listening to entered trades...')
    threads = []
    t = Thread(target=start_listening_trades)
    threads.append(t)
    t.start()
    time.sleep(1)

    print('Listening to entered quotes...')
    t = Thread(target=start_listening_quotes)
    threads.append(t)
    t.start()
    time.sleep(1)