from datetime import datetime
from ..extensions import Serializable, db


class Invoice(db.Model, Serializable):
    __tablename__ = "invoices"
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey("patients.id"), nullable=False)
    appointment_id = db.Column(db.Integer, db.ForeignKey("appointments.id"))
    total = db.Column(db.Float, default=0)
    paid = db.Column(db.Float, default=0)
    status = db.Column(db.String(10), default="unpaid")  # unpaid | partial | paid
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    patient = db.relationship("Patient")
    items = db.relationship("InvoiceItem", cascade="all, delete-orphan")

    def to_dict(self):
        d = super().to_dict()
        d["patient_name"] = f"{self.patient.first_name} {self.patient.last_name}"
        d["balance"] = round(self.total - self.paid, 2)
        d["items"] = [i.to_dict() for i in self.items]
        return d


class InvoiceItem(db.Model, Serializable):
    __tablename__ = "invoice_items"
    id = db.Column(db.Integer, primary_key=True)
    invoice_id = db.Column(db.Integer, db.ForeignKey("invoices.id"), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    quantity = db.Column(db.Integer, default=1)
    unit_price = db.Column(db.Float, nullable=False)
