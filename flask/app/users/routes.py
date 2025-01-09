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
        password = bcrypt.generate_password_hash(form.password.data).decode('UTF-8')
        if Users.query.filter_by(username=username).first():
            flash('此帳號已被使用，請改使用其他帳號', category='warning')
            return render_template('register.html', form=form)
        if Users.query.filter_by(email=email).first():
            flash('此信箱已被使用，請改使用其他信箱。', category='warning')
            return render_template('register.html', form=form)
        user = Users(username=username, email=email, password=password, is_admin=False)
        db.session.add(user)
        db.session.commit()
        if not user.cart:
            cart = Cart(user_id=user.id)
            db.session.add(cart)
            db.session.commit()
        flash("註冊成功!!", category="success")
        return redirect(url_for("users.signin"))
    return render_template("register.html", form=form)

### 登入 ###
@users_bp.route("/signin", methods=["GET", "POST"])
def signin():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))
    form = SigninForm()
    username = form.username.data
    password = form.password.data
    user = Users.query.filter_by(username=username).first()
    if form.validate_on_submit():
        if user and bcrypt.check_password_hash(user.password.encode('UTF-8'), password):
            login_user(user)
            session["username"] = user.username
            flash("歡迎回來", category="success")
            return redirect(url_for("main.index"))
        else:
            flash("error", category="danger")
            return redirect(url_for("main.index"))
    return render_template("sign-in.html", form=form)

### 登出 ###
@users_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("users.signin"))

@users_bp.route('/testpage1')
def testpage():
    return "Hello"

@users_bp.route('/turntotestpage1/<name>')
def turntotestpage1(name):
    if name == 'leo':
        return redirect(url_for('users.testpage'))
    return "error name"