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

logger = Logger.Logger("risk_publisher").get()
logger.setLevel(logging.DEBUG)

# noinspection PyUnresolvedReferences
INVENTORY_STORE = InventoryStore()


class RiskPublisher:

    """Manages the risk metrics for all incoming orders on a per-trader level"""

    def __init__(self):
        self.threads = []

    def start(self):
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
        INVENTORY_STORE.add_trade(trade=json.loads(body))
        logger.debug('Received trade ----> {}'.format(body))

    # noinspection PyMethodMayBeStatic
    def on_quotes_callback(self, body):
        # Todo Run all calculators on the inventoryStore
        logger.debug('Received quote -----> {}'.format(body))


if __name__ == "__main__":
    RiskPublisher().start()
