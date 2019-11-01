import os
import logging
from . import settings


class Logger(object):
    def __init__(self, name):
        name = name.replace('.log', '')
        logger = logging.getLogger('%s.%s' % (settings.LOGGING_NAMESPACE, name))
        logger.setLevel(logging.INFO)
        if not logger.handlers:
            file_name = os.path.join(settings.LOGGING_DIR, '%s.log' % name)
            handler = logging.FileHandler(file_name)
            formatter = logging.Formatter('%(asctime)s %(levelname)s:%(name)s %(message)s')
            handler.setFormatter(formatter)
            handler.setLevel(logging.DEBUG)
            logger.addHandler(handler)
        self._logger = logger

    def get(self):
        return self._logger
