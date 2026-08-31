def register_and_login(client, email, role="STUDENT"):
    client.post("/api/v1/auth/register", json={
        "email": email,
        "password": "TestPass123",
        "full_name": "Test User",
        "role": role,
    })
    response = client.post("/api/v1/auth/login", json={
        "email": email,
        "password": "TestPass123",
    })
    return response.json()["access_token"]


def test_create_ticket_requires_auth(client):
    response = client.post("/api/v1/tickets", json={
        "title": "Broken chair",
        "description": "Chair leg is broken",
        "location": "Room 101",
    })
    assert response.status_code in (401, 403)


def test_create_ticket_auto_classifies(client):
    token = register_and_login(client, "ticketstudent@campus.edu")

    response = client.post(
        "/api/v1/tickets",
        json={
            "title": "Leaking pipe",
            "description": "There is a leaking pipe under the sink in the hostel bathroom",
            "location": "Hostel Block A",
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["status"] == "OPEN"
    assert data["category"] in (
        "IT_EQUIPMENT", "ELECTRICAL", "PLUMBING",
        "FURNITURE", "CLEANING", "OTHER",
    )
    assert data["priority"] in ("LOW", "MEDIUM", "HIGH")


def test_student_only_sees_own_tickets(client):
    token_a = register_and_login(client, "studentA@campus.edu")
    token_b = register_and_login(client, "studentB@campus.edu")

    client.post(
        "/api/v1/tickets",
        json={"title": "A's ticket", "description": "Test description", "location": "Room 1"},
        headers={"Authorization": f"Bearer {token_a}"},
    )
    client.post(
        "/api/v1/tickets",
        json={"title": "B's ticket", "description": "Test description", "location": "Room 2"},
        headers={"Authorization": f"Bearer {token_b}"},
    )

    response = client.get(
        "/api/v1/tickets",
        headers={"Authorization": f"Bearer {token_a}"},
    )
    titles = [t["title"] for t in response.json()]
    assert "A's ticket" in titles
    assert "B's ticket" not in titles


def test_admin_sees_all_tickets(client):
    student_token = register_and_login(client, "studentC@campus.edu")
    admin_token = register_and_login(client, "adminC@campus.edu", role="ADMIN")

    client.post(
        "/api/v1/tickets",
        json={"title": "C's ticket", "description": "Test description", "location": "Room 3"},
        headers={"Authorization": f"Bearer {student_token}"},
    )

    response = client.get(
        "/api/v1/tickets",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    titles = [t["title"] for t in response.json()]
    assert "C's ticket" in titles


def test_student_cannot_update_ticket_status(client):
    token = register_and_login(client, "studentD@campus.edu")

    create_response = client.post(
        "/api/v1/tickets",
        json={"title": "D's ticket", "description": "Test description", "location": "Room 4"},
        headers={"Authorization": f"Bearer {token}"},
    )
    ticket_id = create_response.json()["id"]

    response = client.patch(
        f"/api/v1/tickets/{ticket_id}",
        json={"status": "RESOLVED"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 403


def test_admin_can_update_ticket_status(client):
    student_token = register_and_login(client, "studentE@campus.edu")
    admin_token = register_and_login(client, "adminE@campus.edu", role="ADMIN")

    create_response = client.post(
        "/api/v1/tickets",
        json={"title": "E's ticket", "description": "Test description", "location": "Room 5"},
        headers={"Authorization": f"Bearer {student_token}"},
    )
    ticket_id = create_response.json()["id"]

    response = client.patch(
        f"/api/v1/tickets/{ticket_id}",
        json={"status": "IN_PROGRESS"},
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 200
    assert response.json()["status"] == "IN_PROGRESS"
