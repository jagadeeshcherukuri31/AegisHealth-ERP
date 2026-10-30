import pytest
from datetime import date
from app import create_app
from app.config import TestConfig
from app.extensions import db
from app.models import Doctor, Medicine, Patient, User


@pytest.fixture
def client():
    app = create_app(TestConfig)
    with app.app_context():
        db.create_all()
        for name, email, role in [("Admin", "a@t", "admin"), ("Doc", "d@t", "doctor"), ("Pharm", "p@t", "pharmacist")]:
            u = User(name=name, email=email, role=role)
            u.set_password("pw")
            db.session.add(u)
        db.session.flush()
        db.session.add(Doctor(user_id=2))
        db.session.add(Patient(mrn="MRN1", first_name="A", last_name="B", dob=date(2000, 1, 1)))
        db.session.add(Medicine(name="X", sku="X1", stock=5, reorder_level=1))
        db.session.commit()
    return app.test_client()


def auth(c, email):
    t = c.post("/api/auth/login", json={"email": email, "password": "pw"}).json["token"]
    return {"Authorization": f"Bearer {t}"}


def test_login_rejects_bad_password(client):
    assert client.post("/api/auth/login", json={"email": "a@t", "password": "no"}).status_code == 401


def test_role_enforced(client):
    assert client.get("/api/billing", headers=auth(client, "p@t")).status_code == 403


def test_double_booking_blocked(client):
    h = auth(client, "a@t")
    body = {"patient_id": 1, "doctor_id": 1, "scheduled_at": "2030-01-01T09:00:00"}
    assert client.post("/api/appointments", json=body, headers=h).status_code == 201
    r = client.post("/api/appointments", json={**body, "scheduled_at": "2030-01-01T09:15:00"}, headers=h)
    assert r.status_code == 400


def test_invoice_payment_flow(client):
    h = auth(client, "a@t")
    inv = client.post("/api/billing", headers=h, json={"patient_id": 1, "items": [{"description": "Visit", "unit_price": 100}]}).json
    assert client.post(f"/api/billing/{inv['id']}/pay", json={"amount": 40}, headers=h).json["status"] == "partial"
    assert client.post(f"/api/billing/{inv['id']}/pay", json={"amount": 60}, headers=h).json["status"] == "paid"


def test_dispense_cannot_oversell(client):
    h = auth(client, "p@t")
    assert client.post("/api/pharmacy/1/dispense", json={"quantity": 3}, headers=h).json["stock"] == 2
    assert client.post("/api/pharmacy/1/dispense", json={"quantity": 9}, headers=h).status_code == 400
