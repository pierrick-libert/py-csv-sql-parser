'''Settings for the project'''
import os

DATABASE = {
    'NAME': os.environ.get('POSTGRESQL_ADDON_DB', 'python_sql_csv_parser'),
    'USER': os.environ.get('POSTGRESQL_ADDON_USER', 'postgres'),
    'PASSWORD': os.environ.get('POSTGRESQL_ADDON_PASSWORD', 'toto42'),
    'HOST': os.environ.get('POSTGRESQL_ADDON_HOST', 'localhost'),
    'PORT': os.environ.get('POSTGRESQL_ADDON_PORT', 5432),
    'URI': os.environ.get('POSTGRESQL_ADDON_URI', None),
}

ENV = os.environ.get('ENV', 'local')
