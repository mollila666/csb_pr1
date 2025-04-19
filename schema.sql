CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name TEXT,
    password TEXT,
    logs INTEGER
);

CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    message TEXT,
    name TEXT
);
