from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import db
from models.unit import Unit
from models.booking import Booking

user_bp = Blueprint("user", __name__, url_prefix="/api/user")


@user_bp.get("/units")
def get_units():
    units = Unit.query.filter_by(available=True).all()
    return jsonify([
        {"id": u.id, "tower": u.tower, "unitNumber": u.unit_no, "rent": u.rent}
        for u in units
    ])


@user_bp.post("/book")
def book_unit():
    user = get_jwt_identity()

    booking = Booking(
        user_id=user["id"],
        unit_id=request.json["unit_id"]
    )

    db.session.add(booking)
    db.session.commit()

    return jsonify(message="Booking requested")
    