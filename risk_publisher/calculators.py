import logging

from .models import RiskCalculator
from common_utils import Logger


logger = Logger.Logger("risk_calculators").get()
logger.setLevel(logging.DEBUG)


class ProfitNLoss(RiskCalculator):

    """Simple pnl calculator"""

    def ___init__(self, market_data, inventory_store):
        super().__init__(self, market_data, inventory_store)

    def calculate(self, input):
        """
        Use the original prices of all trades from the inventory and
        find pnl using the current market data.
        Input: SingleTrade
        :return: None
        """
        logger.info('Running profit/loss calculator')
        trade_price = input.get_price()
        symbol = input.get_symbol()
        qty = input.get_qty()
        side = input.get_side()
        # Market data is the MD_BOOK
        current_price = self.market_data[symbol]['bidPrice'] + self.market_data[symbol]['askPrice'] / 2.0

        unit_pnl = 0
        total_pnl = 0
        if side == 1:  # buy
            unit_pnl = current_price - trade_price
            total_pnl = qty * unit_pnl
        else:
            unit_pnl = trade_price - current_price
            total_pnl = qty * unit_pnl
        input.set_metric('pnl', total_pnl)

        return
