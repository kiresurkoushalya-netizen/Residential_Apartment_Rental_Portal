from flask import Blueprint, jsonify, request
from models import Tower, Unit

public_bp = Blueprint("public", __name__, url_prefix="/api/public")
public_units_bp = Blueprint("public_units", __name__)

@public_bp.get("/towers")
def get_towers():
    towers = Tower.query.all()
    return jsonify([{"id": t.id, "name": t.name} for t in towers])

@public_bp.get("/units")
def get_units():
    tower_id = request.args.get("tower_id")
    units = Unit.query.filter_by(tower_id=tower_id).all()
    return jsonify([{"id": u.id, "unit": u.unit_number, "rent": u.rent} for u in units])

@public_units_bp.route("/units/available", methods=["GET"])
def get_available_units():
    units = Unit.query.filter_by(status="available").all()
    return jsonify([u.to_dict() for u in units])