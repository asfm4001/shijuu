import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__)) # 當前檔案絕對路徑, __file__: 當前檔案(config.py)
load_dotenv()   # 引用.env檔

class Config():
    # Database Configuration
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv("SECRET_KEY") or 'A_VERY_LONG_SECRET_KEY'    # 給form使用

    # user add image of porduct upload_folder
    PRODUCT_IMG_UPLOAD_FOLDER = "app/static/product/items"
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv("DEV_DATABASE_URL") or \
        'sqlite:///' + os.path.join(basedir, 'instance', 'devp-data.sqlite')
    
class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'instance', 'test-data.sqlite')
    
class ProductionConfig(Config):
    DEBUG = False
    FLASK_RUN_HOST = "0.0.0.0"
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'mysql+pymysql://{}:{}@{}/{}'.format(
            os.getenv("MYSQL_USERNAME"),
            os.getenv("MYSQL_PASSWORD"),
            os.getenv("MYSQL_IP"),
            os.getenv("MYSQL_DATABASE")
        )
    
config = {
'devp': DevelopmentConfig,
'test': TestingConfig,
'prod': ProductionConfig,
'default': DevelopmentConfig
}