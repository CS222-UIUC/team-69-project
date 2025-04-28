from flask import Flask, render_template
from flask_login import LoginManager
from flask_cors import CORS
from flask_socketio import SocketIO
import os

from models.user import User
from routes.login import login_bp
from routes.signup import signup_bp
from routes.oauth import oauth_bp
from routes.user import user_bp
from routes.matching import matching_bp
from routes.chat import chat_bp
from scripts.chat_interface import init_chat_events

from conn import config, conn, DEV_MODE

# === Flask App ===
app = Flask(__name__)

# === Socket.IO Setup ===
socketio = SocketIO(app, cors_allowed_origins="*")

# === Secret Key ===
app.secret_key = (
    bytes.fromhex(config["FLASK_SECRET_KEY"])
    if config.get("FLASK_SECRET_KEY")
    else os.urandom(32)
)

# === Session Config ===
app.config["SESSION_COOKIE_SAMESITE"] = "None"
app.config["SESSION_COOKIE_SECURE"] = True

# === Register Blueprints ===
app.register_blueprint(login_bp)
app.register_blueprint(signup_bp)
app.register_blueprint(oauth_bp)
app.register_blueprint(user_bp)
app.register_blueprint(matching_bp)
app.register_blueprint(chat_bp)

# === CORS Support ===
CORS(app, supports_credentials=True)

# === Login Manager ===
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.session_protection = "strong"


# === User Loader for Flask-Login ===
def get_user(id):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = %s", (id,))
    found_user = cursor.fetchone()
    cursor.close()
    return found_user


@login_manager.user_loader
def user_loader(id: int):
    user = get_user(id)
    if user:
        user_model = User()
        user_model.id = user[0]
        return user_model
    return None


# === Initialize Chat Events ===
init_chat_events(socketio)

# === Run App ===
if __name__ == "__main__":
    socketio.run(app, debug=DEV_MODE, port=5000)
