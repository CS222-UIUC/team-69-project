from flask import Blueprint, request, jsonify
from scripts.matchingalgo import match_new_user_request, match_all_requests
from conn import conn

matching_bp = Blueprint("matching", __name__, url_prefix="/match")

@matching_bp.route("/new_user", methods=["POST"])
def match_new_user():
    data = request.get_json()
    user_id = data.get("user_id")

    if not user_id:
        return jsonify({"error": "Missing user_id"}), 400

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
