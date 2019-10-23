import pika
import json

EXCHANGE_NAME = 'trade_updates'
ROUTING_KEY = 'trade.new_trade'


def emit_trade(trade):

    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq-server'))
    channel = connection.channel()

    channel.exchange_declare(exchange=EXCHANGE_NAME, exchange_type='topic', durable=True)

    channel.basic_publish(exchange=EXCHANGE_NAME,
                          routing_key=ROUTING_KEY,
                          body=json.dumps(trade),
                          properties=pika.BasicProperties(
                              delivery_mode=2,
                          ))

    print("Successfully sent the data {} to the exchange {} with the routing key {}".format(trade, exchange_name,
                                                                                            routing_key))
    connection.close()
