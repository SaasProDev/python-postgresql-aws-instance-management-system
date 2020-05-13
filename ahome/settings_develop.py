from os import environ
environ['ENVIRONMENT_MODE'] = 'DEVELOP'

environ['DATABASE_HOST'] = 'localhost'
environ['DATABASE_PORT'] = '5432'

environ['REDIS_HOST_NAME'] = 'localhost'

from .settings import *
