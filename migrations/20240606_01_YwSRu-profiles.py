"""
profiles
"""

from yoyo import step

__depends__ = {'20240508_01_AGOLw-users'}

steps = [
    step("""
    CREATE TABLE profiles(
        id SERIAL PRIMARY KEY,
        user_id UUID,
        first_name VARCHAR(256),
        last_name VARCHAR(256),
        telegram VARCHAR(255) UNIQUE,
        bio TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES Users(id)
        );
    """)
]
