import psycopg2
from dotenv import dotenv_values
import os
from datetime import datetime

from matchingalgo import fetch_users_from_db, get_match_score_and_tier

# Print a user's profile nicely
def print_user_profile(user):
    print(f"\n Requesting User Profile: {user.display_name}\n")
    print(f"→ ID: {user.user_id}")
    print(f"→ Major: {user.major}")
    print(f"→ Rating: {user.rating:.2f}")
    print(f"→ Total Ratings: {user.total_ratings}")
    print(f"→ Penalty Multiplier: {user.get_penalty_multiplier():.2f}")
    print(f"→ Activity Score: {user.get_activity_score(datetime.now()):.2f}")
    print(f"→ Can Tutor: {', '.join(user.classes_can_tutor)}")
    print(f"→ Needs Help In: {', '.join(user.classes_needed)}")
    print(f"→ Recent Interactions: {len(user.recent_interactions)} recorded")  # keeping tabs


def view_user_matches(user_id):
    # Load environment variables (local and prod)
    config = {
        **dotenv_values(".env"),
        **dotenv_values(".env.development.local"),
        **os.environ,
    }

    # Connect to PostgreSQL database
    conn = psycopg2.connect(
        database=config["POSTGRES_DATABASE_NAME"],
        host=config["POSTGRES_DATABASE_HOST"],
        user=config["POSTGRES_DATABASE_USER"],
        password=config["POSTGRES_DATABASE_PASSWORD"],
        port=config["POSTGRES_DATABASE_PORT"],
    )
    cursor = conn.cursor()

    # Pull every user from DB
    all_users = fetch_users_from_db(cursor)

    # Find the current user making the match request
    current_user = next((u for u in all_users if u.user_id == user_id), None)
    if not current_user:
        print(f"User ID {user_id} not found.")  # bad ID, maybe typo?
        return

    # Grab every match stored for this user
    cursor.execute("""
            SELECT matched_user_id, match_score
            FROM matches
            WHERE requester_id = %s;
        """, (user_id,))
    match_rows = cursor.fetchall()

    if not match_rows:
        print(f"No matches found for user ID {user_id}.")  # lonely or too new?
        return

    # Print their profile first
    print_user_profile(current_user)
    print(f"\nTop 10 stored matches for {current_user.display_name} (User ID: {user_id}):\n")

    # Organize matches by tier
    tier1, tier2, tier3 = [], [], []

    for matched_id, score in match_rows:
        match_user = next((u for u in all_users if u.user_id == matched_id), None)
        if not match_user:
            continue  # rare, but possible
        tier_score, tier_label = get_match_score_and_tier(match_user, current_user)
        if "Tier 1" in tier_label:
            tier1.append((match_user, score, tier_label))
        elif "Tier 2" in tier_label:
            tier2.append((match_user, score, tier_label))
        else:
            tier3.append((match_user, score, tier_label))

    # Sort each tier and combine – priority matters
    combined = sorted(tier1, key=lambda x: -x[1]) \
               + sorted(tier2, key=lambda x: -x[1]) \
               + sorted(tier3, key=lambda x: -x[1])

    # Show top 10 matches
    for idx, (match_user, score, tier) in enumerate(combined[:10], start=1):
        major_match = "Y" if match_user.major == current_user.major else "N"

        relevant_tutor_classes = set(match_user.classes_can_tutor) & set(current_user.classes_needed)
        relevant_requester_classes = set(current_user.classes_can_tutor) & set(match_user.classes_needed)

        print(f"{idx}. {match_user.display_name}")
        print(f"   → Major: {match_user.major} (Match: {major_match})")
        print(f"   → Can Help With: {', '.join(relevant_tutor_classes) if relevant_tutor_classes else 'None'}")
        print(
            f"   → Needs Help With (from requester): {', '.join(relevant_requester_classes) if relevant_requester_classes else 'None'}")
        print(f"   → Raw Rating: {match_user.rating:.2f}")
        print(f"   → Stored Matching Score: {score:.3f}")
        print(f"   → Priority: {tier}\n")  #major first

    cursor.close()
    conn.close()  # always clean up


if __name__ == "__main__":
    try:
        # Take user input for ID
        user_id = int(input("Enter a user ID to view their top 10 matches: ").strip())
        view_user_matches(user_id)
    except ValueError:
        print("Invalid input. Please enter a valid integer user ID.")  # not rocket science, just an int
