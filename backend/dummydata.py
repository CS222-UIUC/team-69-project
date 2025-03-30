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
    shared_classes = random.sample(uiuc_classes, k=6)  # Add overlap between users
    for _ in range(n):
        display_name = fake.name()
        email = fake.email()
        major = random.choice(uiuc_majors)
        rating = round(random.uniform(0, 5), 2)
        total_ratings = random.randint(0, 100) if rating > 0 else 0
        rating_history = (
            [
                random.choices([4, 5, 3], weights=[0.4, 0.5, 0.1])[0]
                for _ in range(min(50, total_ratings))
            ]
            if total_ratings > 0
            else []
        )

        show_as_backup = random.choice([True, False])
        max_classes = 4

        # Ensure total does not exceed 4 and uses shared pool for overlap
        num_shared_tutor = random.randint(1, min(len(shared_classes), max_classes))
        num_personal_tutor = random.randint(0, max_classes - num_shared_tutor)
        classes_can_tutor = random.sample(shared_classes, num_shared_tutor) + random.sample(
            list(set(uiuc_classes) - set(shared_classes)), num_personal_tutor
        )

        num_shared_needed = random.randint(1, min(len(shared_classes), max_classes))
        num_personal_needed = random.randint(0, max_classes - num_shared_needed)
        classes_needed = random.sample(shared_classes, num_shared_needed) + random.sample(
            list(set(uiuc_classes) - set(shared_classes)), num_personal_needed
        )

        recent_interactions = random_timestamps(min(10, total_ratings))

        users.append(
            (
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
            )
        )
    return users


def insert_users(users, cursor, conn):
    for user in users:
        cursor.execute(
            """
            INSERT INTO users (display_name, email, major, rating, total_ratings, rating_history, show_as_backup, classes_can_tutor, classes_needed, recent_interactions)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
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
