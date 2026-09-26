async def test_liveness_always_ok(client):
    response = await client.get("/health/live")
    assert response.status_code == 200
    assert response.json()["status"] == "alive"


async def test_readiness_ok_when_mongo_up(client):
    response = await client.get("/health/ready")
    assert response.status_code == 200
    assert response.json()["mongodb"] == "connected"
