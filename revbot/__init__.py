from flask import Flask
from .routes import customer_routes

def create_app():
    app = Flask(__name__)

    # Register blueprints
    app.register_blueprint(customer_routes)

    return app