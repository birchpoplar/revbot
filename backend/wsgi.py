import os
from revbot.app import create_app

config_class = os.getenv('FLASK_CONFIG', 'Config')
application = create_app(config_class)
