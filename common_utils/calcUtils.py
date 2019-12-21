# Common utils used throughout the project


def get_mid_price(market_data):
    ask_price = market_data['askPrice']
    bid_price = market_data['bidPrice']
    return (ask_price+bid_price) / 2.0
