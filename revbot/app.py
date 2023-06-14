from flask import Flask, g
import os
from revbot.services.init_db import create_engine_and_session
from revbot.routes.customer_routes import customer_routes
from revbot.routes.contract_routes import contract_routes
from revbot.routes.revenuesegment_routes import revenuesegment_routes
from revbot.routes.dataframe_routes import dataframe_routes

def create_app():
    config_class = os.getenv('FLASK_CONFIG', 'Config')
    app = Flask(__name__)
    app.config.from_object(f'config.{config_class}')

    reset_and_init_db, create_session, remove_session = create_engine_and_session(app)
    reset_and_init_db()
    
    app.register_blueprint(customer_routes)
    app.register_blueprint(contract_routes)
    app.register_blueprint(revenuesegment_routes)
    app.register_blueprint(dataframe_routes)

    @app.before_request
    def before_request():
        g.db_session = create_session()

    @app.teardown_request
    def teardown_request(exception=None):
        remove_session(g.db_session)

    return app
