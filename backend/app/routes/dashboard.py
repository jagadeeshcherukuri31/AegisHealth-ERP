from datetime import date, datetime, timedelta
from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
from sqlalchemy import func
from ..extensions import db
from ..models import Appointment, Invoice, Patient
from ..services import inventory_service

bp = Blueprint("dashboard", __name__, url_prefix="/api/dashboard")


@bp.get("")
@jwt_required()
def stats():
    start = datetime.combine(date.today(), datetime.min.time())
    today = Appointment.query.filter(Appointment.scheduled_at >= start,
                                     Appointment.scheduled_at < start + timedelta(days=1))
    by_status = dict(db.session.query(Invoice.status, func.count()).group_by(Invoice.status).all())
    return jsonify(
        patients=Patient.query.count(),
        appointments_today=today.count(),
        waiting=today.filter(Appointment.status == "checked_in").count(),
        outstanding=round(db.session.query(func.coalesce(func.sum(Invoice.total - Invoice.paid), 0)).scalar(), 2),
        invoices_by_status=by_status,
        low_stock=len(inventory_service.low_stock()),
        upcoming=[a.to_dict() for a in today.filter(Appointment.status.in_(("scheduled", "checked_in")))
                  .order_by(Appointment.scheduled_at).limit(8)],
    )
