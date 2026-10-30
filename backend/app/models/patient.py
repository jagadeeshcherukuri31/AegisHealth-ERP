from datetime import datetime
from ..extensions import Serializable, db


class Patient(db.Model, Serializable):
    __tablename__ = "patients"
    id = db.Column(db.Integer, primary_key=True)
    mrn = db.Column(db.String(20), unique=True, nullable=False)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    dob = db.Column(db.Date, nullable=False)
    gender = db.Column(db.String(10))
    phone = db.Column(db.String(30))
    email = db.Column(db.String(120))
    address = db.Column(db.String(255))
    blood_group = db.Column(db.String(5))
    allergies = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
