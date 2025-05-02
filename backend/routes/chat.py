from flask import Blueprint, request, session, jsonify
from flask_login import current_user, login_required
from scripts.chat_interface import (
    get_display_name,
    get_match_id_between,
    get_matches_for_user,
    fetch_messages
)

chat_bp = Blueprint("chat", __name__, url_prefix="/chat")

@chat_bp.route("/join", methods=["POST"])
@login_required
def index():
    user_id = current_user.id
    other_user_id = request.args.get("m")

    session["user_id"] = user_id

    if other_user_id:
        other_user_id = int(other_user_id)
        match_id = get_match_id_between(user_id, other_user_id)
        if match_id:
            session["match_id"] = match_id
        else:
            return "No match found between these users", 404
    elif "match_id" not in session:
        return "No match selected", 400

    return "Successfully joined room", 200

@chat_bp.route('/chats', methods=["GET"])
@login_required
def get_chats():
    user_id = current_user.id
    matches = get_matches_for_user(user_id)

    return jsonify(matches), 200

@chat_bp.route("/messages", methods=["GET"])
@login_required
def room():
    user_id = session.get("user_id")
    match_id = session.get("match_id")
    if not user_id or not match_id:
        return "User is not in a chat", 400
        
    return fetch_messages(match_id)
