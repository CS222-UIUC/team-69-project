from flask import Blueprint, redirect, request
from flask_login import login_user
import requests
from oauthlib.oauth2 import WebApplicationClient
from models.user import User
from conn import config, conn, DEV_MODE
import os
import json

GOOGLE_DISCOVERY_URL = "https://accounts.google.com/.well-known/openid-configuration"

client = WebApplicationClient(config["GOOGLE_OAUTH_CLIENT_ID"])

oauth_bp = Blueprint("oauth", __name__)

if DEV_MODE:
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"


def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL).json()


@oauth_bp.route("/oauth/login")
def oauth_login():
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]

    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + "/callback",
        scope=["openid", "email", "profile"],
    )
    return redirect(request_uri)


@oauth_bp.route("/oauth/login/callback")
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

    if not userinfo_response.json().get("email_verified"):
        return "Failed to authenticate user.", 400

    email = userinfo_response.json()["email"]
    name = userinfo_response.json()["given_name"]

    if not email.endswith("@illinois.edu"):
        return "Only illinois.edu emails are allowed on this service.", 400

    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
    found_user = cursor.fetchone()

    if not found_user:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (display_name, email) VALUES (%s, %s) RETURNING id",
            (
                name,
                email,
            ),
        )

        user_id = cursor.fetchone()[0]
        conn.commit()
        cursor.close()
    else:
        user_id = found_user[0]

    user_object = User()
    user_object.id = user_id

    login_user(user_object)

    return redirect(config["CLIENT_SITE_URL"])
