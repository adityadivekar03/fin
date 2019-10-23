#!/usr/bin/env python

# Consumer & Publisher config

subcfg_trades = {
    'host': 'rabbitmq',
    'exchangeName': 'trades',
    'exchangeType': 'fanout',
    'queueName': 'stallone_new_trade',
    'routingKey': 'new_trade',
    'exchangeOptions' : {
        'passive': False,
        'durable': False,
        'autoDelete': True,
        'internal': False
    },
    'queueOptions': {
        'passive': False,
        'durable': False,
        'autoDelete': True,
        'exclusive': False
    },
}

subcfg_quotes = {
    'host': 'rabbitmq',
    'exchangeName': 'quotes',
    'exchangeType': 'fanout',
    'queueName': 'new_quotes',
    'routingKey': 'new_quotes',
    'exchangeOptions' : {
        'passive': False,
        'durable': False,
        'autoDelete': True,
        'internal': False
    },
    'queueOptions': {
        'passive': False,
        'durable': False,
        'autoDelete': True,
        'exclusive': False
    },
}
