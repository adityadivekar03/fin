import pika
import traceback


class Publisher:
    def __init__(self, config):
        self.config = config

    def _create_connection(self):
        parameters = pika.ConnectionParameters(self.config['host'])
        return pika.BlockingConnection(parameters)

    def publish(self, message):
        connection = None
        try:
            connection = self._create_connection()
            channel = connection.channel()
            channel.exchange_declare(exchange=self.config['exchangeName'], passive=True)
            channel.basic_publish(exchange=self.config['exchangeName'], routing_key=self.config['routingKey'],
                                  body=message)
            print("[x] Sent message %r " % message)
        except Exception as e:
            print(repr(e))
            traceback.print_exc()
            raise e
        finally:
            if connection:
                connection.close()




