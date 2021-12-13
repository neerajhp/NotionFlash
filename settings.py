import logging.config

LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,

    'formatters': {
        'default_formatter': {
            'format': '[%(levelname)s:%(asctime)s] %(message)s'
        },
    },

    'handlers': {
        'stream_handler': {
            'class': 'logging.StreamHandler',
            'formatter': 'default_formatter',
        },
    },

    'loggers': {
        'main': {
            'handlers': ['stream_handler'],
            'level': 'DEBUG',
            'propagate': True
        },
        'ankiservice': {
            'handlers': ['stream_handler'],
            'level': 'DEBUG',
            'propagate': True
        },
        'notionservice': {
            'handlers': ['stream_handler'],
            'level': 'DEBUG',
            'propagate': True
        }
    }
}

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger('my_logger')
logger.debug('debug log')
