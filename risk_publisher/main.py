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
                if self.inventory[i].symbol == trade.symbol:
                    if self.inventory[i].side == trade.side:
                        self.inventory[i].qty += trade.qty
                    else:
                        if self.inventory[i].qty > trade.qty:
                            self.inventory[i].qty -= trade.qty
                        else:
                            self.inventory[i].qty = trade.qty - self.inventory[i].qty
                            self.inventory[i].side = trade.side
                else:
                    self.inventory.append(trade)
        else:
            self.inventory.append(trade)


class InventoryStore:

    """ Set of all inventories that the risk publisher will maintain"""

    def __init__(self):
        self.inventories = []
        self.traders_map = map()

    def add_trade(self, trade):
        if trade.trader_id in self.traders_map:
            self.inventories[self.traders_map[trade.trader_id]].add_trade(trade)
        else:
            inventory = Inventory(trade.trader_id)
            self.inventories.append(inventory)
            self.traders_map[trade.trader_id] = len(self.inventories) - 1


INVENTORY_STORE = InventoryStore()


def on_trades_callback(body):
    # Save trade for the respective trader
    INVENTORY_STORE.add_trade(trade=json.loads(body))
    logger.debug('Received trade ----> {}'.format(body))


def on_quotes_callback(body):
    # Save in global quote bank
    logger.debug('Received quote -----> {}'.format(body))


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