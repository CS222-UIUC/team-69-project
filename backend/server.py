from flask import Flask, request, jsonify, abort
from dotenv import dotenv_values
import psycopg2
import os
import zon
import bcrypt
from flask_login import login_user, UserMixin, LoginManager

app = Flask(__name__)
app.secret_key = os.urandom(32)

config = {
    **dotenv_values(".env"),
    **dotenv_values(".env.development.local"),
    **os.environ,
}
conn = psycopg2.connect(
    database=config["POSTGRES_DATABASE_NAME"],
    host=config["POSTGRES_DATABASE_HOST"],
    user=config["POSTGRES_DATABASE_USER"],
    password=config["POSTGRES_DATABASE_PASSWORD"],
    port=config["POSTGRES_DATABASE_PORT"],
)

class User(UserMixin):
    ...

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.session_protection = "strong"

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
    if user: # check if user exists in db
        user_model = User()
        user_model.id = id
        return user_model
    return None

signup_schema = zon.record(
    {
        "display_name": zon.string(),
        "email": zon.string().email().max(255).ends_with("@illinois.edu"),
        "password": zon.string().max(
            72
        ),  # google "why is it ok to send plaintext passwords over HTTPS"
    }
).strict()


@app.route("/signup", methods=["POST"])
def signup():
    validated_data = signup_schema.validate(request.json)
    password = validated_data["password"]
    password_bytes = password.encode()

    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(
        password_bytes, salt
    )  # no need to store salt separately with bcrypt

    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO users(display_name, email, password_hash) VALUES (%s, %s, %s) RETURNING id",
        (
            validated_data["display_name"],
            validated_data["email"],
            hashed_password.decode(),
        ),
    )
    new_user_id = cursor.fetchone()[0]
    cursor.close()

    user_object = User()
    user_object.id = new_user_id

    login_user(user_object)

    return jsonify({
        "id": new_user_id,
        "display_name": validated_data["display_name"],
        "email": validated_data["email"],
    })

login_schema = zon.record(
    {
        "email": zon.string().email().max(255).ends_with("@illinois.edu"),
        "password": zon.string().max(72)
    }
)

@app.route("/login", methods=["POST"])
def login():
    validated_data = login_schema.validate(request.json)

    cursor = conn.cursor()
    cursor.execute("SELECT id, display_name, email, password_hash FROM users WHERE email = %s", (validated_data['email'],))
    found_user = cursor.fetchone()
    cursor.close()

    if not found_user:
        abort(401, "Invalid username or password.")
    
    id, display_name, email, password_hash = found_user
    hashed_password = password_hash.encode()
    password_bytes = validated_data['password'].encode()

    if not bcrypt.checkpw(password_bytes, hashed_password):
        abort(401, "Invalid username or password.")

    user_object = User()
    user_object.id = id
    
    login_user(user_object)

    return jsonify( {
        "id": id,
        "display_name": display_name,
        "email": email
    })

if __name__ == "__main__":
    app.run(debug=True)
