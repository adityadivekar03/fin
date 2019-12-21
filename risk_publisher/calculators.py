import logging

from models import RiskCalculator
from common_utils import Logger


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
        logger.info('Running profit/loss calculator')
        trade_price = calculator_input.get_price()
        symbol = calculator_input.get_symbol()
        qty = calculator_input.get_qty()
        side = calculator_input.get_side()

        # Market data is the MD_BOOK
        print('market data ')
        print(market_data)
        current_price = (market_data[symbol]['bidPrice'] + market_data[symbol]['askPrice']) / 2.0

        if side == 1:  # buy
            unit_pnl = current_price - trade_price
            total_pnl = qty * unit_pnl
        else:
            unit_pnl = trade_price - current_price
            total_pnl = qty * unit_pnl
        calculator_input.set_metric('pnl', total_pnl)

        return
