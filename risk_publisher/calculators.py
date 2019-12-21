import logging

from models import RiskCalculator
from common_utils import Logger, calcUtils


logger = Logger.Logger("risk_calculators").get()
logger.setLevel(logging.DEBUG)


class ProfitLoss(RiskCalculator):

    """Simple pnl calculator"""

    def ___init__(self):
        super().__init__()

    def calculate(self, calculator_input, market_data):
        """
        Use the original prices of all trades from the inventory and
        find pnl using the current market data.
        Input: SingleTrade
        :return: None
        """
        logger.info('Running ProfitLoss calculator')
        trade_price = calculator_input.get_price()
        symbol = calculator_input.get_symbol()
        qty = calculator_input.get_qty()
        side = calculator_input.get_side()

        # Market data is the MD_BOOK
        print('market data ')
        print(market_data)
        current_price = calcUtils.get_mid_price(market_data[symbol])

        if side == 1:  # buy
            unit_pnl = current_price - trade_price
            total_pnl = qty * unit_pnl
        else:
            unit_pnl = trade_price - current_price
            total_pnl = qty * unit_pnl
        calculator_input.set_metric('pnl', total_pnl)
        return


class PortfolioComposition(RiskCalculator):

    """Calculate %tage composition of portfolio"""

    def __init__(self):
        super().__init__()
        self.inventory_level = True

    def calculate(self, inventory, market_data):

        """Use current value of trades to calculate %tage composition. """

        logger.info('Running PortfolioComposition calculator')
        total_value = 0
        for i in range(0, len(inventory.trades)):
            qty = inventory.trades[i].get_qty()
            symbol = inventory.trades[i].get_symbol()
            current_value = qty * calcUtils.get_mid_price(market_data[symbol])
            inventory.trades[i].set_metric('currentValue', current_value)
            total_value += current_value

        for i in range(0, len(inventory.trades)):
            current_value = inventory.trades[i].get_metric('currentValue')
            inventory.trades[i].set_metric('%age', current_value/total_value)
        return
