from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from ..extensions import db
from ..models import User
from ..models.user import ROLES
from ..utils.permissions import roles_required
from ..utils.validators import require_fields

bp = Blueprint("auth", __name__, url_prefix="/api/auth")


@bp.post("/login")
def login():
    d = require_fields(request.get_json(), "email", "password")
    u = User.query.filter_by(email=d["email"].lower()).first()
    if not u or not u.active or not u.check_password(d["password"]):
        return jsonify(error="Invalid email or password"), 401
    token = create_access_token(identity=str(u.id), additional_claims={"role": u.role})
    return jsonify(token=token, user=u.to_dict())


@bp.get("/me")
@jwt_required()
def me():
    return jsonify(User.query.get_or_404(int(get_jwt_identity())).to_dict())


@bp.post("/register")
@roles_required("admin")
def register():
    d = require_fields(request.get_json(), "name", "email", "password", "role")
    if d["role"] not in ROLES:
        raise ValueError("Role must be one of: " + ", ".join(ROLES))
    if User.query.filter_by(email=d["email"].lower()).first():
        raise ValueError("Email already registered")
    u = User(name=d["name"], email=d["email"].lower(), role=d["role"])
    u.set_password(d["password"])
    db.session.add(u)
    db.session.commit()
    return jsonify(u.to_dict()), 201
