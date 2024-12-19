from . import cart_bp
from flask import redirect, request, session, flash, url_for,render_template
from flask_login import current_user
from app import db
from app.models import Cart, Product, Order
from app.forms import ReceiverFrom

### 購物車新增 ###
@cart_bp.route("/addcart/items/<int:cart_id>/<int:product_id>", methods=["GET", "POST"])
def add_cart(cart_id, product_id):
    cart = Cart.query.filter_by(id=cart_id).first()
    product = Product.query.filter_by(id=product_id).first()
    cart.addToCart(product)
    db.session.commit()
    return redirect(request.referrer)   # 返回當前頁面

### 購物車刪除 ###
@cart_bp.route("/minuscart/items/<int:cart_id>/<int:product_id>", methods=["GET", "POST"])
def minus_cart(cart_id, product_id):
    cart = Cart.query.filter_by(id=cart_id).first()
    product = Product.query.filter_by(id=product_id).first()
    cart.minusToCart(product)
    db.session.commit()
    return redirect(request.referrer)   # 返回當前頁面

### 購物車確認 ###
@cart_bp.route("/checkout/details", methods=["GET", "POST"])
def checkout_details():
    form = ReceiverFrom()
    if form.validate_on_submit():
        session["receiver"] = form.receiver.data
        session["phone"] = form.phone.data
        session["email"] = form.email.data
        session["received_type"] = form.received_type.data
        if form.received_type.data == "來店自取":
            session["address"] = "宜蘭縣羅東鎮天祥路78號"
        else: 
            session["address"] = form.address.data
        return redirect(url_for('cart.checkout_payment'))
    if form.errors:
        flash(form.errors, category="danger")
    if current_user.cart:
        total_amount = 0
        for i in current_user.cart.cart_products:
            total_amount += (i.product.price * i.quantity)
    return render_template("details.html", form=form, total_amount=total_amount)

### 購物車結帳 ###
@cart_bp.route("/checkout/payment", methods=["GET", "POST"])
def checkout_payment():
    total_amount = 0
    for cp in current_user.cart.cart_products:
        total_amount += (cp.product.price * cp.quantity)
    form = ReceiverFrom()
    if form.validate_on_submit():
        email = session["email"]
        order = Order(
            user_id = current_user.id,
            receiver = form.receiver.data,
            received_type = form.received_type.data,
            address = form.address.data,
            phone = form.phone.data,
            note = form.note.data
        )
        db.session.add(order)
        db.session.commit()
        # 判斷當前order
        order.turnCartToOrder(current_user.cart.cart_products)
        order.setTotalAmount()
        db.session.commit()
        order.owner.cart.cleanCartProducts()
        flash("訂單已成立", category="success")
        return redirect(url_for("index"))
    return render_template("payment.html", form=form, total_amount=total_amount)