from datetime import datetime, timedelta
from flask import Blueprint, jsonify, request
from ..extensions import db
from ..models import Appointment, Doctor
from ..services import appointment_service as svc
from ..utils.permissions import roles_required
from ..utils.validators import parse_date

bp = Blueprint("appointments", __name__, url_prefix="/api/appointments")
CLINICAL = ("doctor", "nurse", "receptionist")


@bp.get("")
@roles_required(*CLINICAL, "billing")
def list_appts():
    q = Appointment.query
    if request.args.get("date"):
        day = datetime.combine(parse_date(request.args["date"]), datetime.min.time())
        q = q.filter(Appointment.scheduled_at >= day, Appointment.scheduled_at < day + timedelta(days=1))
    for key in ("doctor_id", "patient_id", "status"):
        if request.args.get(key):
            q = q.filter(getattr(Appointment, key) == request.args[key])
    return jsonify([a.to_dict() for a in q.order_by(Appointment.scheduled_at).limit(300)])


@bp.get("/doctors")
@roles_required(*CLINICAL, "billing")
def doctors():
    return jsonify([d.to_dict() for d in Doctor.query.all()])


@bp.post("")
@roles_required("receptionist", "nurse", "doctor")
def book():
    return jsonify(svc.book(request.get_json()).to_dict()), 201


@bp.patch("/<int:aid>/status")
@roles_required(*CLINICAL)
def status(aid):
    a = Appointment.query.get_or_404(aid)
    return jsonify(svc.set_status(a, (request.get_json() or {}).get("status")).to_dict())


@bp.delete("/<int:aid>")
@roles_required("receptionist")
def delete(aid):
    db.session.delete(Appointment.query.get_or_404(aid))
    db.session.commit()
    return "", 204
