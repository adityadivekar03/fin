"""
High level settings for common_utils like Logging are defined here.

Settings for other modules can be defined here - but should be placed clubbed together in a specific
region.

"""
import os


###############################################################################
# COMMON_UTILS
###############################################################################

# store logs relative to the current docker container dir
LOGGING_DIR = './logs/'
LOGGING_NAMESPACE = 'fin'


###############################################################################
# TRADE RECEIVER
###############################################################################

SECRET_KEY=os.environ.get('SECRET_KEY') or 'very-difficult-to-crack-secret-key'
