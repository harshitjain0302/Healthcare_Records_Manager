# HealSync - Healthcare Records Manager

Welcome to **HealSync**, a comprehensive web-based application designed to simplify and streamline the management of healthcare records. Built using **Flask**, **SQLite**, and **Bootstrap**, this app allows users to add, update, delete, and visualize key patient, doctor, hospital, and billing data efficiently.

##  Features

- Add, update, and delete **Patients**, **Doctors**, **Hospitals**, **Admissions**, and **Billing** records
- Real-time **search** and **dropdown filtering** on all management pages
- Interactive **data visualizations** using Chart.js, including:
  - Total Billing per Hospital
  - Gender Distribution
  - Admissions by Type
  - Top 5 Doctors by Admissions
- Clean and intuitive dashboard navigation with sidebar

##  Project Structure

```
healthcare_records_manager/
├── app.py                   # Main Flask application
├── templates/
│   ├── dashboard.html
│   ├── patients.html
│   ├── doctors.html
│   ├── admissions.html
│   ├── billing.html
│   └── visualizations.html
├── static/                  # (Optional) CSS or JS static files
├── healthcare_dataset.csv   # Initial data (if applicable)
├── README.md                # This file
└── requirements.txt         # Dependencies
```

##  Technologies Used
- **Python Flask** - for backend routing and logic
- **SQLite** - lightweight embedded database
- **Jinja2** - for HTML templating
- **Chart.js** - for visual analytics
- **Bootstrap 5** - responsive UI design

##  Setup Instructions

1. **Clone the Repository:**
```bash
git clone https://github.com/your-username/healthcare_records_manager.git
cd healthcare_records_manager
```

2. **Create Virtual Environment & Install Dependencies:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
pip install -r requirements.txt
```

3. **Run the Flask App:**
```bash
python app.py
```

4. **Visit in Browser:**
```
http://localhost:5000/
```

##  Video Demo
A recorded walkthrough of the application is available here: *(Add your video demo URL once ready)*

##  Screenshots
Screenshots of the app’s key pages including dashboard, management tables, update forms, and visualizations are available in the project documentation.

##  License
This project is part of an academic submission for the "Applied Database Technologies" course.

---

Contributors: Harshit Jain, Arnav Srivastava, Aashi Sharma
