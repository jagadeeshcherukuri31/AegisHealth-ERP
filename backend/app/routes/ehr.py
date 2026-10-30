from flask import Blueprint, jsonify, request
from ..extensions import db
from ..models import MedicalRecord
from ..utils.permissions import roles_required
from ..utils.validators import require_fields

bp = Blueprint("ehr", __name__, url_prefix="/api/ehr")
FIELDS = ("appointment_id", "notes", "prescription", "bp", "heart_rate", "temperature_c")


@bp.get("")
@roles_required("doctor", "nurse")
def list_records():
    q = MedicalRecord.query
    if request.args.get("patient_id"):
        q = q.filter_by(patient_id=request.args["patient_id"])
    return jsonify([r.to_dict() for r in q.order_by(MedicalRecord.created_at.desc()).limit(200)])


@bp.get("/<int:rid>")
@roles_required("doctor", "nurse")
def get_record(rid):
    return jsonify(MedicalRecord.query.get_or_404(rid).to_dict())


@bp.post("")
@roles_required("doctor")
def create_record():
    d = require_fields(request.get_json(), "patient_id", "doctor_id", "diagnosis")
    r = MedicalRecord(patient_id=d["patient_id"], doctor_id=d["doctor_id"],
                      diagnosis=d["diagnosis"], **{k: d.get(k) or None for k in FIELDS})
    db.session.add(r)
    db.session.commit()
    return jsonify(r.to_dict()), 201
