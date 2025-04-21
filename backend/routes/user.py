from flask import Blueprint, request
from flask_login import login_required, current_user
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
