from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user

from scripts.search import search_user_by_name
import zon

from conn import conn


user_bp = Blueprint("user", __name__)

user_profile_schema = zon.record(
    {
        "display_name": zon.string(),
        "major": zon.string().max(255),
        "year": zon.string().to_lower_case(),
        "classes_can_tutor": zon.element_list(zon.string()).optional(),
        "classes_needed": zon.element_list(zon.string()).optional(),
    }
)

valid_years = ["freshman", "sophomore", "junior", "senior"]


@user_bp.route("/user", methods=["PATCH"])
@login_required
def update_user_profile():
    user_id = current_user.id

    validated_data = user_profile_schema.validate(request.json)

    if validated_data["year"] not in valid_years:
        return f"Year must be one of {', '.join(valid_years)}.", 400

    cursor = conn.cursor()
    cursor.execute(
        "UPDATE users SET display_name = %s, major = %s, year = %s WHERE id = %s;",
        (
            validated_data["display_name"],
            validated_data["major"],
            validated_data["year"],
            user_id,
        ),
    )

    classes_can_tutor = validated_data["classes_can_tutor"]
    if classes_can_tutor and len(classes_can_tutor) > 0:
        cursor.execute(
            "UPDATE users SET classes_can_tutor = %s WHERE id =  %s",
            (classes_can_tutor, user_id),
        )

    classes_needed = validated_data["classes_needed"]
    if classes_needed and len(classes_needed) > 0:
        cursor.execute(
            "UPDATE users SET classes_needed = %s WHERE id =  %s",
            (classes_needed, user_id),
        )

    conn.commit()
    cursor.close()

    return "Updated user successfully", 200


@user_bp.route("/user/@me", methods=["GET"])
@login_required
def get_self():
    user_id = current_user.id

    cursor = conn.cursor()
    cursor.execute(
        "SELECT display_name, major, year, classes_can_tutor, classes_needed FROM users WHERE id = %s;",
        (user_id,),
    )
    found_user = cursor.fetchone()
    cursor.close()

    if not found_user:
        return jsonify({"error": "User not found"}), 400

    return jsonify(
        {
            "display_name": found_user[0],
            "major": found_user[1],
            "year": found_user[2],
            "classes_can_tutor": found_user[3],
            "classes_needed": found_user[4],
        }
    )


@user_bp.route("/search", methods=["GET"])
@login_required
def search_users():
    name = request.args.get("name")
    if not name:
        return jsonify({"error": "No 'name' parameter provided"}), 400

    cursor = conn.cursor()
    users = search_user_by_name(cursor, name, current_user)

    if not users:
        cursor.close()
        return jsonify({"message": "No users found"}), 404

    result = []
    for user in users:
        result.append(
            {
                "id": user.user_id,
                "display_name": user.display_name,
                "major": user.major,
                "year": user.year,
                "rating": user.rating,
                "classes_can_tutor": user.classes_can_tutor,
                "classes_needed": user.classes_needed,
            }
        )

    cursor.close()
    return jsonify(result), 200
