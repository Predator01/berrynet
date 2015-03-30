import os
import logging.config
import logging.handlers
import sys
BASE_DIR = os.environ['BERRYNET_ROOT']

if not os.path.exists(os.path.join(BASE_DIR, "logs")):
    os.makedirs(os.path.join(BASE_DIR, "logs"))

LOGGING ={
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '[%(asctime)s] %(levelname)s %(filename)s: %(message)s',
            'datefmt': '%d/%b/%Y %H:%M:%S'
        }
    },
    'handlers': {
        'debug': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': 'DEBUG',
            'filename': '%s/logs/debug.log' % BASE_DIR,
            'maxBytes': 524288,
            'backupCount': 7,
            'formatter': 'verbose',
        }
    },
    'loggers': {
        'berrynet': {
            'handlers': [
                'debug',
            ],
            'propagate': 'TRUE',
            'level': 'ERROR'
        },
        '': {
            'handlers': ['debug'],
            'level': 'DEBUG'
        }
    }
}


logging.config.dictConfig(LOGGING)  