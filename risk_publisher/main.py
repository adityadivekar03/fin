import json
import logging
from threading import Thread
import time

from common_utils import Logger
from common_utils.consumer import Consumer
# noinspection PyUnresolvedReferences
from config import *
# noinspection PyUnresolvedReferences
from models import *
# noinspection PyUnresolvedReferences
from calculators import *

logger = Logger.Logger("risk_publisher").get()
logger.setLevel(logging.DEBUG)


class RiskPublisher:

    """Manages the risk metrics for all incoming orders on a per-trader level"""

    def __init__(self):
        self.threads = []
        self.calculators = []
        self.cache_md = None
        self.inventory_store = InventoryStore()

    def start(self):
        self.create_calculators()

        logger.info('Listening to entered trades...')
        t = Thread(target=self.start_listening_trades)
        self.threads.append(t)
        t.start()
        time.sleep(1)

        logger.info('Listening to entered quotes...')
        t = Thread(target=self.start_listening_quotes)
        self.threads.append(t)
        t.start()
        time.sleep(1)

    def start_listening_quotes(self):
        # noinspection PyUnresolvedReferences
        consumer = Consumer(subcfg_quotes)
        with consumer:
            consumer.consume(self.on_quotes_callback)

    def start_listening_trades(self):
        # noinspection PyUnresolvedReferences
        consumer = Consumer(subcfg_trades)
        with consumer:
            consumer.consume(self.on_trades_callback)

    # noinspection PyMethodMayBeStatic
    def on_trades_callback(self, body):
        print('trades callback')
        if self.cache_md is not None:
            self.run_calculators()
        self.inventory_store.add_trade(trade=json.loads(body))
        logger.debug('Received trade ----> {}'.format(body))

    # noinspection PyMethodMayBeStatic
    def on_quotes_callback(self, body):
        self.cache_md = json.loads(body)
        print('quotes callback')
        if not self.inventory_store.is_inventory_empty():
            self.run_calculators()
        logger.debug('Received quote -----> {}'.format(body))

    def create_calculators(self):
        self.calculators.append(ProfitLoss())

    def run_calculators(self):
        print('running calc')
        for calculator in self.calculators:
            print('running now')
            calculator.run(self.inventory_store, self.cache_md)
        print(self.inventory_store.get_inventories)


if __name__ == "__main__":
    RiskPublisher().start()
