from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt

from extensions import db
from models.unit import Unit
from models.tower import Tower
from models.booking import Booking
from models.amenity import Amenity

# --------------------------------------------------
# Blueprint
# --------------------------------------------------
admin_bp = Blueprint("admin_bp", __name__)

# --------------------------------------------------
# ✅ ADMIN CHECK (JWT CLAIMS)
# --------------------------------------------------
def admin_required():
    claims = get_jwt()
    return claims.get("role") == "admin"


# ==================================================
# 🏢 TOWERS CRUD (ADMIN)
# ==================================================

@admin_bp.post("/towers")
@jwt_required()
def add_tower():
    if not admin_required():
        return jsonify({"error": "Admin only"}), 403

    data = request.get_json() or {}

    name = data.get("name")
    floors = data.get("floors")

    if not name:
        return jsonify({"error": "name is required"}), 400

    tower = Tower(name=name, floors=int(floors or 1))
    db.session.add(tower)
    db.session.commit()

    return jsonify({
        "message": "Tower added successfully",
        "tower": tower.to_dict()
    }), 201


@admin_bp.get("/towers")
@jwt_required()
def get_towers():
    if not admin_required():
        return jsonify({"error": "Admin only"}), 403

    towers = Tower.query.order_by(Tower.id.desc()).all()
    return jsonify({
        "towers": [t.to_dict() for t in towers]
    }), 200


# ==================================================
# 🏠 UNITS CRUD (ADMIN)
# ==================================================

@admin_bp.post("/units")
@jwt_required()
def add_unit():
    if not admin_required():
        return jsonify({"error": "Admin only"}), 403

    data = request.get_json() or {}

    try:
        unit = Unit(
            tower_id=int(data["tower_id"]),
            unit_no=data["unit_no"],
            floor=int(data["floor"]),
            bhk=data["bhk"],
            rent=float(data["rent"]),
            status=data.get("status", "available"),

            # ✅ FIX
            furnishing_type=data.get("furnishing_type")
        )

        # ✅ SAVE AMENITIES
        if "amenities" in data:
            amenities = Amenity.query.filter(
                Amenity.id.in_(data["amenities"])
            ).all()

            unit.amenities = amenities

        db.session.add(unit)
        db.session.commit()

        return jsonify({"message": "Unit added successfully"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@admin_bp.get("/units")
@jwt_required()
def get_units():
    if not admin_required():
        return jsonify({"error": "Admin only"}), 403

    units = Unit.query.all()

    result = []

    for u in units:
        result.append({
            "id": u.id,
            "unit_no": u.unit_no,
            "tower": u.tower.name if u.tower else None,
            "floor": u.floor,
            "bhk": u.bhk,
            "rent": u.rent,
            "status": u.status,

            # ✅ IMPORTANT
            "furnishing_type": u.furnishing_type,

            # ✅ IMPORTANT
            "amenities": [
                {"id": a.id, "name": a.name}
                for a in u.amenities
            ]
        })

    return jsonify({"units": result}), 200


@admin_bp.delete("/units/<int:unit_id>")
@jwt_required()
def delete_unit(unit_id):
    if not admin_required():
        return jsonify({"error": "Admin only"}), 403

    unit = Unit.query.get_or_404(unit_id)
    db.session.delete(unit)
    db.session.commit()

    return jsonify({
        "message": "Unit deleted successfully"
    }), 200


# ==================================================
# 📅 BOOKINGS (ADMIN)
# ==================================================

@admin_bp.route('/bookings/<int:id>/approve', methods=['PUT'])
@jwt_required()
def approve_booking(id):
    booking = Booking.query.get_or_404(id)

    booking.status = "approved"

    # ✅ Mark unit occupied
    unit = Unit.query.get(booking.unit_id)
    if unit:
        unit.status = "occupied"

    db.session.commit()

    return jsonify({"message": "Booking approved"})


