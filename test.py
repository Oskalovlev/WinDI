# from src.core.database.config import db_settings as settings

# print(settings.database)

import configparser

def get_config_options():
    parser = configparser.ConfigParser()
    parser.read('alembic.ini')
    
    options = {}
    if parser.has_section('alembic'):
        items = parser.items('alembic')
        for key, value in items:
            options[key] = value
    
    return options

options = get_config_options()
print(options.get('sqlalchemy.url'))
