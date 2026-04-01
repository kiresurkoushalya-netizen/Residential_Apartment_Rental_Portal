from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.orm import joinedload

from models import db, Unit, Tower, Amenity

unit_bp = Blueprint("unit_bp", __name__, url_prefix="/api")


def admin_required():
    identity = get_jwt_identity()
    return identity and identity.get("role") == "admin"


@unit_bp.get("/units")
def list_units():
    status = request.args.get("status")

    q = Unit.query
    if status:
        q = q.filter(Unit.status.ilike(status))  # case-safe

    units = q.order_by(Unit.id.asc()).all()
    return jsonify([u.to_dict() for u in units]), 200

@unit_bp.get("/admin/units")
@jwt_required()
def get_admin_units():

    if not admin_required():
        return jsonify({"error": "Admin only"}), 403

    units = Unit.query.options(
        joinedload(Unit.amenities),
        joinedload(Unit.tower)
    ).order_by(Unit.id.asc()).all()

    return jsonify([u.to_dict() for u in units]), 200


@unit_bp.get("/units/<int:unit_id>")
def get_unit(unit_id):
    unit = Unit.query.get_or_404(unit_id)
    return jsonify(unit.to_dict())


@unit_bp.post("/admin/units")
@jwt_required()
def create_unit():
    if not admin_required():
        return jsonify({"error": "Admin only"}), 403

    data = request.get_json()

    tower_id = data.get("tower_id")
    if not tower_id or not Tower.query.get(tower_id):
        return jsonify({"error": "Valid tower_id required"}), 400
    
    amenity_ids = data.get("amenity_ids", [])
    amenities = Amenity.query.filter(
        Amenity.id.in_(amenity_ids)
    ).all()

    unit = Unit(
        tower_id=tower_id,
        unit_no=data.get("unit_no"),
        floor=data.get("floor"),
        bhk=data.get("bhk"),
        rent=data.get("rent"),
        status=data.get("status", "available"),
        furnishing_type=data.get("furnishing_type", "Unfurnished"),
        amenities=amenities
    )

    db.session.add(unit)
    db.session.commit()
    return jsonify(unit.to_dict()), 201


@unit_bp.put("/admin/units/<int:unit_id>")
@jwt_required()
def update_unit(unit_id):
    if not admin_required():
        return jsonify({"error": "Admin only"}), 403

    unit = Unit.query.get_or_404(unit_id)
    data = request.get_json()

    unit.unit_no = data.get("unit_no", unit.unit_no)
    unit.floor = data.get("floor", unit.floor)
    unit.bhk = data.get("bhk", unit.bhk)
    unit.rent = data.get("rent", unit.rent)
    unit.status = data.get("status", unit.status)
    unit.furnishing_type = data.get("furnishing_type", unit.furnishing_type)

    # ✅ UPDATE AMENITIES
    if "amenity_ids" in data:
        amenities = Amenity.query.filter(
            Amenity.id.in_(data.get("amenity_ids", []))
        ).all()
        unit.amenities = amenities

    db.session.commit()
    return jsonify(unit.to_dict())


@unit_bp.delete("/admin/units/<int:unit_id>")
@jwt_required()
def delete_unit(unit_id):
    if not admin_required():
        return jsonify({"error": "Admin only"}), 403

    unit = Unit.query.get_or_404(unit_id)
    db.session.delete(unit)
    db.session.commit()
    return jsonify({"message": "Unit deleted successfully"})
