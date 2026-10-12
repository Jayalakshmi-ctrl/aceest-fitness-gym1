import pytest
from app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_api_metadata_index(client):
    """Verifies operational metadata metrics output on the base route."""
    response = client.get('/')
    assert response.status_code == 200
    data = response.get_json()
    assert "ACEest FUNCTIONAL FITNESS" in data["message"]
    assert data["metrics"]["capacity"] == "150 Users"

def test_list_programs_endpoint(client):
    """Ensures keys exist matching the underlying operational domains."""
    response = client.get('/api/programs')
    assert response.status_code == 200
    data = response.get_json()
    assert "Fat Loss (FL)" in data["programs"]
    assert "Muscle Gain (MG)" in data["programs"]

def test_get_valid_program_details(client):
    """Validates structure metrics match expected target profiles."""
    response = client.get('/api/programs/Fat Loss (FL)')
    assert response.status_code == 200
    data = response.get_json()
    assert "AMRAP" in data["details"]["workout"]
    assert "2,000 kcal" in data["details"]["diet"]

def test_get_invalid_program_handling(client):
    """Validates fallback validation handling returns clean 404 states."""
    response = client.get('/api/programs/NonExistentPlan')
    assert response.status_code == 404
    data = response.get_json()
    assert data["status"] == "error"
