from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import os

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
secret_key = os.urandom(24)

def create_app():
	app = Flask(__name__)
	app.config['SECRET KEY'] = secret_key
	app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../instance/app.db'
	app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

	db.init_app(app)
	bcrypt.init_app(app)
	login_manager.init_app(app)
	login_manager.login_view = 'auth.login'

	# Import and register routes(register blueprints)
	from .routes.auth import auth as auth_blueprint
	from .routes.main import main as main_blueprint
	app.register_blueprint(auth_blueprint)
	app.register_blueprint(main_blueprint)

	return app
