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
    for _ in range(n):
        display_name = fake.name()
        email = fake.email()
        major = random.choice(uiuc_majors)
        rating = round(random.uniform(0, 5), 2)
        total_ratings = random.randint(0, 100) if rating > 0 else 0
        rating_history = (
            [random.randint(1, 5) for _ in range(min(50, total_ratings))]
            if total_ratings > 0
            else []
        )
        show_as_backup = random.choice([True, False])
        classes_can_tutor = random.sample(uiuc_classes, random.randint(0, 4))
        classes_needed = random.sample(uiuc_classes, random.randint(0, 4))
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


def insert_users(users):
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

    users = generate_users(20)
    print(users)
    insert_users(users)

    cursor.close()
    conn.close()
    print("Dummy data inserted into db")
