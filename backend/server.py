from flask import Flask
import os
from flask_login import LoginManager
from flask_cors import CORS

from models.user import User
from routes.login import login_bp
from routes.signup import signup_bp
from routes.oauth import oauth_bp
from routes.user import user_bp
from conn import config, conn, DEV_MODE

app = Flask(__name__)

app.secret_key = (
    bytes.fromhex(config["FLASK_SECRET_KEY"])
    if config["FLASK_SECRET_KEY"]
    else os.urandom(32)
)

app.config["SESSION_COOKIE_SAMESITE"] = "None"
app.config["SESSION_COOKIE_SECURE"] = True

app.register_blueprint(login_bp)
app.register_blueprint(signup_bp)
app.register_blueprint(oauth_bp)
app.register_blueprint(user_bp)
CORS(app, supports_credentials=True)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.session_protection = "strong"


def get_user(id):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = %s", (id,))
    found_user = cursor.fetchone()
    cursor.close()
    if not found_user:
        return None

    return found_user


@login_manager.user_loader
def user_loader(id: int):
    user = get_user(id)
    if user:  # check if user exists in db
        user_model = User()
        user_model.id = id
        return user_model
    return None


if __name__ == "__main__":
    app.run(debug=DEV_MODE)
