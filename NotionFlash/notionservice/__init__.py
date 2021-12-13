from logging import StreamHandler
import sys
import logging
import logging.config

# # Logging Utility
# logger = logging.getLogger(__name__)
logging.config.fileConfig(fname='logging.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)

logger.info('Module ' + __name__ + ' initialised')
