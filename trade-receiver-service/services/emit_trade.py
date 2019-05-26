import pika
import json


def emit_trade(trade):

    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq-server'))
    channel = connection.channel()

    exchange_name = 'trade_updates'
    routing_key = 'trade.new_trade'

    channel.exchange_declare(exchange=exchange_name, exchange_type='topic', durable=True)

    channel.basic_publish(exchange=exchange_name,
                          routing_key=routing_key,
                          body=json.dumps(trade),
                          properties=pika.BasicProperties(
                              delivery_mode=2,
                          ))

    print("Successfully sent the data {} to the exchange {} with the routing key {}".format(trade, exchange_name,
                                                                                            routing_key))
    connection.close()
