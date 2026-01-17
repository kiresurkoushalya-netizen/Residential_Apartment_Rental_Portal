from extensions import db
from datetime import datetime

class Unit(db.Model):
    __tablename__ = "units"

    id = db.Column(db.Integer, primary_key=True)
    tower_id = db.Column(db.Integer, db.ForeignKey("towers.id"), nullable=False)

    unit_no = db.Column(db.String(50), nullable=False)
    floor = db.Column(db.Integer, nullable=False)
    bhk = db.Column(db.String(20), nullable=False)
    rent = db.Column(db.Numeric(10, 2), nullable=False)

    status = db.Column(db.String(20), default="available")  # available/occupied
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    bookings = db.relationship("Booking", backref="unit", lazy=True, cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "tower_id": self.tower_id,
            "tower": self.tower.name if self.tower else None,
            "unit_no": self.unit_no,
            "floor": self.floor,
            "bhk": self.bhk,
            "rent": float(self.rent),
            "status": self.status
        }
