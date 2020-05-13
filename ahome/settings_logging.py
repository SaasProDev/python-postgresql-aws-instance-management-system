import os, socket, logging

urllib3_logger = logging.getLogger('urllib3')
urllib3_logger.setLevel(logging.CRITICAL)

BASE_DIR = os.getenv("BASE_DIR")
LOGGING_FOLDER = os.getenv("LOGGING_FOLDER", "./")

HOST_NAME = os.environ.get('HOST') or socket.gethostname()


def rabbit_routing_key_formatter(rec):
    data = rec.__dict__
    # from pprint import pprint
    # pprint(data, indent=4)
    module = data['name'].split(".")[0]
    level = data['levelname'].lower()
    routing_key = "{}.{}".format(module, level)
    rec.routing_key = routing_key
    rec.module_name = module
    # rec.level =
    # print("**** ROUTING KEY: '{}' *****".format(routing_key))
    return routing_key


def logging_config(settings):
    return {
        'version': 1,
        'formatters': {
            'normal': {
                'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s',
                'datefmt' : "%d/%b/%Y %H:%M:%S"
            },
            'verbose': {
                'format': '[%(asctime)s %(levelname)-8s %(name)-10s] %(message)s (%(filename)s:%(lineno)d).',
                'datefmt': "%H:%M:%S"
            },
            'simple': {
                'format': '%(levelname)s %(message)s'
            },
            'json': {
                '()': 'pythonjsonlogger.jsonlogger.JsonFormatter',
                'fmt': '%(name)s %(levelname) %(asctime)s %(message)s'
            }
        },
        'disable_existing_loggers': False,
        'filters': {
            'require_debug_false': {
                '()': 'django.utils.log.RequireDebugFalse'
            },
        },
        'handlers': {
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'verbose'
                },
            'file': {
                'level': 'DEBUG',
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': '{}/ahome.log'.format(LOGGING_FOLDER),
                'maxBytes': 1024*1024*1,
                'backupCount': 10,
                'formatter': 'simple'
                },
            'rabbit': {
                'level': 'DEBUG',
                #'class': 'python_logging_rabbitmq.RabbitMQHandlerOneWay',
                'class': 'ahome.WrappedRabbitMQHandler.RabbitLogger',
                'host': settings.RABBIT_HOST,
                # 'filters': ['rabbit'],
                'formatter': 'json',
                'port': settings.RABBIT_PORT,
                'username': settings.RABBIT_USERNAME,
                'password': settings.RABBIT_PASSWORD,
                'exchange': 'ahome.server',
                'declare_exchange': False,
                'connection_params': {
                    'virtual_host': settings.RABBIT_VHOST,
                    'connection_attempts': 3,
                    'socket_timeout': 5000
                },
                'routing_key_formatter': rabbit_routing_key_formatter,
            },
        },
        'root': {
            'handlers': ['console', 'rabbit'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'loggers': {
            'pika': {
                'handlers': ['console', 'rabbit'],
                'level': 'INFO',
                'propagate': False,
            },
            'django.request': {
                'handlers': ['console', 'rabbit'],
                'level': 'DEBUG',
                'propagate': False,
            },
            'django.channels.server': {
                'handlers': ['console', 'rabbit'],
                'level': 'WARNING',
                'propagate': False,
            },
            'django': {
                'handlers': ['console', 'rabbit'],
                'level': 'INFO',
                'propagate': False,
            },
            'daphne.http_protocol': {
                'handlers': ['console'],
                'level': 'INFO',
                'propagate': False,
            },
            'daphne.ws_protocol': {
                'handlers': ['console'],
                'level': 'INFO',
                'propagate': False,
            },
            'core': {
                'handlers': ['console', 'rabbit'],
                'level': 'DEBUG',
                'propagate': False,
            },
            'account': {
                'handlers': ['console', 'rabbit'],
                'level': 'DEBUG',
                'propagate': False,
            },
            'celery': {
                'handlers': ['console', 'rabbit'],
                'level': 'DEBUG',
                'propagate': True
            },
            'CELERY': {
                'handlers': ['console', 'rabbit'],
                'level': 'DEBUG',
                'propagate': True
            },
            'celery.task': {
                'handlers': ['console', 'rabbit'],
                'level': 'DEBUG',
                'propagate': True
            },
            'celerytask': {
                'handlers': ['console', 'rabbit'],
                'level': 'DEBUG',
                'propagate': True
            },
        }
    }

def logging_config_no_rabbit(settings):
    return {
        'version': 1,
        'formatters': {
            'normal': {
                'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s',
                'datefmt': "%d/%b/%Y %H:%M:%S"
            },
            'verbose': {
                'format': '[%(asctime)s %(levelname)-8s %(name)-10s] %(message)s (%(filename)s:%(lineno)d).',
                'datefmt': "%H:%M:%S"
            },
            'simple': {
                'format': '%(levelname)s %(message)s'
            },
            'json': {
                '()': 'pythonjsonlogger.jsonlogger.JsonFormatter',
                'fmt': '%(name)s %(levelname) %(asctime)s %(message)s'
            }
        },
        'disable_existing_loggers': False,
        'filters': {
            'require_debug_false': {
                '()': 'django.utils.log.RequireDebugFalse'
            },
        },
        'handlers': {
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'verbose'
            },
            'file': {
                'level': 'DEBUG',
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': '{}/ahome.log'.format(LOGGING_FOLDER),
                'maxBytes': 1024 * 1024 * 1,
                'backupCount': 10,
                'formatter': 'simple'
            },

        },
        'root': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'loggers': {
            'pika': {
                'handlers': ['console'],
                'level': 'INFO',
                'propagate': False,
            },
            'django.request': {
                'handlers': ['console'],
                'level': 'DEBUG',
                'propagate': False,
            },
            'django.channels.server': {
                'handlers': ['console'],
                'level': 'WARNING',
                'propagate': False,
            },
            'django': {
                'handlers': ['console'],
                'level': 'INFO',
                'propagate': False,
            },
            'daphne.http_protocol': {
                'handlers': ['console'],
                'level': 'INFO',
                'propagate': False,
            },
            'daphne.ws_protocol': {
                'handlers': ['console'],
                'level': 'INFO',
                'propagate': False,
            },
            'core': {
                'handlers': ['console'],
                'level': 'DEBUG',
                'propagate': False,
            },
            'account': {
                'handlers': ['console'],
                'level': 'DEBUG',
                'propagate': False,
            },
            'celery': {
                'handlers': ['console'],
                'level': 'DEBUG',
                'propagate': True
            },
            'CELERY': {
                'handlers': ['console'],
                'level': 'DEBUG',
                'propagate': True
            },
            'celery.task': {
                'handlers': ['console'],
                'level': 'DEBUG',
                'propagate': True
            },
            'celerytask': {
                'handlers': ['console'],
                'level': 'DEBUG',
                'propagate': True
            },
        }
    }
