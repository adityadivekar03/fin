#!/usr/bin/env python

# Consumer config

subcfg = {
    'host': 'fin_rabbitmq_1',
    'exchangeName': 'trade_updates',
    'exchangeType': 'topic',
    'queueName': 'new_trade',
    'routingKey': 'new_trade',
    'exchangeOptions' : {
        'passive': False,
        'durable': False,
        'autoDelete': True,
        'internal': True
    },
    'queueOptions': {
        'passive': False,
        'durable': False,
        'autoDelete': True,
        'exclusive': False
    },

}

pubcfg = {
    'host': 'fin_rabbitmq_1',
    'exchangeName': 'quote_updates',
    'routingKey': 'new_quotes',
}
