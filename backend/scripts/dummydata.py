import random
import psycopg2
from faker import Faker
from datetime import datetime, timedelta
from dotenv import dotenv_values
import os

fake = Faker()

uiuc_classes = [
    "MATH 241",
    "MATH 285",
    "MATH 415",
    "MATH 444",
    "MATH 461",
    "PHYS 211",
    "PHYS 212",
    "PHYS 213",
    "PHYS 214",
    "CHEM 102",
    "CHEM 332",
    "CHEM 440",
    "MCB 150",
    "IB 150",
    "IB 302",
    "PHIL 101",
    "PHIL 103",
    "CS 124",
    "CS 225",
    "CS 233",
    "CS 374",
    "ECE 110",
    "ECE 120",
]
uiuc_majors = [
    "Computer Science",
    "Mathematics",
    "Physics",
    "Integrative Biology",
    "Chemistry",
]

def random_timestamps(n):
    return [
        datetime.now()
        - timedelta(days=random.randint(0, 365), hours=random.randint(0, 24))
        for _ in range(n)
    ]

def generate_users(n):
    users = []
    shared_classes = random.sample(uiuc_classes, k=6)  # Shared overlap across users
    used_emails = set()

    while len(users) < n:
        display_name = fake.name()
        email = fake.email()
        if email in used_emails:
            continue
        used_emails.add(email)

        major = random.choice(uiuc_majors)
        total_ratings = random.randint(0, 100)
        rating_history = [
            random.choices([4, 5, 3], weights=[0.4, 0.5, 0.1])[0]
            for _ in range(min(50, total_ratings))
        ] if total_ratings > 0 else []
        rating = round(sum(rating_history) / len(rating_history), 2) if rating_history else 0.0

        show_as_backup = random.choice([True, False])
        max_classes = 4

        # Generate disjoint class lists to generate classes_can_tutor
        num_shared_tutor = random.randint(1, min(len(shared_classes), max_classes)) #num of shared classes the user can tutor
        num_personal_tutor = random.randint(0, max_classes - num_shared_tutor) #num of personal classes the user can tutor
        classes_can_tutor = random.sample(shared_classes, num_shared_tutor) + random.sample(
            list(set(uiuc_classes) - set(shared_classes)), num_personal_tutor
        )

        # Remove tutor classes to enforce disjoint and generate classes_needed
        excluded = set(classes_can_tutor)
        remaining_shared = list(set(shared_classes) - excluded)
        remaining_personal = list(set(uiuc_classes) - excluded)

        # Skip this user if no options left
        if not remaining_shared and not remaining_personal:
            continue

        num_shared_needed = min(len(remaining_shared), random.randint(1, max_classes))
        num_personal_needed = max_classes - num_shared_needed

        if num_shared_needed == 0 and len(remaining_personal) > 0:
            num_personal_needed = 1
        elif num_personal_needed == 0 and len(remaining_shared) > 0:
            num_shared_needed = 1

        needed_shared = random.sample(remaining_shared, num_shared_needed) if remaining_shared else []
        needed_personal = random.sample(remaining_personal, num_personal_needed) if remaining_personal else []
        classes_needed = needed_shared + needed_personal

        # Final safety check
        if not classes_can_tutor or not classes_needed:
            continue

        recent_interactions = random_timestamps(min(10, total_ratings))

        class_ratings = {
            class_name: round(random.uniform(2.5, 5.0), 2) for class_name in classes_can_tutor
        }

        users.append((
            display_name,
            email,
            major,
            rating,
            total_ratings,
            rating_history,
            show_as_backup,
            classes_can_tutor,
            classes_needed,
            recent_interactions,
            class_ratings
        ))

        print(f"\rGenerating users... ({len(users)}/{n})", end="")

    print()
    return users

    print(f"\rGenerating users... ({len(users)}/{n})", end="")
    print()
    return users

def insert_users(users, cursor, conn):
    for user in users:
        cursor.execute(
            """
            INSERT INTO users (display_name, email, major, rating, total_ratings, rating_history, show_as_backup, classes_can_tutor, classes_needed, recent_interactions, class_ratings)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
            """,
            user,
        )
    conn.commit()

if __name__ == "__main__":  # this file can be ran or used as a library
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
    cursor = conn.cursor()

    users = generate_users(200)
    print(users)
    insert_users(users)

    cursor.close()
    conn.close()
    print("Dummy data inserted into db")
