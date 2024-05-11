"""
users_skills
"""

from yoyo import step

__depends__ = {'20240508_01_AGOLw-users'}

steps = [
    step("""
        CREATE TABLE user_skills (
            user_id UUID PRIMARY KEY,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        );
        """,
         "DROP TABLE user_skills;"
         )
]
