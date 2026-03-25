# models/unit.py
from extensions import db
from datetime import datetime

unit_amenities = db.Table(
    "unit_amenities",
    db.Column("unit_id", db.Integer, db.ForeignKey("units.id"), primary_key=True),
    db.Column("amenity_id", db.Integer, db.ForeignKey("amenities.id"), primary_key=True),
)

class Unit(db.Model):
    __tablename__ = "units"

    id = db.Column(db.Integer, primary_key=True)
    tower_id = db.Column(db.Integer, db.ForeignKey("towers.id"), nullable=False)
    unit_no = db.Column(db.String(50), nullable=False)
    floor = db.Column(db.Integer, nullable=False)
    bhk = db.Column(db.String(20), nullable=False)
    furnishing_type = db.Column(db.String(50), nullable=False, default="Unfurnished")
    amenities = db.relationship('Amenity', secondary=unit_amenities)
    rent = db.Column(db.Numeric(10, 2), nullable=False)

    # IMPORTANT: lowercase values only
    status = db.Column(db.String(20), default="available")
    tower = db.relationship("Tower", back_populates="units")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "tower": self.tower.name if self.tower else None,
            "unit_no": self.unit_no,
            "floor": self.floor,
            "bhk": self.bhk,
            "rent": float(self.rent),
            "furnishing_type": self.furnishing_type,   # ✅ NEW
            "amenities": [a.to_dict() for a in self.amenities],
            "status": self.status
        }