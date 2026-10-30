from werkzeug.security import check_password_hash, generate_password_hash
from ..extensions import Serializable, db

ROLES = ("admin", "doctor", "nurse", "receptionist", "pharmacist", "billing")


class User(db.Model, Serializable):
    __tablename__ = "users"
    exclude = ("password_hash",)
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False, default="receptionist")
    active = db.Column(db.Boolean, default=True)

    def set_password(self, pw):
        self.password_hash = generate_password_hash(pw)

    def check_password(self, pw):
        return check_password_hash(self.password_hash, pw)
