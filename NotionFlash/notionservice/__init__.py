from logging import StreamHandler
import os
import logging
import logging.config

# # Logging Utility
logging.config.fileConfig(fname="./logs/logging.conf",
                          disable_existing_loggers=False)
logger = logging.getLogger(__name__)

logger.info('Module ' + __name__ + ' initialised')
