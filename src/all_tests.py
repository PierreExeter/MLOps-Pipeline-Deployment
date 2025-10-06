import pytest
import os
from app import app
from train_model import train_model

"""
USAGE : 
pytest src/all_tests.py -v
"""

def test_model_binary_created():
    """
    Test that the model binary file is created successfully
    after the train_model() function is called
    """
    
    model_path = 'model/pycaret-model.pkl'
    
    # Ensure any existing test file is removed
    if os.path.exists(model_path):
        os.remove(model_path)
    
    # Train and save model
    train_model()
    
    # Check if the model binary was created
    assert os.path.exists(model_path), f"Model file {model_path} was not created"
    

@pytest.fixture
def client():
    """Create a test client for the app"""
    with app.test_client() as client:
        yield client


def test_home_route(client):
    """Test the home page route"""
    response = client.get('/')
    assert response.status_code == 200
    assert b'home.html' in response.data or response.data  # Basic check that page loads


def test_predict_route_post(client):
    """Test the predict route with POST data"""
    # Sample form data that matches the expected columns
    form_data = {
        'age': '25',
        'sex': 'male', 
        'bmi': '22.5',
        'children': '0',
        'smoker': 'no',
        'region': 'southwest'
    }
    
    response = client.post('/predict', data=form_data)
    assert response.status_code == 200
    # Check that we get some prediction response
    assert b'bill' in response.data.lower() or b'$' in response.data


def test_predict_api_route(client):
    """Test the API predict route with JSON data"""
    # Sample JSON data
    json_data = {
        'age': 25,
        'sex': 'male',
        'bmi': 22.5,
        'children': 0,
        'smoker': 'no',
        'region': 'southwest'
    }
    
    response = client.post('/predict_api', json=json_data)
    assert response.status_code == 200
    # Check that we get a JSON response with a number
    assert response.is_json
    data = response.get_json()
    assert isinstance(data, int)  # Should return an integer


def test_predict_route_get(client):
    """Test that predict route returns error for GET requests"""
    response = client.get('/predict')
    # Should return 405 Method Not Allowed or handle GET appropriately
    assert response.status_code != 200  # Should not be successful with GET
    
