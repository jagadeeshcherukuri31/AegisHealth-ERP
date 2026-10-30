from ..extensions import Serializable, db


class Doctor(db.Model, Serializable):
    __tablename__ = "doctors"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), unique=True, nullable=False)
    specialization = db.Column(db.String(80))
    license_no = db.Column(db.String(40))
    department = db.Column(db.String(80))
    user = db.relationship("User")

    def to_dict(self):
        d = super().to_dict()
        d["name"] = self.user.name if self.user else None
        return d
