import os
from flask import render_template, redirect, flash, url_for, current_app
from flask_login import current_user
from app import db
from app.forms import AddProductForm
from app.models import Product
from . import products_bp

# 篩選副檔名符合條件的檔案
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config["ALLOWED_EXTENSIONS"]

@products_bp.route("/all", methods=["GET", "POST"])
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
            img.save(os.path.join(current_app.config["PRODUCT_IMG_UPLOAD_FOLDER"], filename))
            img_path = os.path.join("/", "static", "product", "items", filename)
        new_product = Product(name=name, category=category, price=price, context=context, img=img_path)
        db.session.add(new_product)
        db.session.commit()
        flash("您的商品已成功新增!!", category="success")
        return redirect(url_for("products.products_all"))
    products = Product.query.order_by(Product.id.desc())
    return render_template("product_page.html", form=form, products=products)

### 商品查詢(item) ###
@products_bp.route("/items/<int:product_id>", methods=["GET", "POST"])
def products(product_id):
    # products = [Product.query.filter_by(id=product_id).first()] # 僅只有一個物件時也要加入陣列
    product = Product.query.filter_by(id=product_id).first()
    return render_template("product.html", product=product)

### 商品查詢(category) ###
@products_bp.route("/items/categorys/<category>", methods=["GET", "POST"])
def products_categorys(category):
    products = Product.query.filter_by(category=category)
    if category == "cake": category_name = "蛋糕"
    if category == "milk_roll_cake": category_name = "生乳捲"
    if category == "gift_basket": category_name = "禮盒"
    return render_template("product_page.html", products=products, category_name=category_name)

### 商品刪除 ###
@products_bp.route("/items/delete/<int:product_id>", methods=["GET", "POST"])
def delete_product(product_id):
    product = Product.query.filter_by(id=product_id).first()
    if product:
        db.session.delete(product)
        db.session.commit()
        flash("商品已刪除!!", category="danger")
        redirect(url_for("products.products_all"))
    return redirect(url_for("products.products_all"))

### 商品修改 ###
@products_bp.route("/items/update/<int:product_id>", methods=["GET", "POST"])
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
        img.save(os.path.join(config["PRODUCT_IMG_UPLOAD_FOLDER"], filename))
        img_path = os.path.join("/", "static", "product", "items", filename)
        product.img = img_path
    db.session.commit()
    flash("您的商品已成功修改!!", category="success")
    return redirect(url_for("products.products_all"))
