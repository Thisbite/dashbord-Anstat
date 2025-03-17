# tests/test_app.py
import sys
import os

# Ajoute le répertoire racine au chemin de recherche
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_births_data(client):
    response = client.get('/births_data')
    print(f"Statut: {response.status_code}")
    print(f"Réponse JSON: {response.json}")
    assert response.status_code == 200
    assert 'total_births' in response.json
    assert isinstance(response.json['total_births'], (int, float))