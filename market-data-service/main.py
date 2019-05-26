import pika

SUBSCRIBED_SYMBOLS = []

def on_callback(ch, method, properties, body):
    print("Recevied {}".format(body))

def on_trade():

    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq-server'))
    channel = connection.channel()

    channel.queue_declare('trade.new_trade')

    channel.basic_consume(queue='trade.new_trade',
                          auto_ack=True,
                          on_message_callback=on_callback)
    print('Waiting for messages.. ')
    channel.start_consuming()

