CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    passwords TEXT NOT NULL,
    total DECIMAL(10,2) NOT NULL DEFAULT 0.00
);

