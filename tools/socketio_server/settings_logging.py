
def get_logger_config(log_file_name):
    return {
        'version': 1,
        'formatters': {
            'normal': {
                'format': '%(asctime)s %(levelname)-8s %(name)-10s %(message)s',
                'datefmt': "%Y-%m-%d %H:%M:%S"
            },
            'verbose': {
                'format': '%(asctime)s %(levelname)-8s %(module)s::%(name)-10s %(message)s (%(filename)s:%(lineno)d).',
                'datefmt': "%Y-%m-%d %H:%M:%S"
            },
            'debug': {
                'format': '%(asctime)s %(levelname)-8s %(filename)16s:%(lineno)-4d :: %(message)s',
                'datefmt' : "%H:%M:%S"
            },
            'simple': {
                'format': '%(levelname)s %(message)s'
            },
            'only_message': {
                'format': '%(message)s',
            },
        },
        'disable_existing_loggers': False,
        'handlers': {
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'verbose'
                },
        },
        'root': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'loggers': {
            'runtime': {
                'handlers': ['console'],
                'level': 'DEBUG',
                'propagate': True,
            },
        }
    }
