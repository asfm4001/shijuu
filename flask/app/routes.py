from flask import current_app
from app.forms import *

# 篩選副檔名符合條件的檔案
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config["ALLOWED_EXTENSIONS"]

