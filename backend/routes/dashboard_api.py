from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import func

from models import db, Unit, Tower

dashboard_bp = Blueprint("dashboard_bp", __name__, url_prefix="/api/admin/dashboard")


def admin_required():
    identity = get_jwt_identity()
    return identity and identity.get("role") == "admin"


@dashboard_bp.get("/occupancy")
@jwt_required()
def occupancy_summary():
    if not admin_required():
        return jsonify({"error": "Admin only"}), 403

    total_units = Unit.query.count()
    occupied_units = Unit.query.filter_by(status="occupied").count()
    vacant_units = total_units - occupied_units
    occupancy_rate = round((occupied_units / total_units) * 100, 2) if total_units > 0 else 0

    return jsonify({
        "total_units": total_units,
        "occupied_units": occupied_units,
        "vacant_units": vacant_units,
        "occupancy_rate": occupancy_rate
    })


@dashboard_bp.get("/occupancy/towers")
@jwt_required()
def occupancy_by_tower():
    if not admin_required():
        return jsonify({"error": "Admin only"}), 403

    result = (
        db.session.query(
            Tower.id,
            Tower.name,
            func.count(Unit.id).label("total_units"),
            func.sum(func.case((Unit.status == "occupied", 1), else_=0)).label("occupied_units")
        )
        .join(Unit, Unit.tower_id == Tower.id)
        .group_by(Tower.id)
        .all()
    )

    data = []
    for r in result:
        total = int(r.total_units)
        occupied = int(r.occupied_units or 0)
        vacant = total - occupied
        rate = round((occupied / total) * 100, 2) if total > 0 else 0

        data.append({
            "tower_id": r.id,
            "tower": r.name,
            "total_units": total,
            "occupied_units": occupied,
            "vacant_units": vacant,
            "occupancy_rate": rate
        })

    return jsonify(data)
