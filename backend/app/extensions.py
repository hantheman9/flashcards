from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_smorest import Api
from flask_smorest.arguments import ArgumentsMixin
from flask_jwt_extended import JWTManager

jwt = JWTManager()
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
webargs = ArgumentsMixin.ARGUMENTS_PARSER
api = Api()

def init_app_extensions(app: Flask):
    """Initialize the extensions with app instance."""
    db.init_app(app)
    api.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    jwt.init_app(app)
    
    @login_manager.user_loader
    def load_user(user_id):
        from .models import User  # Import here to avoid circular import
        return User.query.get(int(user_id))
