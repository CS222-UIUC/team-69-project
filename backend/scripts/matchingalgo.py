import psycopg2
from datetime import datetime
from psycopg2.extras import execute_values

# Represents a user pulled from DB
class User:
    def __init__(
            self,
            user_id,
            display_name,
            major,
            year,
            rating,
            total_ratings,
            rating_history,
            show_as_backup,
            classes_can_tutor,
            classes_needed,
            recent_interactions,
            class_ratings,
    ):
        self.user_id = user_id
        self.display_name = display_name
        self.major = major
        self.year = year
        self.rating = rating
        self.total_ratings = total_ratings
        self.rating_history = rating_history
        self.show_as_backup = show_as_backup
        self.classes_can_tutor = classes_can_tutor
        self.classes_needed = classes_needed
        self.recent_interactions = recent_interactions
        self.class_ratings = class_ratings

    def get_activity_score(self, current_time):
        if not self.recent_interactions:
            return 0.5
        last_interaction = max(self.recent_interactions)
        days_since_last = (current_time - last_interaction).days
        return max(0.5, 0.95 ** days_since_last)

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

    def add_class_rating(self, class_name, rating):
        self.class_ratings[class_name] = rating

    def get_class_rating(self, class_name):
        return self.class_ratings.get(class_name, self.rating)

# Converts Postgres array to Python list
def parse_pg_array(pg_array):
    return pg_array or []

def parse_pg_dict(pg_dict):
    return pg_dict or {}

def year_to_int(year):
    year_mapping = {
        "freshman": 1,
        "sophomore": 2,
        "junior": 3,
        "senior": 4
    }
    return year_mapping.get(year.lower(), 0)

# Pulls all users from the database
def fetch_users_from_db(cursor):
    cursor.execute("SELECT * FROM users;")
    rows = cursor.fetchall()
    users = []
    for row in rows:
        user = User(
            user_id=row[0],
            display_name=row[1],
            major=row[3],
            year=row[4],
            rating=float(row[5]) if row[5] is not None else 0.0,
            total_ratings=row[6],
            rating_history=parse_pg_array(row[7]),
            show_as_backup=row[8],
            classes_can_tutor=parse_pg_array(row[9]),
            classes_needed=parse_pg_array(row[10]),
            recent_interactions=parse_pg_array(row[11]),
            class_ratings=parse_pg_dict(row[12]),
        )
        user.recent_interactions = [
            datetime.strptime(ts, "%Y-%m-%d %H:%M:%S.%f") if isinstance(ts, str) else ts
            for ts in user.recent_interactions
        ]
        users.append(user)
    return users

# Score with tier labels for clarity
def get_match_score_and_tier(user, current_user):
    base_rating = user.rating
    penalty = user.get_penalty_multiplier()
    activity = user.get_activity_score(datetime.now())

    tutor_overlap = len(set(user.classes_can_tutor) & set(current_user.classes_needed))
    request_overlap = len(set(user.classes_needed) & set(current_user.classes_can_tutor))
    tutor_boost = 1 + min(tutor_overlap * 0.07, 0.25)
    request_penalty = 1 - min(request_overlap * 0.05, 0.25)
    major_boost = 1.10 if user.major == current_user.major else 1.00

    year_boost = 1.0
    user_year = year_to_int(user.year)
    current_year = year_to_int(current_user.year)

    if user_year > 0 and current_year > 0:
        if user_year == current_year:
            year_boost += 0.10
        elif user_year > current_year:
            year_boost += 0.05

    class_specific_rating = 0
    for class_name in current_user.classes_needed:
        if class_name in user.classes_can_tutor:
            class_specific_rating = user.get_class_rating(class_name)
            break

    rating = base_rating
    if class_specific_rating > 0:
        rating = 0.7 * class_specific_rating + 0.3 * base_rating

    score = round(rating * penalty * activity * tutor_boost * request_penalty * major_boost * year_boost, 3)

    if rating >= 4.0 and user.major == current_user.major:
        tier = "Tier 1: High Rating + Major Match"
    elif rating >= 4.0:
        tier = "Tier 2: High Rating + Major Mismatch"
    else:
        tier = "Tier 3: Lower Rating (Penalized)"

    return score, tier

# Match all students in match_requests
def match_all_requests(cursor, conn, progress_callback=None):
    all_users = fetch_users_from_db(cursor)
    cursor.execute("SELECT student_id FROM match_requests;")
    requests = cursor.fetchall()

    for i, (student_id,) in enumerate(requests, start=1):
        current_user = next((u for u in all_users if u.user_id == student_id), None)
        if not current_user:
            continue

        match_scores = []
        for other_user in all_users:
            if other_user.user_id == current_user.user_id:
                continue
            if not (set(other_user.classes_can_tutor) & set(current_user.classes_needed)):
                continue
            if not (set(current_user.classes_can_tutor) & set(other_user.classes_needed)) and not(other_user.show_as_backup):
                continue

            score, _ = get_match_score_and_tier(other_user, current_user)
            match_scores.append((other_user.user_id, score))

        top_10 = sorted(match_scores, key=lambda x: -x[1])[:10]

        match_pairs = []
        seen_pairs = set()

        for matched_user_id, score in top_10:
            pair1 = (student_id, matched_user_id)
            pair2 = (matched_user_id, student_id)

            if pair1 not in seen_pairs:
                match_pairs.append((student_id, matched_user_id, score))
                seen_pairs.add(pair1)

            if pair2 not in seen_pairs:
                match_pairs.append((matched_user_id, student_id, score))
                seen_pairs.add(pair2)

        execute_values(
            cursor,
            """
            INSERT INTO matches (requester_id, matched_user_id, match_score)
            VALUES %s
            ON CONFLICT DO NOTHING
            """,
            match_pairs
        )

        if progress_callback:
            progress_callback(i)

    conn.commit()
