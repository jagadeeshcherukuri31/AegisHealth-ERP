from datetime import date, datetime
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
jwt = JWTManager()
cors = CORS()


class Serializable:
    """Adds to_dict() to SQLAlchemy models."""
    exclude = ()

    def to_dict(self):
        out = {}
        for c in self.__table__.columns:
            if c.name in self.exclude:
                continue
            v = getattr(self, c.name)
            out[c.name] = v.isoformat() if isinstance(v, (date, datetime)) else v
        return out
