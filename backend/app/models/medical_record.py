from datetime import datetime
from ..extensions import Serializable, db


class MedicalRecord(db.Model, Serializable):
    __tablename__ = "medical_records"
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey("patients.id"), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey("doctors.id"), nullable=False)
    appointment_id = db.Column(db.Integer, db.ForeignKey("appointments.id"))
    diagnosis = db.Column(db.String(255), nullable=False)
    notes = db.Column(db.Text)
    prescription = db.Column(db.Text)
    bp = db.Column(db.String(10))
    heart_rate = db.Column(db.Integer)
    temperature_c = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    doctor = db.relationship("Doctor")

    def to_dict(self):
        d = super().to_dict()
        d["doctor_name"] = self.doctor.user.name
        return d
