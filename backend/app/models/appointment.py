from ..extensions import Serializable, db

STATUSES = ("scheduled", "checked_in", "completed", "cancelled", "no_show")


class Appointment(db.Model, Serializable):
    __tablename__ = "appointments"
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey("patients.id"), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey("doctors.id"), nullable=False)
    scheduled_at = db.Column(db.DateTime, nullable=False)
    duration_min = db.Column(db.Integer, default=30)
    status = db.Column(db.String(20), default="scheduled")
    reason = db.Column(db.String(255))
    patient = db.relationship("Patient")
    doctor = db.relationship("Doctor")

    def to_dict(self):
        d = super().to_dict()
        d["patient_name"] = f"{self.patient.first_name} {self.patient.last_name}"
        d["doctor_name"] = self.doctor.user.name
        return d
