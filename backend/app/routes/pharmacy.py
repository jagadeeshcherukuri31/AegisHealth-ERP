from flask import Blueprint, jsonify, request
from ..extensions import db
from ..models import Medicine
from ..services import inventory_service as svc
from ..utils.permissions import roles_required
from ..utils.validators import parse_date, require_fields

bp = Blueprint("pharmacy", __name__, url_prefix="/api/pharmacy")


@bp.get("")
@roles_required("pharmacist", "doctor", "nurse")
def list_meds():
    q = Medicine.query
    if request.args.get("q"):
        q = q.filter(Medicine.name.ilike(f"%{request.args['q']}%"))
    return jsonify([m.to_dict() for m in q.order_by(Medicine.name)])


@bp.get("/alerts")
@roles_required("pharmacist")
def alerts():
    return jsonify(low_stock=[m.to_dict() for m in svc.low_stock()],
                   expiring=[m.to_dict() for m in svc.expiring_soon()])


@bp.post("")
@roles_required("pharmacist")
def create():
    d = require_fields(request.get_json(), "name", "sku")
    m = Medicine(name=d["name"], sku=d["sku"], stock=int(d.get("stock") or 0),
                 reorder_level=int(d.get("reorder_level") or 20),
                 unit_price=float(d.get("unit_price") or 0),
                 expiry_date=parse_date(d["expiry_date"]) if d.get("expiry_date") else None)
    db.session.add(m)
    db.session.commit()
    return jsonify(m.to_dict()), 201


@bp.post("/<int:mid>/restock")
@roles_required("pharmacist")
def restock(mid):
    m = Medicine.query.get_or_404(mid)
    qty = int((request.get_json() or {}).get("quantity", 0))
    if qty <= 0:
        raise ValueError("Quantity must be positive")
    m.stock += qty
    db.session.commit()
    return jsonify(m.to_dict())


@bp.post("/<int:mid>/dispense")
@roles_required("pharmacist")
def dispense(mid):
    m = Medicine.query.get_or_404(mid)
    return jsonify(svc.dispense(m, (request.get_json() or {}).get("quantity", 1)).to_dict())
