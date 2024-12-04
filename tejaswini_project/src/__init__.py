import os
from flask import Flask
from .quantum_key_dist_api.views import quantum_key_dist_api_bp
from .communication_app.views import communication_app_bp
from .authentication_app.views import authentication_bp
from .authentication_app.models import db
from flask_migrate import Migrate
from dotenv import load_dotenv
from .authentication_app.login_mgr import login_manager
from flask_cors import CORS


def create_app():
    load_dotenv()
    app = Flask(__name__)
    app.secret_key = os.getenv("SECRET_KEY")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI")
    login_manager.init_app(app)
    db.init_app(app)
    migrate = Migrate(app, db)
    CORS(app, supports_credentials=True)
    app.register_blueprint(authentication_bp)
    app.register_blueprint(quantum_key_dist_api_bp)
    app.register_blueprint(communication_app_bp)
    return app