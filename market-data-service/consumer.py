import pika
import traceback

class Consumer:
    def __init__(self, config):
        self.config = config

    def _create_connection(self):
        parameters = pika.ConnectionParameters(host=self.config['host'])
        return pika.BlockingConnection(parameters)