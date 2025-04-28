from datetime import datetime
from backend.scripts.matchingalgo import (
    User,
    parse_pg_array,
    parse_pg_dict,
    fetch_users_from_db,
    get_match_score_and_tier,
)

from rapidfuzz import fuzz


def search_user_by_name(cursor, name):
    cursor.execute("SELECT * FROM users WHERE display_name ILIKE %s;", ('%' + name + '%',))
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


def search_all_users_by_subject(cursor, conn, current_user_id, subject_query):
    all_users = fetch_users_from_db(cursor)
    user_map = {u.user_id: u for u in all_users}
    current_user = user_map.get(current_user_id)
    if not current_user:
        return []

    subject_query_lower = subject_query.lower()

    cursor.execute("""
        SELECT matched_user_id
        FROM matches
        WHERE requester_id = %s
        ORDER BY match_score DESC
        LIMIT 10;
    """, (current_user_id,))
    top_10_matches = {row[0] for row in cursor.fetchall()}

    matching_users = []

    for other_user in all_users:
        if other_user.user_id == current_user.user_id:
            continue

        matching_subjects = [
            cls for cls in other_user.classes_can_tutor
            if subject_query_lower in cls.lower()  # Only exact substring matching here
        ]
        if not matching_subjects:
            continue

        if not (set(other_user.classes_can_tutor) & set(current_user.classes_needed)):
            continue

        if (
            not (set(current_user.classes_can_tutor) & set(other_user.classes_needed))
            and not other_user.show_as_backup
        ):
            continue

        raw_score, tier = get_match_score_and_tier(other_user, current_user)

        if other_user.user_id in top_10_matches:
            priority = 1
        elif other_user.major == current_user.major:
            priority = 2
        else:
            priority = 3

        matching_users.append((priority, raw_score, other_user, tier, matching_subjects))

    matching_users.sort(key=lambda x: (x[0], -x[1]))

    result = []
    for priority, score, user_obj, tier, matched_classes in matching_users:
        result.append((user_obj, score, tier, matched_classes, priority))

    return result


def search_top_5_users_by_subject(cursor, conn, current_user_id, subject_query):
    all_users = fetch_users_from_db(cursor)
    user_map = {u.user_id: u for u in all_users}
    current_user = user_map.get(current_user_id)
    if not current_user:
        return []

    subject_query_lower = subject_query.lower()

    cursor.execute("""
        SELECT matched_user_id
        FROM matches
        WHERE requester_id = %s
        ORDER BY match_score DESC
        LIMIT 10;
    """, (current_user_id,))
    top_10_matches = {row[0] for row in cursor.fetchall()}

    matching_users = []

    for other_user in all_users:
        if other_user.user_id == current_user.user_id:
            continue

        matching_subjects = []
        for cls in other_user.classes_can_tutor:
            #Hybrid fuzzy match: max(partial, token sort)
            similarity = max(
                fuzz.partial_ratio(subject_query_lower, cls.lower()),
                fuzz.token_sort_ratio(subject_query_lower, cls.lower())
            )
            if similarity >= 70:  # higher is stricter, lower is more matches
                matching_subjects.append(cls)

        if not matching_subjects:
            continue

        if not (set(other_user.classes_can_tutor) & set(current_user.classes_needed)):
            continue

        if (
            not (set(current_user.classes_can_tutor) & set(other_user.classes_needed))
            and not other_user.show_as_backup
        ):
            continue

        raw_score, tier = get_match_score_and_tier(other_user, current_user)

        if other_user.user_id in top_10_matches:
            priority = 1
        elif other_user.major == current_user.major:
            priority = 2
        else:
            priority = 3

        matching_users.append((priority, raw_score, other_user, tier, matching_subjects))

    matching_users.sort(key=lambda x: (x[0], -x[1]))

    matching_users = matching_users[:5]  # Limit to top 5

    result = []
    for priority, score, user_obj, tier, matched_classes in matching_users:
        result.append((user_obj, score, tier, matched_classes, priority))

    return result
