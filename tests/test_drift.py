from fastapi.testclient import TestClient
from drift.main import app

def test_shift_and_stable_batch():
    client = TestClient(app)
    reference = [10, 11, 9, 10, 12]
    moved = client.post("/drift", json={"reference": reference, "current": [30, 31, 29, 30, 32]}).json()
    assert moved["drift"] is True
    assert moved["retrained"] is False
    stable = client.post("/drift", json={"reference": reference, "current": reference}).json()
    assert stable["drift"] is False
