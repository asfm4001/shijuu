import os
from flask import render_template, flash, redirect, url_for, session, request, jsonify, make_response
from flask_login import current_user, login_user, login_required, logout_user
from app import a
from app.models import Product, User
from app.forms import *

# 篩選副檔名符合條件的檔案
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config["ALLOWED_EXTENSIONS"]

