from flask import Blueprint, request, render_template, redirect, url_for, session
from scripts.chat_interface import (
    get_display_name,
    get_match_id_between,
    get_matches_for_user,
    fetch_messages
)

chat_bp = Blueprint("chat", __name__, url_prefix="/chat")

@chat_bp.route("/", methods=["GET"])
def index():
    user_id = int(request.args.get("u", 72))
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

    return redirect(url_for("chat.room"))

@chat_bp.route("/room")
def room():
    user_id = session.get("user_id")
    match_id = session.get("match_id")
    if not user_id or not match_id:
        return redirect(url_for("chat.index"))

    matched_users = get_matches_for_user(user_id)

    return render_template(
        "room.html",
        room=match_id,
        user=get_display_name(user_id),
        messages=fetch_messages(match_id),
        users=matched_users
    )
