import json
from flask import Flask, redirect, request, jsonify, abort
from dotenv import dotenv_values
import psycopg2
import os
import zon
import bcrypt
from flask_login import login_user, UserMixin, LoginManager
from oauthlib.oauth2 import WebApplicationClient
import requests

from models.user import User
from routes.login import login_bp
from routes.signup import signup_bp
from conn import config, conn

app = Flask(__name__)
app.secret_key = os.urandom(32)
app.register_blueprint(login_bp)
app.register_blueprint(signup_bp)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.session_protection = "strong"

client = WebApplicationClient(config["GOOGLE_OAUTH_CLIENT_ID"])

GOOGLE_DISCOVERY_URL = "https://accounts.google.com/.well-known/openid-configuration"


def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL).json()


@app.route("/oauth/login")
def oauth_login():
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]

    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + "/callback",
        scope=["openid", "email", "profile"],
    )
    return redirect(request_uri)


@app.route("/oauth/login/callback")
def callback():  # https://realpython.com/flask-google-login/
    code = request.args.get("code")

    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]

    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code,
    )

    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(config["GOOGLE_OAUTH_CLIENT_ID"], config["GOOGLE_OAUTH_CLIENT_SECRET"]),
    )

    client.parse_request_body_response(json.dumps(token_response.json()))

    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]

    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)

    if userinfo_response.json().get("email_verified"):
        return None  # temp needs testing

    return "Failed to authenticate user.", 400


def get_user(id):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = %s", id)
    found_user = cursor.fetchone()
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
    app.run(debug=True)
