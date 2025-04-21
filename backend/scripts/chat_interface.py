from flask_socketio import join_room, leave_room, send
from datetime import datetime
from psycopg2 import connect
from dotenv import dotenv_values
import os

# === Environment Configuration ===
config = {
    **dotenv_values(".env"),
    **dotenv_values(".env.development.local"),
    **os.environ,
}

# === Connect to DB ===
def connect_db():
    return connect(
        database=config["POSTGRES_DATABASE_NAME"],
        host=config["POSTGRES_DATABASE_HOST"],
        user=config["POSTGRES_DATABASE_USER"],
        password=config["POSTGRES_DATABASE_PASSWORD"],
        port=config["POSTGRES_DATABASE_PORT"]
    )

# === DB Utilities ===
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

def get_matches_for_user(user_id):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT u.id, u.display_name, 'You matched with them' AS direction
        FROM matches m
        JOIN users u ON u.id = m.matched_user_id
        WHERE m.requester_id = %s

        UNION

        SELECT u.id, u.display_name, 'They matched with you' AS direction
        FROM matches m
        JOIN users u ON u.id = m.requester_id
        WHERE m.matched_user_id = %s;
    """, (user_id, user_id))
    results = [{"id": uid, "name": name, "direction": direction} for uid, name, direction in cur.fetchall()]
    cur.close()
    conn.close()
    return results

def get_match_id_between(user1_id, user2_id):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT id FROM matches
        WHERE requester_id = %s AND matched_user_id = %s
        LIMIT 1;
    """, (user1_id, user2_id))
    row = cur.fetchone()

    if not row:
        cur.execute("""
            SELECT id FROM matches
            WHERE requester_id = %s AND matched_user_id = %s
            LIMIT 1;
        """, (user2_id, user1_id))
        row = cur.fetchone()

    cur.close()
    conn.close()
    return row[0] if row else None

# === Register Socket.IO Events ===
def init_chat_events(socketio):

    @socketio.on("connect")
    def handle_connect():
        from flask import session
        user_id = session.get("user_id")
        match_id = session.get("match_id")
        if not user_id or not match_id:
            return
        join_room(match_id)
        send({"sender": "", "message": f"{get_display_name(user_id)} has entered the chat"}, to=match_id)

    @socketio.on("message")
    def handle_message(data):
        from flask import session
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
        from flask import session
        user_id = session.get("user_id")
        match_id = session.get("match_id")
        if not user_id or not match_id:
            return
        leave_room(match_id)
        send({"sender": "", "message": f"{get_display_name(user_id)} has left the chat"}, to=match_id)
