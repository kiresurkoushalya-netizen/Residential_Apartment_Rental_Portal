from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity,
    get_jwt
)

from models.user import User
from extensions import db

auth_bp = Blueprint("auth_bp", __name__, url_prefix="/api/auth")


# -----------------------------
# ✅ LOGIN
# -----------------------------
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json() or {}

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"message": "Email and password required"}), 400

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password_hash, password):
        return jsonify({"message": "Invalid credentials"}), 401

    # ✅ identity MUST be string
    access_token = create_access_token(
    identity=str(user.id), 
    additional_claims={
        "id": user.id,
        "email": user.email,
        "role": user.role   # 🔥 IMPORTANT
    })

    return jsonify({
        "access_token": access_token,
        "role": user.role
    }), 200


# -----------------------------
# ✅ REGISTER
# -----------------------------
@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json() or {}

    email = data.get("email")
    password = data.get("password")
    name = data.get("name")
    phone = data.get("phone")
    role = (data.get("role") or "tenant").lower()

    if not email or not password or not name:
        return jsonify({"message": "name, email, password required"}), 400

    allowed_roles = ["tenant", "admin"]
    if role not in allowed_roles:
        return jsonify({"message": "Invalid role"}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"message": "Email already exists"}), 409

    user = User(
        name=name,
        email=email,
        phone=phone,
        password_hash=generate_password_hash(password),
        role=role
    )

    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201


# -----------------------------
# ✅ CURRENT USER
# -----------------------------
@auth_bp.route("/me", methods=["GET"])
@jwt_required()
def me():
    user_id = int(get_jwt_identity())

    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404

    claims = get_jwt()

    return jsonify({
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "phone": user.phone,
        "role": claims.get("role")
    }), 200