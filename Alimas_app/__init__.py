from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import Config
from Alimas_app.extensions import db

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    app.config['SECRET_KEY'] = config_class.SECRET_KEY

    db.init_app(app)
    CORS(app)
    JWTManager(app)

    # Register blueprints
    from Alimas_app.dashboard import bp as dashboard_bp
    app.register_blueprint(dashboard_bp, url_prefix='/')

    from Alimas_app.managecustomers import bp as managecustomers_bp
    app.register_blueprint(managecustomers_bp, url_prefix='/user')

    from Alimas_app.managesnacks import bp as managesnacks_bp
    app.register_blueprint(managesnacks_bp, url_prefix='/todayspecial')

    return app
