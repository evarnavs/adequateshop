import requests
import pytest
import allure

base_url = "http://restapi.adequateshop.com"


@pytest.fixture
def login_data():
    return {
        "email": "fleet@example.com",
        "password": "12345"
    }


@pytest.fixture
def create_tourist():
    create_url = base_url + "/api/Tourist"
    create_payload = {
        "tourist_name": "string",
        "tourist_email": "string123",
        "tourist_location": "string",
        "createdat": "2023-06-11T15:59:58.024Z"
    }
    response = requests.post(create_url, json=create_payload)
    tourist_id = response.json()["id"]
    yield tourist_id
    # Clean up the created tourist
    delete_url = base_url + f"/api/Tourist/{tourist_id}"
    requests.delete(delete_url)


@allure.title("Login - Successful")
def test_login_successful(login_data):
    url = base_url + "/api/AuthAccount/Login"
    response = requests.post(url, json=login_data)
    assert response.status_code == 200
    # Add additional assertions for the response body as needed


@allure.title("Login - Incorrect Credentials")
def test_login_incorrect_credentials():
    url = base_url + "/api/AuthAccount/Login"
    payload = {
        "username": "incorrect_username",
        "password": "incorrect_password"
    }
    response = requests.post(url, json=payload)
    assert response.status_code == 401


@allure.title("Login - Empty Credentials")
def test_login_empty_credentials():
    url = base_url + "/api/AuthAccount/Login"
    payload = {
        "username": "",
        "password": ""
    }
    response = requests.post(url, json=payload)
    assert response.status_code == 400


@allure.title("Delete Tourist - Successful")
def test_delete_tourist_successful(create_tourist):
    tourist_id = create_tourist
    delete_url = base_url + f"/api/Tourist/{tourist_id}"
    response = requests.delete(delete_url)
    assert response.status_code == 200


@allure.title("Delete Tourist - Deleting Same Tourist Twice")
def test_delete_tourist_twice(create_tourist):
    tourist_id = create_tourist
    delete_url = base_url + f"/api/Tourist/{tourist_id}"
    # Delete the tourist for the first time
    response = requests.delete(delete_url)
    assert response.status_code == 200
    # Try to delete the same tourist again
    response = requests.delete(delete_url)
    assert response.status_code == 404  # Assuming 404 is returned for non-existing tourist


@allure.title("Delete Tourist - Non-existing Tourist")
def test_delete_non_existing_tourist():
    tourist_id = "non_existing_id"
    delete_url = base_url + f"/api/Tourist/{tourist_id}"
    response = requests.delete(delete_url)
    assert response.status_code == 404

