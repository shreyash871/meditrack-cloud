import uuid


async def test_create_booking_returns_201(client):
    payload = {
        "patient_name": "Test Patient",
        "doctor_id": f"doc-{uuid.uuid4()}",
        "slot": "2026-12-01T09:00:00Z",
    }
    response = await client.post("/bookings", json=payload)

    assert response.status_code == 201
    body = response.json()
    assert body["status"] == "confirmed"
    assert "id" in body


async def test_duplicate_slot_returns_409(client):
    payload = {
        "patient_name": "First Patient",
        "doctor_id": f"doc-{uuid.uuid4()}",
        "slot": "2026-12-01T10:00:00Z",
    }

    first = await client.post("/bookings", json=payload)
    second = await client.post(
        "/bookings", json={**payload, "patient_name": "Second Patient"}
    )

    assert first.status_code == 201
    assert second.status_code == 409


async def test_empty_patient_name_rejected(client):
    response = await client.post(
        "/bookings",
        json={
            "patient_name": "",
            "doctor_id": "doc-x",
            "slot": "2026-12-01T11:00:00Z",
        },
    )
    assert response.status_code == 422


async def test_invalid_booking_id_returns_400(client):
    response = await client.get("/bookings/not-an-object-id")
    assert response.status_code == 400
