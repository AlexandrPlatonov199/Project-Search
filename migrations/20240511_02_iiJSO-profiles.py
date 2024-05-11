"""
profiles
"""

from yoyo import step

__depends__ = {'20240511_01_H0r83-users-skills'}

steps = [
    step("""
        CREATE TABLE profiles (
            user_id UUID PRIMARY KEY,
            about TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        );
        """,
         "DROP TABLE profiles;"
         ),

]
