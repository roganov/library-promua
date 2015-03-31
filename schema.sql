CREATE TABLE book (
        id INTEGER NOT NULL,
        title VARCHAR,
        PRIMARY KEY (id)
)



CREATE TABLE user (
        id INTEGER NOT NULL,
        email VARCHAR NOT NULL,
        password VARCHAR NOT NULL,
        can_edit BOOLEAN,
        PRIMARY KEY (id),
        UNIQUE (email),
        CHECK (can_edit IN (0, 1))
)



CREATE TABLE author (
        id INTEGER NOT NULL,
        name VARCHAR NOT NULL,
        PRIMARY KEY (id)
)



CREATE TABLE book_author (
        book_id INTEGER,
        page_id INTEGER,
        FOREIGN KEY(book_id) REFERENCES book (id),
        FOREIGN KEY(page_id) REFERENCES author (id)
)
