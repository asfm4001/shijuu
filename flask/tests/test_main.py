import pytest
from app import create_app

# 實體化app
app = create_app('test')

# 建立測試client
@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

### main
def test_index(client):
    response = client.get('/')
    assert response.status_code == 200
def test_about(client):
    assert client.get('/about').status_code == 200

### errors
def test_404(client):
    assert client.get('/error_page').status_code == 404