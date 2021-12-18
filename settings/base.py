'''Settings for the project'''
import os

DATABASE = {
    'NAME': os.environ.get('POSTGRESQL_ADDON_DB', 'clover_health_assignment'),
    'USER': os.environ.get('POSTGRESQL_ADDON_USER', 'postgres'),
    'PASSWORD': os.environ.get('POSTGRESQL_ADDON_PASSWORD', 'toto42'),
    'HOST': os.environ.get('POSTGRESQL_ADDON_HOST', 'localhost'),
    'PORT': os.environ.get('POSTGRESQL_ADDON_PORT', 5432),
}
