from ..extensions import Serializable, db


class Medicine(db.Model, Serializable):
    __tablename__ = "medicines"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    sku = db.Column(db.String(40), unique=True, nullable=False)
    stock = db.Column(db.Integer, default=0)
    reorder_level = db.Column(db.Integer, default=20)
    unit_price = db.Column(db.Float, default=0)
    expiry_date = db.Column(db.Date)

    def to_dict(self):
        d = super().to_dict()
        d["low_stock"] = self.stock <= self.reorder_level
        return d
