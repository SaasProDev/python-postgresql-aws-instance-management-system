import os

from django.conf import settings

from dotenv import load_dotenv

# project_folder = os.path.expanduser('~/ahome')  # adjust as appropriate

load_dotenv(os.path.join(settings.BASE_DIR, '.env'))


ENGINES = {
    'sqlite': 'django.db.backends.sqlite3',
    'postgresql': 'django.db.backends.postgresql_psycopg2',
    'mysql': 'django.db.backends.mysql',
}

DATABASE_ENGINE = os.getenv("DATABASE_ENGINE", ENGINES['sqlite'])
DATABASE_NAME = os.getenv("DATABASE_NAME", 'postgres')
DATABASE_USER = os.getenv("DATABASE_USER", 'postgres')
DATABASE_ADMIN_USER = os.getenv("DATABASE_ADMIN_USER", 'postgres')
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD", 'postgres')
DATABASE_ADMIN_PASSWORD = os.getenv("DATABASE_ADMIN_PASSWORD", 'postgres')
DATABASE_HOST = os.getenv("DATABASE_HOST", 'postgres')
DATABASE_PORT = os.getenv("DATABASE_PORT", '5432')





def config():

    service_name = os.getenv('DATABASE_SERVICE_NAME', DATABASE_ENGINE).upper().replace('-', '_')

    # if openshift or Kubernetes
    database_user = os.getenv('DATABASE_USER', DATABASE_USER)
    database_pass = os.getenv('DATABASE_PASSWORD', DATABASE_PASSWORD)
    
    if os.getenv('OPENSHIFT_BUILD_NAMESPACE'):
        database_user = os.getenv('DATABASE_ADMIN_USER', DATABASE_ADMIN_USER)
        database_pass = os.getenv('DATABASE_ADMIN_PASSWORD', DATABASE_ADMIN_PASSWORD)

    if service_name:
        engine = ENGINES.get(os.getenv('DATABASE_ENGINE'), ENGINES['sqlite'])
    else:
        engine = ENGINES['sqlite']
    
    name = os.getenv('DATABASE_NAME', DATABASE_NAME)
    
    if not name and engine == ENGINES['sqlite']:
        name = os.path.join(settings.BASE_DIR, 'db.sqlite3')
    return {
        'ENGINE': engine,
        'NAME': name,
        'USER': database_user, #os.getenv('DATABASE_ADMIN_USER', DATABASE_ADMIN_USER),
        'PASSWORD': database_pass, #os.getenv('DATABASE_ADMIN_PASSWORD', DATABASE_ADMIN_PASSWORD),
        'HOST': os.getenv('{}_SERVICE_HOST'.format(service_name), DATABASE_HOST),
        'PORT': os.getenv('{}_SERVICE_PORT'.format(service_name), DATABASE_PORT),
    }

