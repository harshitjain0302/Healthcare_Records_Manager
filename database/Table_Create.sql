-- SQLite-Compatible Schema and Inserts
PRAGMA foreign_keys = ON;

CREATE TABLE Patients (
    patient_id INT PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    age INT,
    gender ENUM('Male', 'Female', 'Other'),
    blood_type TEXT,
    medical_condition TEXT
);

CREATE TABLE Hospitals (
    hospital_id INT PRIMARY KEY AUTOINCREMENT,
    name TEXT
);


CREATE TABLE Doctors (
    doctor_id INT PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    hospital_id INT,
    FOREIGN KEY (hospital_id) REFERENCES Hospitals(hospital_id)
);


CREATE TABLE Admissions (
    admission_id INT PRIMARY KEY AUTOINCREMENT,
    patient_id INT,
    doctor_id INT,
    hospital_id INT,
    admission_date DATE,
    discharge_date DATE,
    room_number TEXT,
    admission_type TEXT,
    FOREIGN KEY (patient_id) REFERENCES Patients(patient_id),
    FOREIGN KEY (doctor_id) REFERENCES Doctors(doctor_id),
    FOREIGN KEY (hospital_id) REFERENCES Hospitals(hospital_id)
);

CREATE TABLE Billing (
    billing_id INT PRIMARY KEY AUTOINCREMENT,
    patient_id INT,
    insurance_provider TEXT,
    billing_amount DECIMAL(10,2),
    FOREIGN KEY (patient_id) REFERENCES Patients(patient_id)
);