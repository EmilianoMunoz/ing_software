CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    surname VARCHAR(255),
    email VARCHAR(255),
    password VARCHAR(255)
);


CREATE TABLE IF NOT EXISTS cabins (
    id SERIAL PRIMARY KEY,
    type VARCHAR(255),
    level VARCHAR(255),
    capacity INTEGER
);