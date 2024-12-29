from flask import Flask
from flask_bootstrap import Bootstrap4  # Bootstrap-Flask 仍使用相同套件名
# from flask_wtf.csrf import CSRFProtect
from config import config
from app.models import db, login, bcrypt
from .main import main_bp
from .products import products_bp
from .orders import orders_bp
from .users import users_bp
from .cart import cart_bp

bootstrap = Bootstrap4()

def create_app(configname=None):
    app = Flask(__name__)
    if configname == None:
        configname = 'default'
    app.config.from_object(config[configname])
    
    bootstrap.init_app(app)
    db.init_app(app)
    login.init_app(app)
    bcrypt.init_app(app)
    # csrf = CSRFProtect(app)  # 啟用CSRF保護(非flask form需使用)

    # login_required 設定
    login.login_view = "signin"
    login.login_message = "You must login to access this page."
    login.login_message_category = "info"

    # create db
    with app.app_context():
        db.create_all()

    ### routes, blueprint
    app.register_blueprint(main_bp)
    app.register_blueprint(products_bp, url_prefix='/products') 
    app.register_blueprint(orders_bp, url_prefix='/orders') 
    app.register_blueprint(users_bp)
    app.register_blueprint(cart_bp)

    ### shell context
    # from app.models import User, Product, Cart, Order
    # @app.shell_context_processor
    # def make_shell_context():
    #     return dict(db=db, User=User, Product=Product, Cart=Cart, Order=Order)
    
    return app