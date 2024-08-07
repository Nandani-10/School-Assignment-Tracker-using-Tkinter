CREATE DATABASE assignment_tracker;
USE assignment_tracker;

CREATE TABLE assignments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    due_date DATE,
    status VARCHAR(50),
    file_path VARCHAR(255)
);
