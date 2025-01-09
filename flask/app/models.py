from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin
from flask_bcrypt import Bcrypt
from datetime import datetime

db = SQLAlchemy()
login = LoginManager()
bcrypt = Bcrypt()


@login.user_loader
def load_user(user_id):
    return Users.query.filter_by(id=user_id).first()

# Cart(1) <-> CartProduct <-> Product(n)
class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id",))
    user = db.relationship("Users", back_populates="cart")
    cart_products = db.relationship("CartProduct", back_populates="cart")

    ### 輸出(Boolen, index)
    def checkProduct(self, product):
        for index, i in enumerate(self.cart_products):
            if i.product == product:
                return True, index
        else:
            return False, -1
    ### 若product在cart則quantity+=1, 否則加入cart
    def addToCart(self, product):
        result, index = self.checkProduct(product)
        if result:
            self.cart_products[index].quantity += 1
        else:
            addCart = CartProduct(cart_id=self.id, product_id=product.id)
            self.cart_products.append(addCart)
    ### 若product在cart 且 quantity >= 2
    def minusToCart(self, product):
        result, index = self.checkProduct(product)
        if result and self.cart_products[index].quantity >= 2:
            self.cart_products[index].quantity -= 1
        else:
            db.session.delete(self.cart_products[index])
    ### 清除cart_products
    def cleanCartProducts(self):
        for cp in self.cart_products:
            db.session.delete(cp)
            db.session.commit()


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True, nullable=False)
    category = db.Column(db.String(20), default="default", nullable=False)
    price = db.Column(db.Integer, default=1, nullable=False)
    img = db.Column(db.String(120), default="/static/product/default.png", nullable=False)
    context = db.Column(db.String(200), default=" ")
    cart_products = db.relationship("CartProduct", back_populates="product")
    order_products = db.relationship("OrderProduct", back_populates="product")
    def __repr__(self):
        return f'<Product {self.name}>'

### User(1) <-> Cart(1), uselist=Fasle
### User(1) <-> Order(n)
class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)    #20->255, 儲存至mysql時需擴充欄位大小
    is_admin = db.Column(db.Boolean, default=False, nullable=False)
    cart = db.relationship("Cart", uselist=False, back_populates="user")
    orders = db.relationship("Order", backref=db.backref("owner", lazy=True))
    def __repr__(self):
        return f'<Users {self.username}>'

# Order(n) <-> OrderProduct <-> Product(n)
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    # user = db.relationship("User", back_populates="orders")
    order_products = db.relationship("OrderProduct", back_populates="order")

    total_amount = db.Column(db.Integer, default=1, nullable=False)         # 訂單總金額
    receiver = db.Column(db.String(20), nullable=False)                     # 收件人姓名
    received_type = db.Column(db.String(10), default="來店自取")             # 收件種類(自取, 宅配)
    address = db.Column(db.String(100))
    phone = db.Column(db.String(11))
    status = db.Column(db.String(20), default="確認中")                    
    payment_status = db.Column(db.String(20), default="未付款")           # 訂單付款狀態
    created_time = db.Column(db.DateTime, default=datetime.now())        # 訂單成立時間
    updated_time = db.Column(db.DateTime, default=datetime.now())        # 訂單異動時間
    note = db.Column(db.String(50))
    # canceled_time = db.Column(db.DateTime)
    
    ### 計算並設定total_amount
    def setTotalAmount(self):
        self.total_amount = 0
        for op in self.order_products:
            self.total_amount += (op.product.price * op.quantity)
    def turnCartToOrder(self, cart):
        for cp in cart:
            op = OrderProduct(
                order_id = self.id,
                product_id = cp.product.id,
                quantity = cp.quantity
            )
            db.session.add(op)
            db.session.commit()
    def cleanOrder(slef):
        for op in slef.order_products:
            db.session.delete(op)
            db.session.commit()

### Cart(n) <- CartProduct -> Product(n)
class CartProduct(db.Model):
    __tablename__ = "cart_product"
    cart_id = db.Column(db.Integer, db.ForeignKey("cart.id"), primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"), primary_key=True)
    quantity = db.Column(db.Integer, default=1, nullable=False)
    cart = db.relationship("Cart", back_populates="cart_products")
    product = db.relationship("Product", back_populates="cart_products")
    def __repr__(self):
        return f'<CartProduct {self.product_id}, {self.quantity}>'

### Order(n) <- OrderProduct -> Prodcut(n)
class OrderProduct(db.Model):
    __tablename__ = "order_product"
    order_id = db.Column(db.Integer, db.ForeignKey("order.id"), primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"), primary_key=True)
    quantity = db.Column(db.Integer, default=1, nullable=False)
    order = db.relationship("Order", back_populates="order_products")
    product = db.relationship("Product", back_populates="order_products")
    def __repr__(self):
        return f'<OrderProduct {self.product_id}, {self.quantity}>'  
