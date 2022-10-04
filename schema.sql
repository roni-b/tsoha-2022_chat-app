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
    user_id INTEGER REFERENCES users,
    groups_id INTEGER REFERENCES groups 
);

CREATE TABLE groups (
    id SERIAL PRIMARY KEY,
    name TEXT[] UNIQUE
);

CREATE TABLE groupMembers (
    groups_id INTEGER REFERENCES groups,
    member_id INTEGER REFERENCES users
);



