from flask import Blueprint, jsonify, request
from sqlalchemy import or_
from ..extensions import db
from ..models import Patient
from ..utils.permissions import roles_required
from ..utils.validators import parse_date, require_fields

bp = Blueprint("patients", __name__, url_prefix="/api/patients")
FIELDS = ("first_name", "last_name", "gender", "phone", "email", "address", "blood_group", "allergies")


@bp.get("")
@roles_required("doctor", "nurse", "receptionist", "billing", "pharmacist")
def list_patients():
    q = Patient.query
    s = request.args.get("q", "").strip()
    if s:
        like = f"%{s}%"
        q = q.filter(or_(Patient.first_name.ilike(like), Patient.last_name.ilike(like),
                         Patient.mrn.ilike(like), Patient.phone.ilike(like)))
    return jsonify([p.to_dict() for p in q.order_by(Patient.id.desc()).limit(200)])


@bp.post("")
@roles_required("receptionist", "nurse", "doctor")
def create_patient():
    d = require_fields(request.get_json(), "first_name", "last_name", "dob")
    p = Patient(mrn="TMP", dob=parse_date(d["dob"]), **{k: d.get(k) for k in FIELDS})
    db.session.add(p)
    db.session.flush()
    p.mrn = f"MRN{p.id:06d}"
    db.session.commit()
    return jsonify(p.to_dict()), 201


@bp.get("/<int:pid>")
@roles_required("doctor", "nurse", "receptionist", "billing", "pharmacist")
def get_patient(pid):
    return jsonify(Patient.query.get_or_404(pid).to_dict())


@bp.put("/<int:pid>")
@roles_required("receptionist", "nurse", "doctor")
def update_patient(pid):
    p, d = Patient.query.get_or_404(pid), request.get_json() or {}
    for k in FIELDS:
        if k in d:
            setattr(p, k, d[k])
    if "dob" in d:
        p.dob = parse_date(d["dob"])
    db.session.commit()
    return jsonify(p.to_dict())


@bp.delete("/<int:pid>")
@roles_required()
def delete_patient(pid):
    db.session.delete(Patient.query.get_or_404(pid))
    db.session.commit()
    return "", 204
