from flask import Flask
# from flask_bootstrap import Bootstrap
from flask_bootstrap import Bootstrap4  # Bootstrap-Flask 仍使用相同套件名
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
# from flask_wtf.csrf import CSRFProtect
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
# csrf = CSRFProtect(app)  # 啟用CSRF保護(非flask form需使用)
# bootstrap = Bootstrap(app)
bootstrap = Bootstrap4(app)
bcrypt = Bcrypt(app)
login = LoginManager(app)
db = SQLAlchemy(app)

from app.routes import *