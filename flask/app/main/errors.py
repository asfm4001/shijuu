from . import main_bp
from flask import render_template

@main_bp.app_errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@main_bp.app_errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 500