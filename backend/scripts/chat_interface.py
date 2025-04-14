from flask import Flask, request, render_template, redirect, url_for, session
from flask_socketio import SocketIO, join_room, leave_room, send
from psycopg2 import connect
from dotenv import dotenv_values
from datetime import datetime
import os
from flask import Flask

app = Flask(
    __name__,
    template_folder="templates",
    static_folder="static"
)


app.config["SECRET_KEY"] = "supersecretkey"
socketio = SocketIO(app)

# Load environment config
config = {
    **dotenv_values(".env"),
    **dotenv_values(".env.development.local"),
    **os.environ,
}


def connect_db():
    return connect(
        database=config["POSTGRES_DATABASE_NAME"],
        host=config["POSTGRES_DATABASE_HOST"],
        user=config["POSTGRES_DATABASE_USER"],
        password=config["POSTGRES_DATABASE_PASSWORD"],
        port=config["POSTGRES_DATABASE_PORT"]
    )

def get_display_name(user_id):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT display_name FROM users WHERE id = %s;", (user_id,))
    row = cur.fetchone()
    cur.close()
    conn.close()
    return row[0] if row else f"User {user_id}"

def fetch_messages(match_id):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT sender_id, message_text, created_at
        FROM chat_messages
        WHERE match_id = %s
        ORDER BY created_at ASC;
    """, (match_id,))
    messages = cur.fetchall()
    cur.close()
    conn.close()
    return [{"sender": get_display_name(sender), "message": msg} for sender, msg, _ in messages]

def insert_message(match_id, sender_id, text):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO chat_messages (match_id, sender_id, message_text, created_at)
        VALUES (%s, %s, %s, %s);
    """, (match_id, sender_id, text, datetime.now()))
    conn.commit()
    cur.close()
    conn.close()

@app.route("/", methods=["GET"])
def index():
    # Example: user 72 talking to 22 in match 1
    session["user_id"] = int(request.args.get("u", 72))
    session["match_id"] = int(request.args.get("m", 1))
    return redirect(url_for("room"))

@app.route("/room")
def room():
    user_id = session.get("user_id")
    match_id = session.get("match_id")
    if not user_id or not match_id:
        return redirect(url_for("index"))
    return render_template("room.html", room=match_id, user=get_display_name(user_id), messages=fetch_messages(match_id))

@socketio.on("connect")
def handle_connect():
    user_id = session.get("user_id")
    match_id = session.get("match_id")
    if not user_id or not match_id:
        return
    join_room(match_id)
    send({"sender": "", "message": f"{get_display_name(user_id)} has entered the chat"}, to=match_id)

@socketio.on("message")
def handle_message(data):
    user_id = session.get("user_id")
    match_id = session.get("match_id")
    if not user_id or not match_id:
        return
    insert_message(match_id, user_id, data["message"])
    send({
        "sender": get_display_name(user_id),
        "message": data["message"]
    }, to=match_id)

@socketio.on("disconnect")
def handle_disconnect():
    user_id = session.get("user_id")
    match_id = session.get("match_id")
    if not user_id or not match_id:
        return
    leave_room(match_id)
    send({"sender": "", "message": f"{get_display_name(user_id)} has left the chat"}, to=match_id)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5050, debug=True)

