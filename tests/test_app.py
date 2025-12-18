import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "Programming Class" in data

def test_signup_for_activity_success():
    response = client.post("/activities/Chess Club/signup?email=tester@mergington.edu")
    assert response.status_code == 200 or response.status_code == 400  # Already signed up or success
    # If successful, participant should be in the list
    activities = client.get("/activities").json()
    assert "tester@mergington.edu" in activities["Chess Club"]["participants"]

def test_signup_for_activity_not_found():
    response = client.post("/activities/Nonexistent/signup?email=someone@mergington.edu")
    assert response.status_code == 404

def test_signup_duplicate():
    email = "duplicate@mergington.edu"
    # First signup
    client.post(f"/activities/Gym Class/signup?email={email}")
    # Second signup should fail
    response = client.post(f"/activities/Gym Class/signup?email={email}")
    assert response.status_code == 400

def test_unregister_participant():
    # Add then remove
    email = "remove@mergington.edu"
    client.post(f"/activities/Programming Class/signup?email={email}")
    response = client.post(f"/activities/Programming Class/unregister?email={email}")
    assert response.status_code == 200
    activities = client.get("/activities").json()
    assert email not in activities["Programming Class"]["participants"]
