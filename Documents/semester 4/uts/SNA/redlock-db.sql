CREATE DATABASE Redlock;

USE Redlock;

CREATE TABLE users (
    ID INT PRIMARY KEY,
    Nama VARCHAR(255),
    Alamat VARCHAR(255),
    Jabatan VARCHAR(255)
);

INSERT INTO users(ID, Nama, Alamat, Jabatan)
values 
(1, 'huda', 'tambun', 'Direktur'),
(2, 'udil', 'cibitung', 'HRD'),
(3, 'gudal', 'cikarang', 'sales'),
(4, 'jenggo', 'cikarang', 'Office Boy');