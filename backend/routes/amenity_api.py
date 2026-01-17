from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from models import db, Amenity, Unit
from amenity import unit_amenities 

amenity_bp = Blueprint("amenity_bp", __name__, url_prefix="/api")


def admin_required():
    identity = get_jwt_identity()
    return identity and identity.get("role") == "admin"


# -------------------------
# Public/Resident
# -------------------------
@amenity_bp.get("/amenities")
def list_amenities():
    amenities = Amenity.query.order_by(Amenity.id.asc()).all()
    return jsonify([a.to_dict() for a in amenities])


# -------------------------
# Admin - CRUD
# -------------------------
@amenity_bp.post("/admin/amenities")
@jwt_required()
def create_amenity():
    if not admin_required():
        return jsonify({"error": "Admin only"}), 403

    data = request.get_json()
    name = data.get("name")

    if not name:
        return jsonify({"error": "name required"}), 400

    if Amenity.query.filter_by(name=name).first():
        return jsonify({"error": "Amenity already exists"}), 409

    amenity = Amenity(
        name=name,
        icon=data.get("icon")
    )

    db.session.add(amenity)
    db.session.commit()
    return jsonify(amenity.to_dict()), 201


@amenity_bp.put("/admin/amenities/<int:amenity_id>")
@jwt_required()
def update_amenity(amenity_id):
    if not admin_required():
        return jsonify({"error": "Admin only"}), 403

    amenity = Amenity.query.get_or_404(amenity_id)
    data = request.get_json()

    amenity.name = data.get("name", amenity.name)
    amenity.icon = data.get("icon", amenity.icon)

    db.session.commit()
    return jsonify(amenity.to_dict())


@amenity_bp.delete("/admin/amenities/<int:amenity_id>")
@jwt_required()
def delete_amenity(amenity_id):
    if not admin_required():
        return jsonify({"error": "Admin only"}), 403

    amenity = Amenity.query.get_or_404(amenity_id)
    db.session.delete(amenity)
    db.session.commit()
    return jsonify({"message": "Amenity deleted successfully"})


# -------------------------
# Unit Amenities Mapping APIs
# -------------------------

@amenity_bp.get("/units/<int:unit_id>/amenities")
def get_unit_amenities(unit_id):
    unit = Unit.query.get_or_404(unit_id)

    # SQLAlchemy "secondary" can be done, but here using raw join table
    rows = db.session.execute(
        unit_amenities.select().where(unit_amenities.c.unit_id == unit_id)
    ).fetchall()

    amenity_ids = [r.amenity_id for r in rows]
    amenities = Amenity.query.filter(Amenity.id.in_(amenity_ids)).all()

    return jsonify({
        "unit_id": unit_id,
        "unit_no": unit.unit_no,
        "amenities": [a.to_dict() for a in amenities]
    })


@amenity_bp.post("/admin/units/<int:unit_id>/amenities")
@jwt_required()
def add_unit_amenities(unit_id):
    if not admin_required():
        return jsonify({"error": "Admin only"}), 403

    Unit.query.get_or_404(unit_id)
    data = request.get_json()

    amenity_ids = data.get("amenity_ids", [])
    if not amenity_ids:
        return jsonify({"error": "amenity_ids required"}), 400

    # Insert into join table
    for aid in amenity_ids:
        if Amenity.query.get(aid):
            db.session.execute(unit_amenities.insert().values(unit_id=unit_id, amenity_id=aid))

    db.session.commit()
    return jsonify({"message": "Amenities mapped to unit successfully"}), 201


@amenity_bp.delete("/admin/units/<int:unit_id>/amenities/<int:amenity_id>")
@jwt_required()
def remove_unit_amenity(unit_id, amenity_id):
    if not admin_required():
        return jsonify({"error": "Admin only"}), 403

    Unit.query.get_or_404(unit_id)
    Amenity.query.get_or_404(amenity_id)

    db.session.execute(
        unit_amenities.delete().where(
            (unit_amenities.c.unit_id == unit_id) &
            (unit_amenities.c.amenity_id == amenity_id)
        )
    )
    db.session.commit()
    return jsonify({"message": "Amenity removed from unit"})
