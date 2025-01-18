from . import api_v1_bp
from flask import jsonify
from app.models import Product
from datetime import datetime

# all product
@api_v1_bp.route("products/all")
def porducts_all():
    products = Product.query.all()

    # Product to list.
    product_list = []
    if products:
        for i in products:
            d = []
            d.append(i.id)
            d.append(i.name)
            d.append(i.category)
            d.append(i.price)
            d.append(i.context)
            product_list.append(d)
        
        data = {
            'stat': 'ok',
            'time': datetime.today().strftime('%Y-%m-%d %H:%M'),
            'fields': ['id', '產品名稱', '分類', '價格', '產品描述'],
            'data': product_list
        }
    else:
        data = {
            'stat': 'not fount',
            'time': datetime.today().strftime('%Y-%m-%d %H:%M'),
        }
    return jsonify(data)