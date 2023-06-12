import requests
import pytest
import allure
from datetime import datetime

base_url = "http://restapi.adequateshop.com"
rid = datetime.now().strftime("%Y%m%d%H%M%S")  # random id


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
        "tourist_name": f"user{rid}",
        "tourist_email": f"email{rid}@email.com",
        "tourist_location": "neverland",
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
        "email": "incorrect_username",
        "password": "incorrect_password"
    }
    response = requests.post(url, json=payload)
    assert response.status_code == 200
    assert response.json()["code"] == 1
    assert response.json()["message"] == "invalid username or password"
    assert response.json()["data"] is None


@allure.title("Login - Empty Credentials")
def test_login_empty_credentials():
    url = base_url + "/api/AuthAccount/Login"
    payload = {
        "email": "",
        "password": ""
    }
    response = requests.post(url, json=payload)
    assert response.status_code == 400
    response_json = response.json()
    assert response_json["Message"] == "The request is invalid."
    assert response_json["ModelState"]["log.email"] == ["field is required"]
    assert response_json["ModelState"]["log.password"] == ["field is required"]


@allure.title("Get Tourist by ID - Successful")
def test_get_tourist_successful(create_tourist):
    tourist_id = create_tourist
    get_url = base_url + f"/api/Tourist/{tourist_id}"
    with allure.step(f"Get tourist with ID: {tourist_id}"):
        response = requests.get(get_url)
    assert response.status_code == 200
    assert response.json()["id"] == tourist_id
    assert response.json()["tourist_name"] == f"user{rid}"
    assert response.json()["tourist_email"] == f"email{rid}@email.com"
    assert response.json()["tourist_location"] == "neverland"


@allure.title("Get Tourist by ID - Tourist Not Found")
def test_get_tourist_not_found():
    tourist_id = "non_existing_id"
    get_url = base_url + f"/api/Tourist/{tourist_id}"
    with allure.step(f"Get tourist with ID: {tourist_id}"):
        response = requests.get(get_url)
    assert response.status_code == 400
    assert response.json()["Message"] == "The request is invalid."
