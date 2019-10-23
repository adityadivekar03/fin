#!/usr/bin/env python

# Consumer & Publisher config

subcfg = {
    'host': 'rabbitmq',
    'exchangeName': 'trades',
    'exchangeType': 'fanout',
    'queueName': 'mds_new_trade',
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

pubcfg = {
    'host': 'rabbitmq',
    'exchangeName': 'quotes',
    'routingKey': 'new_quotes',
}
