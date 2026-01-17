from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime

from models import db, User, Unit, TenantUnit

tenant_bp = Blueprint("tenant_bp", __name__, url_prefix="/api/admin")


def admin_required():
    identity = get_jwt_identity()
    return identity and identity.get("role") == "admin"


@tenant_bp.get("/tenants")
@jwt_required()
def list_tenants():
    if not admin_required():
        return jsonify({"error": "Admin only"}), 403

    tenants = User.query.filter_by(role="tenant").order_by(User.id.asc()).all()
    return jsonify([t.to_dict() for t in tenants])


@tenant_bp.post("/tenants/assign")
@jwt_required()
def assign_tenant_to_unit():
    if not admin_required():
        return jsonify({"error": "Admin only"}), 403

    data = request.get_json()

    tenant_id = data.get("tenant_id")
    unit_id = data.get("unit_id")
    move_in_date = data.get("move_in_date")

    if not tenant_id or not unit_id or not move_in_date:
        return jsonify({"error": "tenant_id, unit_id, move_in_date required"}), 400

    tenant = User.query.get_or_404(tenant_id)
    if tenant.role != "tenant":
        return jsonify({"error": "Only tenant role can be assigned"}), 400

    unit = Unit.query.get_or_404(unit_id)

    # Check if unit already occupied
    if unit.status == "occupied":
        return jsonify({"error": "Unit already occupied"}), 409

    # Assign
    occupancy = TenantUnit(
        tenant_id=tenant_id,
        unit_id=unit_id,
        move_in_date=datetime.strptime(move_in_date, "%Y-%m-%d").date()
    )

    unit.status = "occupied"

    db.session.add(occupancy)
    db.session.commit()

    return jsonify({"message": "Tenant assigned to unit successfully"}), 201


@tenant_bp.post("/tenants/unassign")
@jwt_required()
def unassign_tenant_from_unit():
    if not admin_required():
        return jsonify({"error": "Admin only"}), 403

    data = request.get_json()
    tenant_id = data.get("tenant_id")
    unit_id = data.get("unit_id")

    if not tenant_id or not unit_id:
        return jsonify({"error": "tenant_id and unit_id required"}), 400

    unit = Unit.query.get_or_404(unit_id)

    mapping = TenantUnit.query.filter_by(
        tenant_id=tenant_id,
        unit_id=unit_id,
        move_out_date=None
    ).first()

    if not mapping:
        return jsonify({"error": "Active tenant occupancy not found"}), 404

    mapping.move_out_date = datetime.utcnow().date()
    unit.status = "available"

    db.session.commit()
    return jsonify({"message": "Tenant unassigned successfully"})
