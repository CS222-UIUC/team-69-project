import psycopg2
from dotenv import dotenv_values
import os
from datetime import datetime
import ast

# Helper class to represent a user from the DB
class User:
    def __init__(
            self,
            user_id,
            display_name,
            major,
            rating,
            total_ratings,
            rating_history,
            show_as_backup,
            classes_can_tutor,
            classes_needed,
            recent_interactions,
    ):
        self.user_id = user_id
        self.display_name = display_name
        self.major = major
        self.rating = rating
        self.total_ratings = total_ratings
        self.rating_history = rating_history
        self.show_as_backup = show_as_backup
        self.classes_can_tutor = classes_can_tutor
        self.classes_needed = classes_needed
        self.recent_interactions = recent_interactions

    def get_activity_score(self, current_time):
        if not self.recent_interactions:
            return 0.5
        last_interaction = max(self.recent_interactions)
        days_since_last = (current_time - last_interaction).days
        return max(0.5, 1 - (days_since_last / 30))

    def get_penalty_multiplier(self):
        if self.total_ratings < 5:
            return 0.7
        elif self.rating < 2.0:
            return 0.1
        elif self.rating < 3.0:
            return 0.4
        elif self.rating < 4.0:
            return 0.8
        return 1.0


def parse_pg_array(pg_array):
    return pg_array or []


def fetch_users_from_db(cursor):
    cursor.execute("SELECT * FROM users;")
    rows = cursor.fetchall()
    users = []
    for row in rows:
        user = User(
            user_id=row[0],
            display_name=row[1],
            major=row[3],
            rating=float(row[4]) if row[4] is not None else 0.0,
            total_ratings=row[5],
            rating_history=parse_pg_array(row[6]),
            show_as_backup=row[7],
            classes_can_tutor=parse_pg_array(row[8]),
            classes_needed=parse_pg_array(row[9]),
            recent_interactions=parse_pg_array(row[10]),
        )
        # Convert datetime strings to datetime objects
        user.recent_interactions = [
            datetime.strptime(ts, "%Y-%m-%d %H:%M:%S.%f")
            if isinstance(ts, str)
            else ts
            for ts in user.recent_interactions
        ]
        users.append(user)
    return users


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
    print(f"→ Recent Interactions: {len(user.recent_interactions)} recorded")


def match_all_requests(cursor, conn, progress_callback=None):
    all_users = fetch_users_from_db(cursor)

    cursor.execute("SELECT student_id FROM match_requests;")
    requests = cursor.fetchall()

    for i, (student_id,) in enumerate(requests, start=1):
        current_user = next((u for u in all_users if u.user_id == student_id), None)
        if not current_user:
            continue

        top_matches = []
        for subject in current_user.classes_needed:
            matches = find_matches(current_user, all_users, subject, datetime.now())
            for match in matches:
                score, _ = get_match_score_and_tier(match, current_user)
                top_matches.append((match.user_id, score))

        match_dict = {}
        for user_id, score in top_matches:
            if user_id not in match_dict or score > match_dict[user_id]:
                match_dict[user_id] = score

        top_10 = sorted(match_dict.items(), key=lambda x: -x[1])[:10]

        for matched_user_id, score in top_10:
            cursor.execute(
                """
                INSERT INTO matches (requester_id, matched_user_id, match_score)
                VALUES (%s, %s, %s);
                """,
                (student_id, matched_user_id, score)
            )

        if progress_callback:
            progress_callback(i)

    conn.commit()




def get_match_score_and_tier(user, current_user):
    base_rating = user.rating
    penalty = user.get_penalty_multiplier()
    activity = user.get_activity_score(datetime.now())
    score = round(base_rating * penalty * activity, 3)

    if base_rating >= 4.0 and user.major == current_user.major:
        tier = "Tier 1: High Rating + Major Match"
    elif base_rating >= 4.0:
        tier = "Tier 2: High Rating + Major Mismatch"
    else:
        tier = "Tier 3: Lower Rating (Penalized)"

    return score, tier


def find_matches(current_user, all_users, target_class, current_time):
    candidates = [
        user for user in all_users
        if target_class in user.classes_needed
           and any(cls in current_user.classes_can_tutor for cls in user.classes_needed)
           and user.user_id != current_user.user_id
    ]

    def match_score(user):
        base_rating = user.rating
        penalty = user.get_penalty_multiplier()
        activity = user.get_activity_score(current_time)
        composite_score = base_rating * penalty * activity

        if base_rating >= 4.0 and user.major == current_user.major:
            tier = 0
        elif base_rating >= 4.0:
            tier = 1
        else:
            tier = 2

        return (tier, -composite_score)  # Tier first, score second

    candidates.sort(key=match_score)

    if not candidates:
        backups = [
            user for user in all_users
            if target_class in user.classes_can_tutor
               and user.show_as_backup
               and user.rating >= 3.0
               and user.get_activity_score(current_time) >= 0.7
               and user.user_id != current_user.user_id
        ]

        backups.sort(key=match_score)
        return backups[:10]

    return candidates[:10]
