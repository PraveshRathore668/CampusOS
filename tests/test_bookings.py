from app.models.booking import Resource, ResourceTypeEnum


def register_and_login(client, email):
    client.post("/api/v1/auth/register", json={
        "email": email,
        "password": "TestPass123",
        "full_name": "Test User",
        "role": "STUDENT",
    })
    response = client.post("/api/v1/auth/login", json={
        "email": email,
        "password": "TestPass123",
    })
    return response.json()["access_token"]


def seed_resource(db_session):
    resource = Resource(name="Test Lab", resource_type=ResourceTypeEnum.LAB, location="Block Z")
    db_session.add(resource)
    db_session.commit()
    db_session.refresh(resource)
    return resource


def test_create_booking_succeeds(client, db_session):
    resource = seed_resource(db_session)
    token = register_and_login(client, "bookinguser1@campus.edu")

    response = client.post(
        "/api/v1/bookings",
        json={
            "resource_id": resource.id,
            "start_time": "2026-09-10T10:00:00",
            "end_time": "2026-09-10T11:00:00",
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 201


def test_double_booking_same_slot_rejected(client, db_session):
    resource = seed_resource(db_session)
    token = register_and_login(client, "bookinguser2@campus.edu")

    booking_payload = {
        "resource_id": resource.id,
        "start_time": "2026-09-11T14:00:00",
        "end_time": "2026-09-11T15:00:00",
    }

    first = client.post(
        "/api/v1/bookings",
        json=booking_payload,
        headers={"Authorization": f"Bearer {token}"},
    )
    assert first.status_code == 201

    second = client.post(
        "/api/v1/bookings",
        json=booking_payload,
        headers={"Authorization": f"Bearer {token}"},
    )
    assert second.status_code == 409


def test_different_time_slot_same_resource_succeeds(client, db_session):
    resource = seed_resource(db_session)
    token = register_and_login(client, "bookinguser3@campus.edu")

    client.post(
        "/api/v1/bookings",
        json={
            "resource_id": resource.id,
            "start_time": "2026-09-12T09:00:00",
            "end_time": "2026-09-12T10:00:00",
        },
        headers={"Authorization": f"Bearer {token}"},
    )

    response = client.post(
        "/api/v1/bookings",
        json={
            "resource_id": resource.id,
            "start_time": "2026-09-12T11:00:00",
            "end_time": "2026-09-12T12:00:00",
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 201


def test_booking_nonexistent_resource_fails(client):
    token = register_and_login(client, "bookinguser4@campus.edu")

    response = client.post(
        "/api/v1/bookings",
        json={
            "resource_id": 999999,
            "start_time": "2026-09-13T10:00:00",
            "end_time": "2026-09-13T11:00:00",
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 404
