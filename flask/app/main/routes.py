from . import main_bp
from flask import make_response, render_template

### 首頁 ###
@main_bp.route("/")
def index():
    # if "username" in session:
    #     # flash(f"Logged in as {session['username']}", category="success")
    #     print(session)
    # flash(current_user, category="success")
    resp = make_response(render_template("index.html"))
    # resp.set_cookie('user_id', '234')
    # flash(request.cookies.get('user_id'), category="success")
    return resp

### 關於 ###
@main_bp.route("/about")
def about():
    return render_template("about.html")

