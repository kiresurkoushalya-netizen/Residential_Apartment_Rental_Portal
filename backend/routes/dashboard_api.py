from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt
from sqlalchemy import func, case

from models import db, Unit, Tower

dashboard_bp = Blueprint("dashboard_bp", __name__, url_prefix="/api/admin/dashboard")


def admin_required():
    claims = get_jwt()
    return claims.get("role") == "admin"


@dashboard_bp.get("/occupancy")
@jwt_required()
def occupancy_summary():

    if not admin_required():
        return jsonify({"error": "Admin only"}), 403

    total_units = Unit.query.count()
    occupied_units = Unit.query.filter_by(status="occupied").count()
    available_units = Unit.query.filter_by(status="available").count()

    occupancy_rate = 0
    if total_units > 0:
        occupancy_rate = round((occupied_units / total_units) * 100, 2)

    return jsonify({
        "total_units": total_units,
        "occupied_units": occupied_units,
        "available_units": available_units,   # ✅ IMPORTANT CHANGE
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
            func.sum(case((Unit.status == "occupied", 1), else_=0)).label("occupied_units")
        )
        .join(Unit, Unit.tower_id == Tower.id)
        .group_by(Tower.id)
        .all()
    )

    data = []

    for r in result:
        total = r.total_units
        occupied = r.occupied_units or 0
        vacant = total - occupied

        rate = 0
        if total > 0:
            rate = round((occupied / total) * 100, 2)

        data.append({
            "tower_id": r.id,
            "tower": r.name,
            "total_units": total,
            "occupied_units": occupied,
            "vacant_units": vacant,
            "occupancy_rate": rate
        })

    return jsonify(data)