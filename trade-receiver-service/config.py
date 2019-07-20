#!/usr/bin/env python

# Publisher config

cfg = {
    'host': 'fin_rabbitmq_1',
    'exchangeName': 'trade_updates',
    'routingKey': 'new_trade',
}
