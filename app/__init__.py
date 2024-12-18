from flask import Flask, Blueprint
# from flask_bootstrap import Bootstrap
from flask_bootstrap import Bootstrap4  # Bootstrap-Flask 仍使用相同套件名
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
# from flask_wtf.csrf import CSRFProtect
from app.config import config

bootstrap = Bootstrap4()
bcrypt = Bcrypt()
login = LoginManager()
db = SQLAlchemy()

def create_app(configname):
    app = Flask(__name__)
    app.config.from_object(config[configname])
    # csrf = CSRFProtect(app)  # 啟用CSRF保護(非flask form需使用)
    # bootstrap = Bootstrap(app)
    bootstrap = Bootstrap4(app)
    bcrypt = Bcrypt(app)
    login = LoginManager(app)
    db = SQLAlchemy(app)

    # login_required 設定
    login.login_view = "signin"
    login.login_message = "You must login to access this page."
    login.login_message_category = "info"

    # routes
    
    return app