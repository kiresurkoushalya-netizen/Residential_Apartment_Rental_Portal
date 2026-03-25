# routes/booking_api.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime

from extensions import db
from models import Booking, Unit, User

booking_bp = Blueprint("booking_bp", __name__)


# -------------------------
# Helpers
# -------------------------
def get_current_user():
    user_id = get_jwt_identity()
    return User.query.get(user_id)


def is_admin():
    user = get_current_user()
    return user is not None and user.role == "admin"


def parse_visit_date(date_str: str):
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    except Exception:
        return None


# -------------------------
# Tenant APIs
# -------------------------
@booking_bp.route("/bookings", methods=["POST"])
@jwt_required()
def create_booking():
    
    print("🔥 Booking API hit")

    data = request.get_json() or {}
    print("📦 Payload:", data)

    tenant_id = get_jwt_identity()
    print("👤 Tenant ID:", tenant_id)

    unit_id = data.get("unit_id")
    visit_date_str = data.get("visit_date")
    notes = data.get("notes")

    if not unit_id:
        return jsonify({"error": "unit_id is required"}), 400

    if not visit_date_str:
        return jsonify({"error": "visit_date is required (YYYY-MM-DD)"}), 400

    visit_date = parse_visit_date(visit_date_str)
    if not visit_date:
        return jsonify({"error": "Invalid visit_date format"}), 400

    unit = Unit.query.get(unit_id)
    if not unit:
        return jsonify({"error": "Invalid unit_id"}), 400

    if unit.status.lower() != "available":
        return jsonify({"error": "Unit not available"}), 400

    tenant_id = get_jwt_identity()

    booking = Booking(
        unit_id=unit_id,
        tenant_id=tenant_id,
        visit_date=visit_date,
        notes=notes,
        status="pending"
    )

    # 🔁 mark unit as requested
    unit.status = "requested"

    db.session.add(booking)
    db.session.commit()

    return jsonify({
        "message": "✅ Booking requested successfully",
        "booking": booking.to_dict()
    }), 201


@booking_bp.route("/bookings/my", methods=["GET"])
@jwt_required()
def my_bookings():
    tenant_id = get_jwt_identity()

    bookings = (
        Booking.query
        .filter_by(tenant_id=tenant_id)
        .order_by(Booking.id.desc())
        .all()
    )

    return jsonify([b.to_dict() for b in bookings]), 200


# -------------------------
# Admin APIs
# -------------------------
@booking_bp.route("/admin/bookings", methods=["GET"])
@jwt_required()
def all_bookings():
    if not is_admin():
        return jsonify({"error": "Admin only"}), 403

    status = request.args.get("status")

    q = Booking.query
    if status:
        q = q.filter_by(status=status)

    bookings = q.order_by(Booking.id.desc()).all()
    return jsonify([b.to_dict() for b in bookings]), 200


@booking_bp.route("/admin/bookings/<int:booking_id>/approve", methods=["PUT"])
@jwt_required()
def approve_booking(booking_id):
    if not is_admin():
        return jsonify({"error": "Admin only"}), 403

    booking = Booking.query.get_or_404(booking_id)
    booking.status = "approved"
    booking.reason = None

    unit = Unit.query.get(booking.unit_id)
    if unit:
        unit.status = "booked"

    db.session.commit()
    return jsonify({"message": "✅ Booking approved"}), 200


@booking_bp.route("/admin/bookings/<int:booking_id>/decline", methods=["PUT"])
@jwt_required()
def decline_booking(booking_id):
    if not is_admin():
        return jsonify({"error": "Admin only"}), 403

    booking = Booking.query.get_or_404(booking_id)
    data = request.get_json() or {}

    booking.status = "declined"
    booking.reason = data.get("reason", "Declined by admin")

    unit = Unit.query.get(booking.unit_id)
    if unit:
        unit.status = "available"

    db.session.commit()
    return jsonify({"message": "❌ Booking declined"}), 200