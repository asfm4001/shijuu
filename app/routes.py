import os
from flask import render_template, flash, redirect, url_for, session, request, jsonify, make_response
from flask_login import current_user, login_user, login_required, logout_user
from app import app, db, bcrypt
from app.models import Product, User
from app.forms import *

# 篩選副檔名符合條件的檔案
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config["ALLOWED_EXTENSIONS"]

### 首頁 ###
@app.route("/", methods=["GET"])
def index():
    # if "username" in session:
    #     # flash(f"Logged in as {session['username']}", category="success")
    #     print(session)
    # flash(current_user, category="success")
    resp = make_response(render_template("index.html"))
    # resp.set_cookie('user_id', '234')
    # flash(request.cookies.get('user_id'), category="success")
    return resp

### 商品查詢(all) ###
@app.route("/products/all", methods=["GET", "POST"])
def products_all():
    form = AddProductForm()
    if form.validate_on_submit() and current_user.is_admin == True:
        name = form.name.data
        category = form.category.data
        price = form.price.data
        context = form.context.data
        img = form.img.data
        if img.filename == "":
            img_path = os.path.join("/", "static", "product", "default.png")
        if img and allowed_file(img.filename):  # 以商品名稱重新命名img.filename
            filename = name + os.path.splitext(img.filename)[1]
                # splitext, ("檔名", "副檔名")
            img.save(os.path.join(app.config["PRODUCT_IMG_UPLOAD_FOLDER"], filename))
            img_path = os.path.join("/", "static", "product", "items", filename)
        new_product = Product(name=name, category=category, price=price, context=context, img=img_path)
        db.session.add(new_product)
        db.session.commit()
        flash("您的商品已成功新增!!", category="success")
        return redirect(url_for("products_all"))
    products = Product.query.order_by(Product.id.desc())
    return render_template("product/product_page.html", form=form, products=products)

### 商品查詢(item) ###
@app.route("/products/items/<int:product_id>", methods=["GET", "POST"])
def products(product_id):
    # products = [Product.query.filter_by(id=product_id).first()] # 僅只有一個物件時也要加入陣列
    product = Product.query.filter_by(id=product_id).first()
    return render_template("product/product.html", product=product)

### 商品查詢(category) ###
@app.route("/products/items/categorys/<category>", methods=["GET", "POST"])
def products_categorys(category):
    products = Product.query.filter_by(category=category)
    if category == "cake": category_name = "蛋糕"
    if category == "milk_roll_cake": category_name = "生乳捲"
    if category == "gift_basket": category_name = "禮盒"
    return render_template("product/product_page.html", products=products, category_name=category_name)

### 商品刪除 ###
@app.route("/products/items/delete/<int:product_id>", methods=["GET", "POST"])
def delete_product(product_id):
    product = Product.query.filter_by(id=product_id).first()
    if product:
        db.session.delete(product)
        db.session.commit()
        flash("商品已刪除!!", category="danger")
        redirect(url_for("products_all"))
    return redirect(url_for("products_all"))

### 商品修改 ###
@app.route("/products/items/update/<int:product_id>", methods=["GET", "POST"])
def update_product(product_id):
    form = AddProductForm()
    product = Product.query.filter_by(id=product_id).first()
    product.name = form.name.data
    product.category = form.category.data
    product.price = form.price.data
    product.context = form.context.data
    img = form.img.data
    if img and allowed_file(img.filename):  # 以商品名稱重新命名img.filename
        filename = product.name + os.path.splitext(img.filename)[1]
            # splitext, ("檔名", "副檔名")
        img.save(os.path.join(app.config["PRODUCT_IMG_UPLOAD_FOLDER"], filename))
        img_path = os.path.join("/", "static", "product", "items", filename)
        product.img = img_path
    db.session.commit()
    flash("您的商品已成功修改!!", category="success")
    return redirect(url_for("products_all"))

### 購物車新增 ###
@app.route("/addcart/items/<int:cart_id>/<int:product_id>", methods=["GET", "POST"])
def add_cart(cart_id, product_id):
    cart = Cart.query.filter_by(id=cart_id).first()
    product = Product.query.filter_by(id=product_id).first()
    cart.addToCart(product)
    db.session.commit()
    return redirect(request.referrer)   # 返回當前頁面

### 購物車刪除 ###
@app.route("/minuscart/items/<int:cart_id>/<int:product_id>", methods=["GET", "POST"])
def minus_cart(cart_id, product_id):
    cart = Cart.query.filter_by(id=cart_id).first()
    product = Product.query.filter_by(id=product_id).first()
    cart.minusToCart(product)
    db.session.commit()
    return redirect(request.referrer)   # 返回當前頁面

### 關於 ###
@app.route("/about", methods=["GET"])
def about():
    return render_template("about.html")

### 註冊 ###
@app.route("/register", methods=["GET", "POST"])
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
    return render_template("user/register.html", form=form)

### 登入 ###
@app.route("/signin", methods=["GET", "POST"])
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
    return render_template("user/sign-in.html", form=form)

### 登出 ###
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("signin"))

### 訂單查詢(all) ###
@app.route("/orders/all", methods=["GET", "POST"])
def orders():
    try:
        if current_user.is_admin == True:
            orders = Order.query.order_by(Order.id.desc()).all()
            return render_template("order/order_page.html", orders=orders)
    except:
        return "無權訪問", 403

### 訂單查詢頁面 ###
@app.route("/orders/query", methods=["GET", "POST"])
def order_query():
    try: 
        if current_user.is_admin == True:
            return redirect(url_for("orders"))
    except:
        form = OrderQueryFrom()
        if form.is_submitted():
            if form.validate_on_submit():
                phone = form.phone.data
                # email = form.email.data
                orders = Order.query.filter_by(phone=phone).all()
                print(orders)
                return render_template("order/order_page.html", orders=orders)
            else:
                flash("查無資料或資料有誤", category="danger")
        return render_template("order/order_query.html", form=form)

### 訂單修改 ###
@app.route("/orders/update/<int:order_id>", methods=["POST"])
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
    return redirect(url_for("orders"))

### 訂單刪除 ###
@app.route("/orders/delete/<int:order_id>", methods=["POST"])
def order_delete(order_id):
    if current_user.is_admin == False:
        return "無權訪問", 403
    order = Order.query.filter_by(id=order_id).first()
    order.cleanOrder()
    db.session.delete(order)
    db.session.commit()
    flash("已刪除", category="success")
    return redirect(url_for("orders"))

### 購物車確認 ###
@app.route("/products/checkout/details", methods=["GET", "POST"])
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
        return redirect(url_for('checkout_payment'))
    if form.errors:
        flash(form.errors, category="danger")
    if current_user.cart:
        total_amount = 0
        for i in current_user.cart.cart_products:
            total_amount += (i.product.price * i.quantity)
    return render_template("checkout/details.html", form=form, total_amount=total_amount)

### 購物車結帳 ###
@app.route("/products/checkout/payment", methods=["GET", "POST"])
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
    return render_template("checkout/payment.html", form=form, total_amount=total_amount)