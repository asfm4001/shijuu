from . import orders_bp
from flask import render_template, redirect, url_for, request, flash
from flask_login import current_user
from app.models import *
from app.forms import *

### 訂單查詢(all) ###
@orders_bp.route("/all", methods=["GET", "POST"])
def orders():
    try:
        if current_user.is_admin == True:
            orders = Order.query.order_by(Order.id.desc()).all()
            return render_template("order_page.html", orders=orders)
    except:
        return render_template("order_page.html", orders=orders)

### 訂單查詢頁面 ###
@orders_bp.route("/query", methods=["GET", "POST"])
def order_query():
    form = OrderQueryFrom()
    if current_user.is_authenticated and current_user.is_admin:
        return redirect(url_for("orders.orders"))
    if form.validate_on_submit():
        phone = form.phone.data
        # email = form.email.data
        orders = Order.query.filter_by(phone=phone).all()
        print(orders)
        return render_template("order_page.html", orders=orders)
    return render_template("order_query.html", form=form)

### 訂單修改 ###
@orders_bp.route("/update/<int:order_id>", methods=["POST"])
def order_update(order_id):
    if current_user.is_admin == False:
        return "無權訪問", 403
    order = Order.query.filter_by(id=order_id).first()
    order.receiver = request.form.get("receiver")
    order.phone = request.form.get("phone")
    order.received_type = request.form.get("received_type")
    if order.received_type == "來店自取":
        order.address = "宜蘭縣羅東鎮天祥路78號"
    else:
        order.address = request.form.get("address")
    order.payment_status = request.form.get("payment_status")
    order.status = request.form.get("status")
    db.session.commit()
    return redirect(url_for("orders.orders"))

### 訂單刪除 ###
@orders_bp.route("/delete/<int:order_id>", methods=["POST"])
def order_delete(order_id):
    if current_user.is_admin == False:
        return "無權訪問", 403
    order = Order.query.filter_by(id=order_id).first()
    order.cleanOrder()
    db.session.delete(order)
    db.session.commit()
    flash("已刪除", category="success")
    return redirect(url_for("orders.orders"))
