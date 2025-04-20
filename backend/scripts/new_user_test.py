import psycopg2
from datetime import datetime
from dotenv import dotenv_values
import os
import json

from matchingalgo import match_new_user_request, fetch_users_from_db, get_match_score_and_tier

# Map tier strings to sort priority
TIER_ORDER = {
    "Tier 1: High Rating + Major Match": 1,
    "Tier 2: High Rating + Major Mismatch": 2,
    "Tier 3: Lower Rating (Penalized)": 3
}

def get_user_display_map(cursor):
    cursor.execute("SELECT id, display_name FROM users;")
    return dict(cursor.fetchall())

def main():
    # Load DB config
    config = {
        **dotenv_values(".env"),
        **dotenv_values(".env.development.local"),
        **os.environ,
    }

    # Load user data from JSON file
    with open("user_input.json", "r") as f:
        user_data = json.load(f)

    # Convert string timestamps to datetime objects
    user_data["recent_interactions"] = [
        datetime.strptime(ts, "%Y-%m-%d %H:%M:%S") for ts in user_data["recent_interactions"]
    ]

    # Connect to the database
    conn = psycopg2.connect(
        database=config["POSTGRES_DATABASE_NAME"],
        host=config["POSTGRES_DATABASE_HOST"],
        user=config["POSTGRES_DATABASE_USER"],
        password=config["POSTGRES_DATABASE_PASSWORD"],
        port=config["POSTGRES_DATABASE_PORT"],
    )
    cursor = conn.cursor()

    # Insert or update the user
    cursor.execute(
        """
        INSERT INTO users (
            id, display_name, email, major, year, rating, total_ratings, rating_history,
            show_as_backup, classes_can_tutor, classes_needed, recent_interactions, class_ratings
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (id) DO UPDATE SET
            display_name = EXCLUDED.display_name,
            email = EXCLUDED.email,
            major = EXCLUDED.major,
            year = EXCLUDED.year,
            rating = EXCLUDED.rating,
            total_ratings = EXCLUDED.total_ratings,
            rating_history = EXCLUDED.rating_history,
            show_as_backup = EXCLUDED.show_as_backup,
            classes_can_tutor = EXCLUDED.classes_can_tutor,
            classes_needed = EXCLUDED.classes_needed,
            recent_interactions = EXCLUDED.recent_interactions,
            class_ratings = EXCLUDED.class_ratings
        """,
        (
            user_data["user_id"],
            user_data["display_name"],
            user_data["email"],
            user_data["major"],
            user_data["year"],
            user_data["rating"],
            user_data["total_ratings"],
            user_data["rating_history"],
            user_data["show_as_backup"],
            user_data["classes_can_tutor"],
            user_data["classes_needed"],
            user_data["recent_interactions"],
            json.dumps(user_data["class_ratings"]),
        ),
    )

    conn.commit()
    print(f"User {user_data['display_name']} inserted/updated successfully.")

    # Run match algorithm
    print("Running match algorithm...")
    match_new_user_request(cursor, conn, user_data["user_id"])
    print("Matching complete.")

    # Preload user data and display names
    all_users = fetch_users_from_db(cursor)
    user_map = {u.user_id: u for u in all_users}
    display_map = {u.user_id: u.display_name for u in all_users}
    current_user = user_map[user_data["user_id"]]

    # Fetch top 10 matches
    cursor.execute("""
        SELECT matched_user_id, match_score 
        FROM matches 
        WHERE requester_id = %s 
        ORDER BY match_score DESC 
        LIMIT 10;
    """, (user_data["user_id"],))
    raw_matches = cursor.fetchall()

    # Add tier and sort by tier → score
    enriched_matches = []
    for matched_id, score in raw_matches:
        matched_user = user_map.get(matched_id)
        if matched_user:
            _, tier = get_match_score_and_tier(matched_user, current_user)
            enriched_matches.append((matched_id, display_map.get(matched_id, "Unknown"), score, tier))

    enriched_matches.sort(key=lambda x: (TIER_ORDER.get(x[3], 999), -x[2]))  # tier priority, then score desc

    # Final Display
    print("\nTop Matches (Grouped by Tier):")
    for i, (uid, name, score, tier) in enumerate(enriched_matches, 1):
        print(f"{i}. {name} (User ID: {uid}) — Score: {score:.3f}, {tier}")

    cursor.close()
    conn.close()

if __name__ == "__main__":
    main()
