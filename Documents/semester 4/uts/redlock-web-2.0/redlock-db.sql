CREATE DATABASE Redlock;

USE Redlock

CREATE TABLE users (
    ID INT PRIMARY KEY,
    Nama VARCHAR(255),
    Alamat VARCHAR(255),
    Jabatan VARCHAR(255)
);

INSERT INTO users VALUES
(1, 'Joshua', 'Kemanggisan', 'Manager'),
(2, 'Vinsen', 'Kebayoran', 'Sales Associate'),
(3, 'Namira', 'Kebon Jeruk', 'Customer Service Representative');


