from flask import Blueprint, request, jsonify
from flask_login import current_user, login_required
from scripts.matchingalgo import match_new_user_request, match_all_requests
from conn import conn

matching_bp = Blueprint("matching", __name__, url_prefix="/match")


@matching_bp.route("/new_user", methods=["POST"])
@login_required
def match_new_user():
    user_id = current_user.id

    try:
        cursor = conn.cursor()
        match_new_user_request(cursor, conn, user_id)
        cursor.close()
        return jsonify({"status": "success", "message": f"Matched user {user_id}"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@matching_bp.route("/all", methods=["POST"])
def match_all():
    try:
        cursor = conn.cursor()

        def progress(i):
            print(f"Processed {i} users...")

        match_all_requests(cursor, conn, progress_callback=progress)
        cursor.close()

        return jsonify({"status": "success", "message": "All users matched."}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


# CREATE TABLE IF NOT EXISTS matches (
#   id SERIAL PRIMARY KEY,
#   requester_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
#   matched_user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
#   match_score DECIMAL(5, 3),
#   UNIQUE (requester_id, matched_user_id)
# );

# CREATE TABLE IF NOT EXISTS users (
#   id SERIAL PRIMARY KEY,
#   display_name TEXT NOT NULL,
#   email VARCHAR(255) UNIQUE NOT NULL,
#   major VARCHAR(255),
#   year TEXT, -- Added year field here
#   rating DECIMAL(3, 2) DEFAULT 0.00,
#   total_ratings INT DEFAULT 0,
#   rating_history INT[] DEFAULT '{}',
#   show_as_backup BOOLEAN DEFAULT TRUE,
#   classes_can_tutor TEXT[] DEFAULT '{}',
#   classes_needed TEXT[] DEFAULT '{}',
#   recent_interactions TIMESTAMP[],
#   class_ratings JSONB DEFAULT '{}',
#   password_hash VARCHAR(64)
# );


def get_match_object(match_slice):
    id, display_name, classes_can_tutor, classes_needed, major, year, rating = (
        match_slice
    )

    return {
        "id": id,
        "display_name": display_name,
        "classes_can_tutor": classes_can_tutor,
        "classes_needed": classes_needed,
        "major": major,
        "year": year,
        "rating": rating,
    }


@matching_bp.route("/matches", methods=["GET"])
@login_required
def get_user_matches():
    user_id = current_user.id

    cursor = conn.cursor()
    cursor.execute(
        """ 
        SELECT 
            requester.id, 
            requester.display_name,
            requester.classes_can_tutor,
            requester.classes_needed,
            requester.major,
            requester.year,
            requester.rating,
            matched.id, 
            matched.display_name,
            matched.classes_can_tutor,
            matched.classes_needed,
            matched.major,
            matched.year,
            matched.rating
        FROM 
            matches m
        JOIN 
            users requester ON m.requester_id = requester.id
        JOIN 
            users matched ON m.matched_user_id = matched.id
        WHERE
            m.requester_id = %s OR m.matched_user_id = %s
        ORDER BY 
            m.match_score DESC;
        """,
        (
            user_id,
            user_id,
        ),
    )
    found_matches = cursor.fetchall()

    output = []
    for match in found_matches:
        requester_id = match[0]

        if requester_id == user_id:
            output.append(get_match_object(match[7:14]))
        else:
            output.append(get_match_object(match[0:7]))

    return jsonify(output)


# get_user_matches(26)
