CREATE DATABASE adt_final_project;
USE adt_final_project;

CREATE TABLE Patients (
    patient_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100),
    age INT,
    gender ENUM('Male', 'Female', 'Other'),
    blood_type VARCHAR(5),
    medical_condition TEXT
);

CREATE TABLE Hospitals (
    hospital_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255)
);


CREATE TABLE Doctors (
    doctor_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100),
    hospital_id INT,
    FOREIGN KEY (hospital_id) REFERENCES Hospitals(hospital_id)
);


CREATE TABLE Admissions (
    admission_id INT PRIMARY KEY AUTO_INCREMENT,
    patient_id INT,
    doctor_id INT,
    hospital_id INT,
    admission_date DATE,
    discharge_date DATE,
    room_number VARCHAR(20),
    admission_type VARCHAR(50),
    FOREIGN KEY (patient_id) REFERENCES Patients(patient_id),
    FOREIGN KEY (doctor_id) REFERENCES Doctors(doctor_id),
    FOREIGN KEY (hospital_id) REFERENCES Hospitals(hospital_id)
);

CREATE TABLE Billing (
    billing_id INT PRIMARY KEY AUTO_INCREMENT,
    patient_id INT,
    insurance_provider VARCHAR(100),
    billing_amount DECIMAL(10,2),
    FOREIGN KEY (patient_id) REFERENCES Patients(patient_id)
);