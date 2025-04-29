INSERT INTO Patients (name, age, gender, blood_type, medical_condition)
SELECT DISTINCT Name, Age, Gender, `Blood Type`, `Medical Condition`
FROM healthcare_dataset;

SELECT * FROM Patients LIMIT 5;

INSERT INTO Hospitals (name)
SELECT DISTINCT Hospital FROM healthcare_dataset;

SELECT * FROM Hospitals LIMIT 5;

INSERT INTO Doctors (name, hospital_id)
SELECT DISTINCT r.Doctor, h.hospital_id
FROM healthcare_dataset r
JOIN Hospitals h ON r.Hospital = h.name;

SELECT * FROM Doctors LIMIT 5;

INSERT INTO Admissions (patient_id, doctor_id, hospital_id, admission_date, discharge_date, room_number, admission_type)
SELECT 
    p.patient_id, 
    d.doctor_id, 
    h.hospital_id, 
    STR_TO_DATE(r.`Date of Admission`, '%d-%m-%Y'),  
    STR_TO_DATE(r.`Discharge Date`, '%d-%m-%Y'),  
    r.`Room Number`, 
    r.`Admission Type`
FROM healthcare_dataset r
JOIN Patients p ON r.Name = p.name
JOIN Doctors d ON r.Doctor = d.name
JOIN Hospitals h ON r.Hospital = h.name;

SELECT * FROM Admissions LIMIT 5;

INSERT INTO Billing (patient_id, insurance_provider, billing_amount)
SELECT p.patient_id, r.`Insurance Provider`, r.`Billing Amount`
FROM healthcare_dataset r
JOIN Patients p ON r.Name = p.name;

SELECT * FROM Billing LIMIT 5;
