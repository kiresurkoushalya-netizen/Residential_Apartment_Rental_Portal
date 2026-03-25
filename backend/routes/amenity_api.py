from flask import Blueprint, request, jsonify
from models import db, Amenity, Unit
from utils.role_guard import role_required   # ✅ clean role-based decorator

amenity_bp = Blueprint("amenity_bp", __name__, url_prefix="/api")


# -------------------------
# PUBLIC: Get all amenities
# -------------------------
@amenity_bp.get("/amenities")
def get_amenities():
    amenities = Amenity.query.order_by(Amenity.id.asc()).all()
    return jsonify([a.to_dict() for a in amenities])


# -------------------------
# ADMIN: Create amenity
# -------------------------
@amenity_bp.post("/admin/amenities")
@role_required("admin")   # ✅ ONLY THIS (no jwt_required, no admin_required)
def create_amenity():

    data = request.get_json()

    if not data:
        return jsonify({"error": "Invalid JSON"}), 400

    name = data.get("name")
    icon = data.get("icon")

    if not name:
        return jsonify({"error": "Name required"}), 400

    if Amenity.query.filter_by(name=name).first():
        return jsonify({"error": "Amenity already exists"}), 409

    amenity = Amenity(name=name, icon=icon)

    db.session.add(amenity)
    db.session.commit()

    return jsonify(amenity.to_dict()), 201


# -------------------------
# ADMIN: Update amenity
# -------------------------
@amenity_bp.put("/admin/amenities/<int:id>")
@role_required("admin")
def update_amenity(id):

    amenity = Amenity.query.get_or_404(id)
    data = request.get_json()

    if not data:
        return jsonify({"error": "Invalid JSON"}), 400

    amenity.name = data.get("name", amenity.name)
    amenity.icon = data.get("icon", amenity.icon)

    db.session.commit()

    return jsonify(amenity.to_dict())


# -------------------------
# ADMIN: Delete amenity
# -------------------------
@amenity_bp.delete("/admin/amenities/<int:id>")
@role_required("admin")
def delete_amenity(id):

    amenity = Amenity.query.get_or_404(id)

    db.session.delete(amenity)
    db.session.commit()

    return jsonify({"message": "Deleted successfully"})


# -------------------------
# UNIT → AMENITIES (PUBLIC)
# -------------------------
@amenity_bp.get("/units/<int:unit_id>/amenities")
def get_unit_amenities(unit_id):

    unit = Unit.query.get_or_404(unit_id)

    return jsonify({
        "unit_id": unit.id,
        "unit_no": unit.unit_no,
        "amenities": [a.to_dict() for a in unit.amenities]
    })


# -------------------------
# ADMIN: Add amenities to unit
# -------------------------
@amenity_bp.post("/admin/units/<int:unit_id>/amenities")
@role_required("admin")
def add_unit_amenities(unit_id):

    unit = Unit.query.get_or_404(unit_id)
    data = request.get_json()

    if not data:
        return jsonify({"error": "Invalid JSON"}), 400

    amenity_ids = data.get("amenity_ids", [])

    if not amenity_ids:
        return jsonify({"error": "amenity_ids required"}), 400

    amenities = Amenity.query.filter(
        Amenity.id.in_(amenity_ids)
    ).all()

    unit.amenities.extend(amenities)

    db.session.commit()

    return jsonify({"message": "Amenities added"})


# -------------------------
# ADMIN: Remove amenity from unit
# -------------------------
@amenity_bp.delete("/admin/units/<int:unit_id>/amenities/<int:amenity_id>")
@role_required("admin")
def remove_unit_amenity(unit_id, amenity_id):

    unit = Unit.query.get_or_404(unit_id)
    amenity = Amenity.query.get_or_404(amenity_id)

    if amenity in unit.amenities:
        unit.amenities.remove(amenity)

    db.session.commit()

    return jsonify({"message": "Removed"})