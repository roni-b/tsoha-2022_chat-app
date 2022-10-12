CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    password TEXT,
    username TEXT UNIQUE,
    admin BOOLEAN
);

CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    content TEXT,
    sent_at TIMESTAMP,
    user_id INTEGER REFERENCES users,
    groups_id INTEGER REFERENCES groups
);

CREATE TABLE groups (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE
);

CREATE TABLE groupMembers (
    group_id INTEGER REFERENCES groups,
    member_id INTEGER REFERENCES users
);

CREATE TABLE messageRatings (
    id SERIAL PRIMARY KEY,
    message_id INTEGER REFERENCES messages,
    likes INTEGER DEFAULT 0,
    dislikes INTEGER DEFAULT 0
);

CREATE TABLE publicMessages (
    id SERIAL PRIMARY KEY,
    content TEXT,
    sent_at TIMESTAMP
);

CREATE TABLE reports (
    id SERIAL PRIMARY KEY,
    message_id INTEGER REFERENCES messages,
    report_count INTEGER DEFAULT 0
);

