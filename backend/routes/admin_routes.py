from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt

from extensions import db
from models.unit import Unit
from models.tower import Tower
from models.booking import Booking

admin_bp = Blueprint("admin_bp", __name__, url_prefix="/api/admin")


# ✅ simple admin check using JWT claims
def admin_required():
    claims = get_jwt()
    return claims.get("role") == "admin"


# -----------------------------------
# ✅ UNITS CRUD (Admin)
# -----------------------------------

@admin_bp.post("/units")
@jwt_required()
def add_unit():
    if not admin_required():
        return jsonify({"error": "Admin only"}), 403

    data = request.get_json() or {}

    required_fields = ["tower_id", "unit_no", "floor", "bhk", "rent"]
    for field in required_fields:
        if field not in data or data[field] in [None, ""]:
            return jsonify({"error": f"{field} is required"}), 400

    # ✅ validate tower_id FK
    tower = Tower.query.get(int(data["tower_id"]))
    if not tower:
        return jsonify({"error": "Invalid tower_id. Tower does not exist"}), 400

    unit = Unit(
        tower_id=int(data["tower_id"]),
        unit_no=data["unit_no"],
        floor=int(data["floor"]),
        bhk=data["bhk"],
        rent=data["rent"],
        status=data.get("status", "available")
    )

    db.session.add(unit)
    db.session.commit()

    return jsonify({
        "message": "Unit added successfully",
        "unit": unit.to_dict()
    }), 201


@admin_bp.get("/units")
@jwt_required()
def get_all_units():
    if not admin_required():
        return jsonify({"error": "Admin only"}), 403

    units = Unit.query.order_by(Unit.id.desc()).all()
    return jsonify({"units": [u.to_dict() for u in units]}), 200


@admin_bp.delete("/units/<int:unit_id>")
@jwt_required()
def delete_unit(unit_id):
    if not admin_required():
        return jsonify({"error": "Admin only"}), 403

    unit = Unit.query.get_or_404(unit_id)
    db.session.delete(unit)
    db.session.commit()

    return jsonify({"message": "Unit deleted successfully"}), 200


# -----------------------------------
# ✅ BOOKINGS (Admin)
# -----------------------------------

@admin_bp.put("/bookings/<int:booking_id>/approve")
@jwt_required()
def approve_booking(booking_id):
    if not admin_required():
        return jsonify({"error": "Admin only"}), 403

    booking = Booking.query.get_or_404(booking_id)
    booking.status = "APPROVED"
    db.session.commit()

    return jsonify({"message": "Booking approved"}), 200
