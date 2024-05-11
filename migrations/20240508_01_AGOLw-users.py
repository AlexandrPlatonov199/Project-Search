"""
users
"""

from yoyo import step

__depends__ = {}

steps = [
    step("""
        CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
        CREATE TABLE users (
            id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
            email VARCHAR(255) UNIQUE,
            password VARCHAR(72),
            first_name VARCHAR(255),
            last_name VARCHAR(255),
            avatar VARCHAR(255) UNIQUE,
            telegram VARCHAR(255) UNIQUE,
            is_activated BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """,
         "DROP TABLE users;"
         ),
]
