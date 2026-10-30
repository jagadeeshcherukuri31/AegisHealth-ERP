from ..extensions import db
from ..models import Invoice, InvoiceItem
from ..utils.validators import require_fields


def create_invoice(data):
    require_fields(data, "patient_id", "items")
    if not data["items"]:
        raise ValueError("Invoice needs at least one item")
    inv = Invoice(patient_id=data["patient_id"], appointment_id=data.get("appointment_id"))
    for it in data["items"]:
        require_fields(it, "description", "unit_price")
        inv.items.append(InvoiceItem(description=it["description"],
                                     quantity=int(it.get("quantity", 1)),
                                     unit_price=float(it["unit_price"])))
    inv.total = round(sum(i.quantity * i.unit_price for i in inv.items), 2)
    db.session.add(inv)
    db.session.commit()
    return inv


def record_payment(inv, amount):
    amount = float(amount)
    if amount <= 0:
        raise ValueError("Payment must be greater than zero")
    if inv.paid + amount > inv.total + 1e-9:
        raise ValueError("Payment exceeds outstanding balance")
    inv.paid = round(inv.paid + amount, 2)
    inv.status = "paid" if inv.paid >= inv.total else "partial"
    db.session.commit()
    return inv
