class SingleTrade:

    """Represents a single trade"""

    def __init__(self, symbol, qty, side):
        self.symbol = symbol
        self.qty = qty
        self.side = side
        self.trade_price = 5
        self.calculated_metrics = dict()

    def get_symbol(self):
        return self.symbol

    def get_qty(self):
        return self.qty

    def get_side(self):
        return self.side

    def get_price(self):
        return self.trade_price

    def set_metric(self, key, value):
        self.calculated_metrics[key] = value

    def get_metric(self, key):
        return self.calculated_metrics[key]

    def set_rolling_metric(self, key, value):
        if key not in self.calculated_metrics:
            self.calculated_metrics[key] = list()
            self.calculated_metrics[key].append(value)
        else:
            self.calculated_metrics[key].append(value)


class Inventory:

    """Represents the inventory of a single trader - collection of SingleTrade objects"""

    def __init__(self, trader_id):
        self.trades = []
        self.trader_id = trader_id
        self.calculated_metrics = dict()

    def add_trade(self, trade):
        if len(self.trades) > 0:
            for i in range(0, len(self.trades)):
                if self.trades[i].symbol == trade['symbol']:
                    if self.trades[i].side == trade['side']:
                        self.trades[i].qty += trade['qty']
                    else:
                        if self.trades[i].qty > trade['qty']:
                            self.trades[i].qty -= trade['qty']
                        else:
                            self.trades[i].qty = trade['qty'] - self.inventory[i]['qty']
                            self.trades[i].side = trade['side']
                else:
                    self.trades.append(SingleTrade(trade['symbol'], trade['qty'], trade['side']))
        else:
            self.trades.append(SingleTrade(trade['symbol'], trade['qty'], trade['side']))


class InventoryStore:

    """Set of all inventories that the risk publisher will maintain - collection of Inventory objects"""

    def __init__(self):
        self.inventories = []
        self.traders_map = dict()

    def add_trade(self, trade):
        if trade['trader_id'] in self.traders_map:
            self.inventories[self.traders_map[trade['trader_id']]].add_trade(trade)
        else:
            inventory = Inventory(trade['trader_id'])
            inventory.add_trade(trade)
            self.inventories.append(inventory)
            self.traders_map[trade['trader_id']] = len(self.inventories) - 1

    def is_inventory_empty(self):
        return len(self.inventories) == 0

    def get_inventories(self):
        return self.inventories


class RiskCalculator:

    """
    Abstract base class for all calculators/.
    Calculators can be at a single trade level or at the inventory level.
    """

    def __init__(self):
        self.inventory_level = False  # Should run at Inventory or at SingleTrade level

    def run(self, inventory_store, market_data):
        if self.inventory_level:
            for inventory in inventory_store.get_inventories():
                self.calculate(inventory, market_data)
        else:
            for inventory in inventory_store.get_inventories():
                print('level 1')
                for trade in inventory.trades:
                    print('level 2')
                    self.calculate(trade, market_data)
        return

    def calculate(self, calculator_input, market_data):
        # each calculator needs to implement this with its own behaviour
        pass
