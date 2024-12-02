import os
from dotenv import load_dotenv

load_dotenv()   # 引用.env檔

class Config(object):
    # Database Configuration
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI") or 'sqlite:///data.db'
    # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{}:{}@{}/{}'.format(
    #     os.getenv("MYSQL_USERNAME"),
    #     os.getenv("MYSQL_PASSWORD"),
    #     os.getenv("MYSQL_IP"),
    #     os.getenv("MYSQL_DATABASE")
    # )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv("SECRET_KEY") or 'A_VERY_LONG_SECRET_KEY'    # 給form使用

    # user add porduct image upload_folder
    PRODUCT_IMG_UPLOAD_FOLDER = "app/static/product/items"
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
