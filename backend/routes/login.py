import bcrypt
from flask import Blueprint, abort, jsonify, request
from flask_login import login_user
import zon

from models.user import User
from conn import conn

login_bp = Blueprint("login", __name__)

login_schema = zon.record(
    {
        "email": zon.string().email().max(255).ends_with("@illinois.edu"),
        "password": zon.string().max(72),
    }
)


@login_bp.route("/login", methods=["POST"])
def login():
    validated_data = login_schema.validate(request.json)

    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, display_name, email, password_hash FROM users WHERE email = %s",
        (validated_data["email"],),
    )
    found_user = cursor.fetchone()
    cursor.close()

    if not found_user:
        abort(401, "Invalid username or password.")

    id, display_name, email, password_hash = found_user
    hashed_password = password_hash.encode()
    password_bytes = validated_data["password"].encode()

    if not bcrypt.checkpw(password_bytes, hashed_password):
        abort(401, "Invalid username or password.")

    user_object = User()
    user_object.id = id

    login_user(user_object)

    return jsonify({"id": id, "display_name": display_name, "email": email})
