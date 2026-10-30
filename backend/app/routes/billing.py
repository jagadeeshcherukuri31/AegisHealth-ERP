from flask import Blueprint, jsonify, request
from ..models import Invoice
from ..services import billing_service as svc
from ..utils.permissions import roles_required

bp = Blueprint("billing", __name__, url_prefix="/api/billing")


@bp.get("")
@roles_required("billing", "receptionist")
def list_invoices():
    q = Invoice.query
    if request.args.get("status"):
        q = q.filter_by(status=request.args["status"])
    return jsonify([i.to_dict() for i in q.order_by(Invoice.id.desc()).limit(200)])


@bp.post("")
@roles_required("billing", "receptionist")
def create():
    return jsonify(svc.create_invoice(request.get_json()).to_dict()), 201


@bp.get("/<int:iid>")
@roles_required("billing", "receptionist")
def get_invoice(iid):
    return jsonify(Invoice.query.get_or_404(iid).to_dict())


@bp.post("/<int:iid>/pay")
@roles_required("billing", "receptionist")
def pay(iid):
    inv = Invoice.query.get_or_404(iid)
    amount = (request.get_json() or {}).get("amount", inv.total - inv.paid)
    return jsonify(svc.record_payment(inv, amount).to_dict())
