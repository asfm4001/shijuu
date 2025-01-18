import pytest
from app import create_app
from app.models import Product

# 實體化app
app = create_app('test')

# 建立測試client
@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

### api_v1
def test_products_all(client):
    response = client.get('/api/v1/products/all')
    assert response.status_code == 200

    json_data = response.get_json()     # 取得json格式
    assert json_data['stat'] == 'ok'

    p_id = json_data['data'][0][0]
    p_name = json_data['data'][0][1]
    assert p_name == Product.query.filter_by(id=p_id).first().name