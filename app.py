from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)

def get_db_connection():
    base_dir = os.path.abspath(os.path.dirname(__file__))
    db_path = os.path.join(base_dir, "healthcare.db")
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/', methods=['GET', 'POST'])
def index():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM Hospitals')
    hospitals = cursor.fetchall()
    cursor.execute('SELECT * FROM Patients')
    patients = cursor.fetchall()
    cursor.execute('SELECT * FROM Doctors')
    doctors = cursor.fetchall()

    cursor.execute('''
        SELECT Hospitals.name AS hospital, SUM(Billing.billing_amount) AS total_billing
        FROM Billing
        JOIN Patients ON Billing.patient_id = Patients.patient_id
        JOIN Admissions ON Patients.patient_id = Admissions.patient_id
        JOIN Hospitals ON Admissions.hospital_id = Hospitals.hospital_id
        GROUP BY Hospitals.name
    ''')
    billing_data = cursor.fetchall()

    cursor.execute('SELECT gender, COUNT(*) FROM Patients GROUP BY gender')
    gender_data = cursor.fetchall()

    if request.method == 'POST':
        form_type = request.form.get('form_type')

        if form_type == 'add_patient':
            cursor.execute('''
                INSERT INTO Patients (name, age, gender, blood_type, medical_condition)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                request.form['name'], request.form['age'], request.form['gender'],
                request.form['blood_type'], request.form['medical_condition']
            ))

        elif form_type == 'add_doctor':
            cursor.execute('''
                INSERT INTO Doctors (name, hospital_id)
                VALUES (?, ?)
            ''', (request.form['name'], request.form['hospital_id']))

        elif form_type == 'add_admission':
            cursor.execute('''
                INSERT INTO Admissions (patient_id, doctor_id, hospital_id, admission_date, discharge_date, room_number, admission_type)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                request.form['patient_id'], request.form['doctor_id'], request.form['hospital_id'],
                request.form['admission_date'], request.form['discharge_date'],
                request.form['room_number'], request.form['admission_type']
            ))

        elif form_type == 'add_billing':
            cursor.execute('''
                INSERT INTO Billing (patient_id, insurance_provider, billing_amount)
                VALUES (?, ?, ?)
            ''', (
                request.form['patient_id'], request.form['insurance_provider'], request.form['billing_amount']
            ))

        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    conn.close()
    return render_template(
        'dashboard.html',
        billing_data=billing_data,
        gender_data=gender_data,
        hospitals=hospitals,
        patients=patients,
        doctors=doctors
    )

@app.route('/patients')
def patients():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Patients')
    data = cursor.fetchall()
    conn.close()
    return render_template('patients.html', patients=data)

@app.route('/update_patient/<int:id>', methods=['GET', 'POST'])
def update_patient(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    if request.method == 'POST':
        cursor.execute('''
            UPDATE Patients SET name=?, age=?, gender=?, blood_type=?, medical_condition=?
            WHERE patient_id=?
        ''', (
            request.form['name'], request.form['age'], request.form['gender'],
            request.form['blood_type'], request.form['medical_condition'], id
        ))
        conn.commit()
        conn.close()
        return redirect(url_for('patients'))
    else:
        cursor.execute('SELECT * FROM Patients WHERE patient_id = ?', (id,))
        patient = cursor.fetchone()
        conn.close()
        return render_template('update_patient.html', patient=patient)

@app.route('/delete_patient/<int:id>')
def delete_patient(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM Patients WHERE patient_id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('patients'))

@app.route("/doctors")
def doctors():
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Fetch doctor records
    cur.execute("""
        SELECT Doctors.doctor_id, Doctors.name, Hospitals.name 
        FROM Doctors 
        JOIN Hospitals ON Doctors.hospital_id = Hospitals.hospital_id
    """)
    doctors = cur.fetchall()

    # Fetch unique hospital names
    cur.execute("SELECT DISTINCT name FROM Hospitals")
    hospitals = [row[0] for row in cur.fetchall()]

    conn.close()
    return render_template("doctors.html", doctors=doctors, hospitals=hospitals)

@app.route('/update_doctor/<int:id>', methods=['GET', 'POST'])
def update_doctor(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Hospitals')
    hospitals = cursor.fetchall()
    if request.method == 'POST':
        cursor.execute('''
            UPDATE Doctors SET name=?, hospital_id=? WHERE doctor_id=?
        ''', (request.form['name'], request.form['hospital_id'], id))
        conn.commit()
        conn.close()
        return redirect(url_for('doctors'))
    else:
        cursor.execute('SELECT doctor_id, name, hospital_id FROM Doctors WHERE doctor_id = ?', (id,))
        doctor = cursor.fetchone()
        conn.close()
        return render_template('update_doctor.html', doctor=doctor, hospitals=hospitals)

@app.route('/delete_doctor/<int:id>')
def delete_doctor(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM Doctors WHERE doctor_id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('doctors'))

@app.route('/hospitals')
def hospitals():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Hospitals')
    hospitals = cursor.fetchall()
    conn.close()
    return render_template('hospitals.html', hospitals=hospitals)

@app.route('/add_hospital', methods=['GET', 'POST'])
def add_hospital():
    if request.method == 'POST':
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO Hospitals (name) VALUES (?)', (request.form['name'],))
        conn.commit()
        conn.close()
        return redirect(url_for('hospitals'))
    return render_template('add_hospital.html')

@app.route('/delete_hospital/<int:id>')
def delete_hospital(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM Hospitals WHERE hospital_id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('hospitals'))

@app.route("/admissions")
def admissions():
    conn = get_db_connection()
    cur = conn.cursor()

    # Fetch admissions
    cur.execute("""
        SELECT Admissions.admission_id, Patients.name, Doctors.name, Hospitals.name, 
               admission_date, discharge_date, room_number, admission_type
        FROM Admissions
        JOIN Patients ON Admissions.patient_id = Patients.patient_id
        JOIN Doctors ON Admissions.doctor_id = Doctors.doctor_id
        JOIN Hospitals ON Admissions.hospital_id = Hospitals.hospital_id
    """)
    admissions = cur.fetchall()

    # Fetch unique admission types
    cur.execute("SELECT DISTINCT admission_type FROM Admissions")
    admission_types = [row[0] for row in cur.fetchall()]

    conn.close()
    return render_template("admissions.html", admissions=admissions, admission_types=admission_types)

@app.route('/update_admission/<int:id>', methods=['GET', 'POST'])
def update_admission(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Patients')
    patients = cursor.fetchall()
    cursor.execute('SELECT * FROM Doctors')
    doctors = cursor.fetchall()
    cursor.execute('SELECT * FROM Hospitals')
    hospitals = cursor.fetchall()

    if request.method == 'POST':
        cursor.execute('''
            UPDATE Admissions
            SET patient_id=?, doctor_id=?, hospital_id=?, admission_date=?, discharge_date=?, room_number=?, admission_type=?
            WHERE admission_id=?
        ''', (
            request.form['patient_id'],
            request.form['doctor_id'],
            request.form['hospital_id'],
            request.form['admission_date'],
            request.form['discharge_date'],
            request.form['room_number'],
            request.form['admission_type'],
            id
        ))
        conn.commit()
        conn.close()
        return redirect(url_for('admissions'))
    
    cursor.execute('SELECT * FROM Admissions WHERE admission_id = ?', (id,))
    admission = cursor.fetchone()
    conn.close()
    return render_template('update_admission.html', admission=admission, patients=patients, doctors=doctors, hospitals=hospitals)

@app.route('/delete_admission/<int:id>')
def delete_admission(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM Admissions WHERE admission_id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('admissions'))

@app.route("/billing")
def billing():
    conn = get_db_connection()
    cur = conn.cursor()

    # Fetch billing records
    cur.execute("""
        SELECT Billing.billing_id, Patients.name, Billing.insurance_provider, Billing.billing_amount
        FROM Billing
        JOIN Patients ON Billing.patient_id = Patients.patient_id
    """)
    billing = cur.fetchall()

    # Fetch unique insurance providers
    cur.execute("SELECT DISTINCT insurance_provider FROM Billing")
    providers = [row[0] for row in cur.fetchall()]

    conn.close()
    return render_template("billing.html", billing=billing, providers=providers)

@app.route('/update_billing/<int:id>', methods=['GET', 'POST'])
def update_billing(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Patients')
    patients = cursor.fetchall()

    if request.method == 'POST':
        cursor.execute('''
            UPDATE Billing
            SET patient_id=?, insurance_provider=?, billing_amount=?
            WHERE billing_id=?
        ''', (
            request.form['patient_id'],
            request.form['insurance_provider'],
            request.form['billing_amount'],
            id
        ))
        conn.commit()
        conn.close()
        return redirect(url_for('billing'))
    
    cursor.execute('SELECT * FROM Billing WHERE billing_id = ?', (id,))
    bill = cursor.fetchone()
    conn.close()
    return render_template('update_billing.html', bill=bill, patients=patients)

@app.route('/delete_billing/<int:id>')
def delete_billing(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM Billing WHERE billing_id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('billing'))

@app.route("/visualizations")
def visualizations():
    conn = get_db_connection()
    conn.row_factory = None  # Return regular tuples instead of sqlite3.Row
    cur = conn.cursor()

    # Billing totals by hospital
    cur.execute("""
        SELECT Hospitals.name, SUM(Billing.billing_amount)
        FROM Billing
        JOIN Admissions ON Billing.patient_id = Admissions.patient_id
        JOIN Hospitals ON Admissions.hospital_id = Hospitals.hospital_id
        GROUP BY Hospitals.name
    """)
    billing_data = cur.fetchall()

    # Gender distribution
    cur.execute("SELECT gender, COUNT(*) FROM Patients GROUP BY gender")
    gender_data = cur.fetchall()

    # Admission types
    cur.execute("SELECT admission_type, COUNT(*) FROM Admissions GROUP BY admission_type")
    type_data = cur.fetchall()

    # Top 5 doctors by admission count
    cur.execute("""
        SELECT Doctors.name, COUNT(*)
        FROM Admissions
        JOIN Doctors ON Admissions.doctor_id = Doctors.doctor_id
        GROUP BY Doctors.name
        ORDER BY COUNT(*) DESC
        LIMIT 5
    """)
    top_doctors = cur.fetchall()

    conn.close()

    return render_template("visualizations.html",
                           billing_data=billing_data,
                           gender_data=gender_data,
                           type_data=type_data,
                           top_doctors=top_doctors)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    app.run(debug=True, port=port)
   
