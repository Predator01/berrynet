import os
import logging.config
import sys
BASE_DIR = os.environ['BERRYNET_ROOT']

if not os.path.exists(os.path.join(BASE_DIR, "logs")):
    os.makedirs(os.path.join(BASE_DIR, "logs"))

LOGGING ={
    "version": 1,
    "disable_existing_loggers": "FALSE",
    "formatters": {
        "verbose": {
            "format": "[%(asctime)s] %(levelname)s %(filename)s: %(message)s",
            "datefmt": "%d/%b/%Y %H:%M:%S"
        }
    },
    "handlers": {
        "debug": {
            "level": "DEBUG",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "%s/logs/debug.log" % BASE_DIR,
            "maxBytes": "1024",
            "backupCount": "7",
            "formatter": "verbose",
        }
    },
    "loggers": {
        "berrynet": {
            "handlers": [
                "debug",
            ],
            "propagate": "TRUE",
            "level": "ERROR"
        },
        "": {
            "handlers": [
                "debug"
            ],
            "level": "DEBUG"
        }
    }
}

logging.config.dictConfig(LOGGING)