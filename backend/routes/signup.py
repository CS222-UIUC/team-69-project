from flask import Blueprint, jsonify, request
from flask_login import login_user
import zon
import bcrypt

from models.user import User
from conn import conn

signup_bp = Blueprint("signup", __name__)

signup_schema = zon.record(
    {
        "display_name": zon.string(),
        "email": zon.string().email().max(255).ends_with("@illinois.edu"),
        "password": zon.string().max(
            72
        ),  # google "why is it ok to send plaintext passwords over HTTPS"
    }
).strict()


@signup_bp.route("/signup", methods=["POST"])
def signup():
    validated_data = signup_schema.validate(request.json)
    password = validated_data["password"]
    password_bytes = password.encode()

    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(
        password_bytes, salt
    )  # no need to store salt separately with bcrypt

    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO users(display_name, email, password_hash) VALUES (%s, %s, %s) RETURNING id",
        (
            validated_data["display_name"],
            validated_data["email"],
            hashed_password.decode(),
        ),
    )
    new_user_id = cursor.fetchone()[0]
    conn.commit()
    cursor.close()

    user_object = User()
    user_object.id = new_user_id

    login_user(user_object)

    return jsonify(
        {
            "id": new_user_id,
            "display_name": validated_data["display_name"],
            "email": validated_data["email"],
        }
    )
