import os
from flask import Flask
from .quantum_key_dist_api.views import quantum_key_dist_api_bp
from .communication_app.views import communication_app_bp
from src.authentication_app.views import authentication_bp
from src.authentication_app.models import db
from flask_migrate import Migrate
from dotenv import load_dotenv

def create_app():
    load_dotenv()
    app = Flask(__name__)
    app.secret_key = os.getenv("SECRET_KEY")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI")
    db.init_app(app)
    migrate = Migrate(app, db)
    app.register_blueprint(authentication_bp)
    app.register_blueprint(quantum_key_dist_api_bp)
    app.register_blueprint(communication_app_bp)
    return app