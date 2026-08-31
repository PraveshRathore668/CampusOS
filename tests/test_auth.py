def test_register_new_user(client):
    response = client.post("/api/v1/auth/register", json={
        "email": "teststudent@campus.edu",
        "password": "TestPass123",
        "full_name": "Test Student",
        "role": "STUDENT",
    })
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "teststudent@campus.edu"
    assert "hashed_password" not in data


def test_register_duplicate_email_fails(client):
    client.post("/api/v1/auth/register", json={
        "email": "dupe@campus.edu",
        "password": "TestPass123",
        "full_name": "First User",
        "role": "STUDENT",
    })
    response = client.post("/api/v1/auth/register", json={
        "email": "dupe@campus.edu",
        "password": "AnotherPass123",
        "full_name": "Second User",
        "role": "STUDENT",
    })
    assert response.status_code == 400


def test_login_with_correct_credentials(client):
    client.post("/api/v1/auth/register", json={
        "email": "logintest@campus.edu",
        "password": "CorrectPass123",
        "full_name": "Login Test",
        "role": "STUDENT",
    })
    response = client.post("/api/v1/auth/login", json={
        "email": "logintest@campus.edu",
        "password": "CorrectPass123",
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data


def test_login_with_wrong_password_fails(client):
    client.post("/api/v1/auth/register", json={
        "email": "wrongpass@campus.edu",
        "password": "CorrectPass123",
        "full_name": "Wrong Pass Test",
        "role": "STUDENT",
    })
    response = client.post("/api/v1/auth/login", json={
        "email": "wrongpass@campus.edu",
        "password": "IncorrectPass456",
    })
    assert response.status_code == 401


def test_protected_route_without_token_fails(client):
    response = client.get("/api/v1/auth/me")
    assert response.status_code in (401, 403)


def test_protected_route_with_valid_token_succeeds(client):
    client.post("/api/v1/auth/register", json={
        "email": "metest@campus.edu",
        "password": "TestPass123",
        "full_name": "Me Test",
        "role": "STUDENT",
    })
    login_response = client.post("/api/v1/auth/login", json={
        "email": "metest@campus.edu",
        "password": "TestPass123",
    })
    token = login_response.json()["access_token"]

    response = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    assert response.json()["email"] == "metest@campus.edu"
