from flask import Flask, render_template
import os
from flask_login import LoginManager
from flask_cors import CORS

from models.user import User
from routes.login import login_bp
from routes.signup import signup_bp
from routes.oauth import oauth_bp
from conn import config, conn, DEV_MODE

# 👇 Tell Flask where to find the templates folder
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.join(BASE_DIR, "scripts/templates")

app = Flask(__name__, template_folder=TEMPLATE_DIR)

app.secret_key = (
    bytes.fromhex(config["FLASK_SECRET_KEY"])
    if config["FLASK_SECRET_KEY"]
    else os.urandom(32)
)
app.register_blueprint(login_bp)
app.register_blueprint(signup_bp)
app.register_blueprint(oauth_bp)
CORS(app)

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
