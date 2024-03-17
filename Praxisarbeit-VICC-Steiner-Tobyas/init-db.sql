-- Erstellung der Tabelle User
CREATE TABLE "user"
(
    id               SERIAL PRIMARY KEY,
    username         VARCHAR(64)  NOT NULL,
    email            VARCHAR(128) NOT NULL,
    password_hash    VARCHAR(128) NOT NULL,
    cd
                     token VARCHAR(32),
    token_expiration TIMESTAMP
);

-- Erstellung der Tabelle rentalvehicle
CREATE TABLE rentalvehicle
(
    id    SERIAL PRIMARY KEY,
    price FLOAT NOT NULL,
    info  VARCHAR(256)
);

-- Erstellung der Tabelle Reservation
CREATE TABLE reservation
(
    id              SERIAL PRIMARY KEY,
    date            DATE NOT NULL,
    rental_vehicle_id INT  NOT NULL,
    user_id         INT  NOT NULL,
    FOREIGN KEY (rental_vehicle_id) REFERENCES rentalvehicle (id),
    FOREIGN KEY (user_id) REFERENCES "user" (id)
);
