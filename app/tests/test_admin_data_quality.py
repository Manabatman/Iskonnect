"""Admin data-quality dashboard endpoint."""

from app import models
from app.auth import create_access_token


def _admin_headers(client, Session):
    db = Session()
    try:
        user = models.User(
            email="admin_dq@example.com",
            password_hash="x",
            role="admin",
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        token = create_access_token(user.id, role="admin")
        return {"Authorization": f"Bearer {token}"}
    finally:
        db.close()


def test_admin_data_quality_dashboard(api_with_db):
    client, Session = api_with_db
    headers = _admin_headers(client, Session)
    r = client.get("/api/v1/admin/data-quality", headers=headers)
    assert r.status_code == 200, r.text
    data = r.json()
    assert "total_active" in data
    assert "average_completeness" in data
    assert "tier_distribution" in data
    assert "high_priority_records" in data
    assert "publishability_threshold" in data
