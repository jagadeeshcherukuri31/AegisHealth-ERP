from datetime import timedelta
from ..extensions import db
from ..models import Appointment
from ..models.appointment import STATUSES
from ..utils.validators import parse_dt, require_fields


def book(data):
    require_fields(data, "patient_id", "doctor_id", "scheduled_at")
    start = parse_dt(data["scheduled_at"])
    dur = int(data.get("duration_min", 30))
    if has_conflict(data["doctor_id"], start, dur):
        raise ValueError("Doctor already has an appointment in that time slot")
    appt = Appointment(patient_id=data["patient_id"], doctor_id=data["doctor_id"],
                       scheduled_at=start, duration_min=dur, reason=data.get("reason"))
    db.session.add(appt)
    db.session.commit()
    return appt


def has_conflict(doctor_id, start, dur, ignore_id=None):
    end = start + timedelta(minutes=dur)
    q = Appointment.query.filter(Appointment.doctor_id == doctor_id,
                                 Appointment.status.in_(("scheduled", "checked_in")))
    for a in q:
        if a.id == ignore_id:
            continue
        a_end = a.scheduled_at + timedelta(minutes=a.duration_min)
        if start < a_end and a.scheduled_at < end:
            return True
    return False


def set_status(appt, status):
    if status not in STATUSES:
        raise ValueError("Status must be one of: " + ", ".join(STATUSES))
    appt.status = status
    db.session.commit()
    return appt
