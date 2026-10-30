from datetime import date, timedelta
from ..extensions import db
from ..models import Medicine


def dispense(med, qty):
    qty = int(qty)
    if qty <= 0:
        raise ValueError("Quantity must be positive")
    if med.expiry_date and med.expiry_date < date.today():
        raise ValueError("Medicine batch has expired")
    if med.stock < qty:
        raise ValueError(f"Insufficient stock: {med.stock} available")
    med.stock -= qty
    db.session.commit()
    return med


def low_stock():
    return Medicine.query.filter(Medicine.stock <= Medicine.reorder_level).all()


def expiring_soon(days=60):
    cutoff = date.today() + timedelta(days=days)
    return Medicine.query.filter(Medicine.expiry_date <= cutoff).all()
