from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from flask_scss import Scss

from config import Config

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
mail = Mail()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app=app)
    migrate.init_app(app=app, db=db)
    login_manager.init_app(app=app)
    mail.init_app(app=app)
    Scss(app)
    from app.auth import auth as auth_bp
    app.register_blueprint(auth_bp)
    from app.core import core as core_bp
    app.register_blueprint(core_bp)
    from app.subreddit import subreddit as subreddit_bp
    app.register_blueprint(subreddit_bp)
    from .models import comment, post, user, subreddit

    return app
