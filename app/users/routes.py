from . import users_bp
from flask import redirect, flash, render_template, url_for, session
from flask_login import current_user, login_user, logout_user, login_required
from app.forms import *

### 註冊 ###
@users_bp.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = bcrypt.generate_password_hash(form.password.data)
        user = User(username=username, email=email, password=password, is_admin=False)
        db.session.add(user)
        db.session.commit()
        if not user.cart:
            cart = Cart(user_id=user.id)
            db.session.add(cart)
            db.session.commit()
        flash("註冊成功!!", category="success")
        return redirect(url_for("signin"))
    return render_template("users.register.html", form=form)

### 登入 ###
@users_bp.route("/signin", methods=["GET", "POST"])
def signin():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = SigninForm()
    username = form.username.data
    password = form.password.data
    user = User.query.filter_by(username=username).first()
    if form.validate_on_submit():
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            session["username"] = user.username
            flash("歡迎回來", category="success")
            return redirect(url_for("index"))
        flash("找不到使用者或密碼錯誤", category="danger")
    return render_template("sign-in.html", form=form)

### 登出 ###
@users_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("users.signin"))
