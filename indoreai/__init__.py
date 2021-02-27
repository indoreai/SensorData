from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from indoreai.config import Config

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_massage_category = 'info'
mail = Mail()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    with app.app_context():
        from indoreai.users.models import User
        from indoreai.pca.models import Samples, Samples_meta, Samples_userdevices
        # from models import Device, Camera, ROI, EmailAddress, ROI2MailRel, AuditLog, ROI2MailRel
        db.create_all()  # Creat.

    from indoreai.users.routes import users
    from indoreai.api.routes import api
    from indoreai.pca.routes import pca
    from indoreai.errors.handlers import errors
    app.register_blueprint(users)
    app.register_blueprint(api)
    app.register_blueprint(pca)
    app.register_blueprint(errors)
    return app