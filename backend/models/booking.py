from extensions import db
from datetime import datetime

class Booking(db.Model):
    __tablename__ = "bookings"

    id = db.Column(db.Integer, primary_key=True)

    unit_id = db.Column(db.Integer, db.ForeignKey("units.id"), nullable=False)
    tenant_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    visit_date = db.Column(db.Date, nullable=False)
    notes = db.Column(db.Text, nullable=True)

    status = db.Column(db.String(20), default="pending")  # pending/approved/declined
    reason = db.Column(db.Text, nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    unit = db.relationship("Unit")
    
    def to_dict(self):
        return {
            "id": self.id,
            "unit_id": self.unit_id,
            "unit": self.unit.unit_no if self.unit else None,
            "tower": self.unit.tower.name if self.unit and self.unit.tower else None,
            "tenant_id": self.tenant_id,
            "tenant": self.tenant.name if self.tenant else None,
            "visit_date": self.visit_date.isoformat(),
            "notes": self.notes,
            "status": self.status,
            "reason": self.reason
        }
