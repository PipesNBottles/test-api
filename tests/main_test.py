from fastapi.testclient import TestClient
from shift_service.server import app
import uuid
import datetime

client = TestClient(app)


def test_read_main():
    response = client.get("/ping")
    assert response.status_code == 200
    assert response.json() == {"message": "pong"}


def test_create_users():
    payload_1 = {
        "id": str(uuid.uuid4()),
        "level": 1,
        "email": "Employee@job.com",
        "password": "password",
    }
    payload_2 = {
        "id": str(uuid.uuid4()),
        "level": 2,
        "email": "Boss@job.com",
        "password": "harder_password",
    }
    payload_3 = {
        "id": str(uuid.uuid4()),
        "level": 3,
        "email": "not an email",
        "password": "harder_password",
    }
    response = client.post("/v1/users", json=payload_1)
    payload_1.pop("password")
    assert response.status_code == 200

    response_2 = client.post("/v1/users", json=payload_2)
    assert response_2.status_code == 200
    assert response_2.json()["level"] == payload_2["level"]

    response_3 = client.post("/v1/users", json=payload_3)
    assert response_3.status_code == 422


def test_login():
    form_data = {"username": "employee@job.com", "password": "password"}
    response = client.post("/token", data=form_data)
    assert response.status_code == 200
    assert response.json() == {
        "access_token": form_data["username"],
        "token_type": "bearer",
    }


def test_delete_user_not_auth():
    response = client.get("/v1/users")
    resp_json = response.json()
    param = {"user_id": resp_json[-1]["id"]}
    response = client.delete("/v1/users", params=param)
    assert response.status_code != 200
    assert response.json()["detail"] == "Not authenticated"


def test_delete_user_wrong_level():
    form_data = {"username": "employee@job.com", "password": "password"}
    client.post("/token", data=form_data).json()
    response = client.get("/v1/users")
    resp_json = response.json()
    param = {"user_id": resp_json[-1]["id"]}
    headers = {
        "accept": "application/json",
        "Authorization": f'Bearer {form_data["username"]}',
    }
    response = client.delete("/v1/users", headers=headers, params=param)
    assert response.status_code != 200
    assert response.json()["detail"] == "Not allowed to delete users"


def test_edit_user():
    form_data = {"username": "boss@job.com", "password": "harder_password"}
    client.post("/token", data=form_data).json()
    response = client.get("/v1/users")
    resp_json = response.json()
    param = {"user_id": resp_json[0]["id"]}
    headers = {
        "accept": "application/json",
        "Authorization": f'Bearer {form_data["username"]}',
    }
    payload = {"email": "test@test.com"}
    response = client.put("/v1/users", json=payload, headers=headers, params=param)
    assert response.status_code == 200
    assert response.json()["email"] == "test@test.com"


def test_create_shifts():
    form_data = {"username": "boss@job.com", "password": "harder_password"}
    client.post("/token", data=form_data).json()
    response = client.get("/v1/users")
    resp_json = response.json()
    param = {"user_id": resp_json[0]["id"]}
    headers = {
        "accept": "application/json",
        "Authorization": f'Bearer {form_data["username"]}',
    }
    payload_1 = {
        "start_time": str(datetime.datetime.now()),
        "end_time": str(datetime.datetime.now() + datetime.timedelta(minutes=10)),
    }
    payload_2 = {
        "start_time": str(datetime.datetime.now() - datetime.timedelta(minutes=5)),
        "end_time": str(datetime.datetime.now() + datetime.timedelta(minutes=10)),
    }
    payload_3 = {
        "start_time": str(datetime.datetime.now() + datetime.timedelta(minutes=5)),
        "end_time": str(datetime.datetime.now() + datetime.timedelta(minutes=10)),
    }
    resp_1 = client.post("/v1/shifts", json=payload_1, headers=headers, params=param)
    resp_2 = client.post("/v1/shifts", json=payload_2, headers=headers, params=param)
    resp_3 = client.post("/v1/shifts", json=payload_3, headers=headers, params=param)
    assert resp_1.status_code == 200
    assert resp_2.status_code == 405
    assert resp_3.status_code == 405


def test_edit_shift():
    form_data = {"username": "boss@job.com", "password": "harder_password"}
    client.post("/token", data=form_data).json()
    response = client.get("/v1/users")
    resp_json = response.json()
    param = {"user_id": resp_json[0]["id"]}
    headers = {
        "accept": "application/json",
        "Authorization": f'Bearer {form_data["username"]}',
    }
    payload_1 = {
        "start_time": str(datetime.datetime.now() - datetime.timedelta(minutes=30)),
        "end_time": str(datetime.datetime.now() + datetime.timedelta(minutes=10)),
    }
    resp_1 = client.put("/v1/shifts", json=payload_1, headers=headers, params=param)
    assert resp_1.status_code == 405
