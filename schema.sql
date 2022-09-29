CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    password TEXT,
    username TEXT UNIQUE,
    admin TEXT
);

CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    content TEXT,
    sent_at TIMESTAMP,
    user_id INTEGER REFERENCES users
);

CREATE TABLE groups (
    id SERIAL PRIMARY KEY,
    name TEXT,
    user_id INTEGER REFERENCES users
);

CREATE TABLE members (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users
);

CREATE TABLE groupMembers (
    group_id INTEGER REFERENCES groups,
    member_id INTEGER REFERENCES members
);
