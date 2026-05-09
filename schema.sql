CREATE TABLE "user" (

    id SERIAL PRIMARY KEY,

    username VARCHAR(100) UNIQUE NOT NULL,

    password VARCHAR(200) NOT NULL

);

CREATE TABLE task (

    id SERIAL PRIMARY KEY,

    title VARCHAR(200),

    description VARCHAR(500),

    priority VARCHAR(50),

    status VARCHAR(50),

    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    user_id INTEGER NOT NULL,

    FOREIGN KEY (user_id)
    REFERENCES "user"(id)

);