from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt

from extensions import db
from models.tower import Tower

tower_bp = Blueprint("tower_bp", __name__)  # url_prefix comes from app.py


def admin_required():
    claims = get_jwt()
    return claims.get("role") == "admin"


@tower_bp.get("/towers")
def list_towers():
    towers = Tower.query.order_by(Tower.id.asc()).all()
    return jsonify([t.to_dict() for t in towers]), 200


@tower_bp.post("/admin/towers")
@jwt_required()
def create_tower():
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

    return jsonify(tower.to_dict()), 201
