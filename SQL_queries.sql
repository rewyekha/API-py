CREATE DATABASE chs;

use chs;

CREATE TABLE User_details (
    User_id INT AUTO_INCREMENT PRIMARY KEY,
    First_Name VARCHAR(255),
    Last_Name VARCHAR(255),
    Age INT,
    Sex VARCHAR(10),
    Contact_Number VARCHAR(20),
    Email_ID VARCHAR(255),
    Password VARCHAR(255)
);

CREATE TABLE Store_user (
    Store_user_id INT AUTO_INCREMENT PRIMARY KEY,
    First_Name VARCHAR(255),
    Last_Name VARCHAR(255),
    Age INT,
    Sex VARCHAR(10),
    Contact_Number VARCHAR(20),
    Email_ID VARCHAR(255),
    Password VARCHAR(255),
    Designation VARCHAR(20)
);

CREATE TABLE Products (
    Product_id INT AUTO_INCREMENT PRIMARY KEY,
    Product_name VARCHAR(255),
    Rate DECIMAL(10, 2),
    Stock INT
);

CREATE TABLE Purchase (
    Purchase_id INT AUTO_INCREMENT PRIMARY KEY,
    User_id INT,
    Item VARCHAR(255),
    Quantity INT,
    Rate DECIMAL(10, 2),
    Date_of_purchase DATE,
    FOREIGN KEY (User_id) REFERENCES User_details(User_id)
);
