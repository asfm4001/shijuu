from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileRequired
from wtforms import (
    StringField,
    SelectField,
    IntegerField, 
    FileField,
    TextAreaField,
    SubmitField,
    PasswordField)
from wtforms.validators import (
    DataRequired, 
    Length, 
    NumberRange, 
    ValidationError, 
    Email,
    EqualTo)
from app.models import *

class AddProductForm(FlaskForm):
    name = StringField("", validators=[DataRequired(), Length(min=2, max=20)])
    category = SelectField("", validators=[DataRequired(), Length(min=4, max=20)], 
                           choices=[("default", "無"),
                                    ("cake", "蛋糕"),
                                    ("milk_roll_cake","生乳捲"),
                                    ("gift_basket","禮盒")])
    price = IntegerField("", validators=[DataRequired(), NumberRange(min=1,max=9999)])
    context = TextAreaField("", validators=[Length(max=200)])
    # img = FileField("", validators=[FileRequired() ,FileAllowed(["jpg", "png"], "僅能上傳jpg, png檔")])
    # FileAllowed 無作用
    img = FileField("", validators=[])
    submit = SubmitField("")
    def validate_name(self, name):  # name 必須與上方的變數名相同
        product = Product.query.filter_by(name=name.data).first()
        if product:
            raise ValidationError("商品名稱已存在")
        
class RegisterForm(FlaskForm):
    username = StringField("帳號", validators=[DataRequired(), Length(min=6, max=20)])
    # 需安裝email_validator
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("密碼", validators=[DataRequired(), Length(min=6, max=20)])
    confirm = PasswordField("確認密碼", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("註冊")

class SigninForm(FlaskForm):
    username = StringField("帳號", validators=[DataRequired(), Length(min=6, max=20)])
    password = PasswordField("密碼", validators=[DataRequired(), Length(min=6, max=20)])
    submit = SubmitField("註冊")
    def validate_name(self, username, password):  # name 必須與上方的變數名相同
        user = Users.query.filter_by(username=username.data).first() 
        if user :
            raise ValidationError("帳號不存在或密碼錯誤")
        
class ReceiverFrom(FlaskForm):
    receiver = StringField("收件人", validators=[DataRequired(), Length(min=2, max=20)])
    phone = StringField("聯絡電話", validators=[DataRequired(), Length(min=10, max=12)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    received_type = SelectField("", validators=[DataRequired()], 
                                choices=[("來店自取", "來店自取"), 
                                         ("宅配", "宅配")])
    address = StringField("地址", validators=[Length(max=50)])
    note = StringField("訂單備註", validators=[Length(max=50)])
    submit = SubmitField("下一步")

class OrderQueryFrom(FlaskForm):
    # email = StringField("Email", validators=[DataRequired(), Email()])
    phone = StringField("聯絡電話", validators=[DataRequired(), Length(min=10, max=12)])
    submit = SubmitField("查詢")