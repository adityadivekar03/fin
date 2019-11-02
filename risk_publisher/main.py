import json
import logging
from threading import Thread
import time

from common_utils import Logger
from common_utils.consumer import Consumer
from config import *

logger = Logger.Logger("market_data").get()
logger.setLevel(logging.DEBUG)


class SingleTrade:

    """Represents a single trade"""

    def __init__(self, symbol, qty, side):
        self.symbol = symbol
        self.qty = qty
        self.side = side

    def get_symbol(self):
        return self.symbol

    def get_qty(self):
        return self.qty

    def get_side(self):
        return self.side


class Inventory:

    """Represents the inventory of a single trader - collection of SingleTrade objects"""

    def __init__(self, trader_id):
        self.inventory = []
        self.trader_id = trader_id

    def add_trade(self, trade):
        if len(self.inventory) > 0:
            for i in range(0, len(self.inventory)):
                if self.inventory[i].symbol == trade['symbol']:
                    if self.inventory[i].side == trade['side']:
                        self.inventory[i].qty += trade['qty']
                    else:
                        if self.inventory[i].qty > trade['qty']:
                            self.inventory[i].qty -= trade['qty']
                        else:
                            self.inventory[i].qty = trade['qty'] - self.inventory[i]['qty']
                            self.inventory[i].side = trade['side']
                else:
                    self.inventory.append(trade)
        else:
            self.inventory.append(trade)


class InventoryStore:

    """ Set of all inventories that the risk publisher will maintain"""

    def __init__(self):
        self.inventories = []
        self.traders_map = dict()

    def add_trade(self, trade):
        if trade['trader_id'] in self.traders_map:
            self.inventories[self.traders_map[trade['trader_id']]].add_trade(trade)
        else:
            inventory = Inventory(trade['trader_id'])
            self.inventories.append(inventory)
            self.traders_map[trade['trader_id']] = len(self.inventories) - 1


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
        consumer = Consumer(subcfg_quotes)
        with consumer:
            consumer.consume(self.on_quotes_callback)

    def start_listening_trades(self):
        consumer = Consumer(subcfg_trades)
        with consumer:
            consumer.consume(self.on_trades_callback)

    # noinspection PyMethodMayBeStatic
    def on_trades_callback(self, body):
        INVENTORY_STORE.add_trade(trade=json.loads(body))
        logger.debug('Received trade ----> {}'.format(body))

    # noinspection PyMethodMayBeStatic
    def on_quotes_callback(self, body):
        logger.debug('Received quote -----> {}'.format(body))


if __name__ == "__main__":
    RiskPublisher().start()
