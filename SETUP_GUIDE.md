# Hospital Information System (HIS) - Complete Setup Guide

## Project Overview
This is a full-featured Hospital Information System built with Django and Bootstrap 5. It supports:
- Patient registration and management
- Doctor profiles and scheduling
- Appointment booking and cancellation
- Medical records management
- Prescription tracking
- Patient scans/documents
- Payment tracking
- Admin dashboard

---

## Prerequisites

Make sure you have:
- Python 3.8+ installed
- MySQL Server 5.7+ installed
- pip package manager

---

## Installation Steps

### Step 1: Activate Virtual Environment

In VS Code terminal, navigate to the project root and activate the virtual environment:

```powershell
cd "d:\UNI\Database Systems\DB_Project"
.\venv\Scripts\Activate.ps1
```

### Step 2: Install Dependencies

```powershell
pip install --upgrade pip
pip install django==5.2.14
pip install django-crispy-forms==2.1
pip install crispy-bootstrap5==2.0.2
pip install mysqlclient==2.2.6
pip install pillow==10.0.0
```

### Step 3: Create MySQL Database

Open MySQL Workbench or Command Line:

```sql
CREATE DATABASE hospital_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### Step 4: Update Database Configuration

Open `his_config/settings.py` and update the DATABASES section with your MySQL credentials:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'hospital_db',
        'USER': 'root',  # Your MySQL username
        'PASSWORD': 'your_password',  # Your MySQL password
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

### Step 5: Run Migrations

```powershell
cd "d:\UNI\Database Systems\DB_Project\DB-Project"
python manage.py makemigrations
python manage.py migrate
```

If you get any errors, run:
```powershell
python manage.py migrate --run-syncdb
```

### Step 6: Create Superuser (Admin)

```powershell
python manage.py createsuperuser
```

Follow the prompts to create an admin account:
- Username: admin
- Email: admin@hospital.com
- Password: (choose a secure password)

### Step 7: Create Department

```powershell
python manage.py shell
```

Then in the Python shell:

```python
from hospital.models import Department
Department.objects.create(
    department_code='SURG001',
    name='Surgery Department',
    location='Building A, Floor 3',
    contact_number='+1-800-123-4567'
)
exit()
```

### Step 8: Run the Development Server

```powershell
python manage.py runserver
```

The application will be available at: `http://localhost:8000/`

---

## Initial Access

1. **Home Page**: http://localhost:8000/
2. **Admin Panel**: http://localhost:8000/admin/
   - Use superuser credentials you created
3. **Patient Registration**: http://localhost:8000/patient/register/
4. **Doctor Registration**: http://localhost:8000/doctor/register/

---

## Project Structure

```
DB-Project/
├── hospital/                 # Main Django app
│   ├── models.py            # Database models
│   ├── views.py             # View functions
│   ├── urls.py              # URL routing
│   ├── forms.py             # Django forms
│   ├── admin.py             # Admin configuration
│   └── migrations/          # Database migrations
│
├── his_config/              # Project configuration
│   ├── settings.py          # Settings (update DB here)
│   ├── urls.py              # Main URL routing
│   └── wsgi.py              # WSGI application
│
├── templates/               # HTML templates
│   └── hospital/            # App templates
│       ├── base.html        # Base template
│       ├── home.html        # Home page
│       ├── login.html       # Login page
│       └── ...
│
├── static/                  # Static files (CSS, JS, images)
│   ├── css/
│   └── js/
│
├── media/                   # User uploads (photos, documents)
│   ├── patient_photos/
│   ├── doctor_photos/
│   ├── patient_scans/
│   └── ...
│
└── manage.py               # Django management script
```

---

## Creating Sample Data

### Add a Sample Doctor

Via Admin Panel:
1. Go to http://localhost:8000/admin/
2. Click on "Doctors" 
3. Add a new doctor with:
   - User: Create new user first
   - License Number: LIC123456
   - Specialty: General Surgery
   - Department: Surgery Department

### Add Sample Rooms

1. Go to Admin Panel
2. Click on "Rooms"
3. Add rooms with various types (General Ward, ICU, Operation Theatre, etc.)

---

## Key Features Usage

### For Patients

1. **Register**: Visit `/patient/register/` and fill the form
2. **Complete Profile**: Enter medical information
3. **Book Appointment**: Go to dashboard and click "Book Appointment"
4. **View Medical Records**: Access previous medical records and vitals
5. **View Prescriptions**: See all prescriptions from doctors
6. **View Scans**: Access uploaded medical scans

### For Doctors

1. **Register**: Visit `/doctor/register/`
2. **Complete Profile**: Enter medical credentials
3. **View Appointments**: See scheduled appointments
4. **Manage Patients**: View all your patients
5. **Add Medical Records**: Record patient vitals
6. **Write Prescriptions**: Create prescriptions for patients
7. **Upload Scans**: Upload patient medical scans

### For Admins

1. Access Admin Panel: `/admin/`
2. Manage all data: Users, Patients, Doctors, Appointments, etc.
3. View Dashboard: `/admin/dashboard/`

---

## Common Issues & Solutions

### Issue 1: ModuleNotFoundError: mysqlclient

**Solution**: Ensure mysqlclient is installed:
```powershell
pip install mysqlclient==2.2.6
```

If it fails on Windows, try:
```powershell
pip install mysqlclient==2.1.1
```

### Issue 2: "Can't connect to MySQL server"

**Solution**:
1. Check MySQL is running
2. Verify database name, username, and password in settings.py
3. Make sure MySQL port 3306 is accessible

### Issue 3: "No tables exist"

**Solution**: Run migrations again:
```powershell
python manage.py migrate
```

### Issue 4: Static files not loading

**Solution**: Collect static files:
```powershell
python manage.py collectstatic --noinput
```

---

## Additional Setup

### To Stop the Server

Press `Ctrl + C` in the terminal

### To Deactivate Virtual Environment

```powershell
deactivate
```

### To View Database Records

Use MySQL Workbench or command line:
```sql
USE hospital_db;
SELECT * FROM patients;
SELECT * FROM doctors;
SELECT * FROM appointments;
```

---

## Frontend Customization

The UI uses Bootstrap 5 and is fully responsive. Modify styling in:
- `templates/hospital/base.html` - Main CSS (in `<style>` tag)
- `static/css/` - For custom CSS files

---

## Database Models Overview

1. **Patient** - Stores patient information
2. **Doctor** - Stores doctor information and credentials
3. **Department** - Hospital departments
4. **Appointment** - Appointment bookings
5. **Prescription** - Medication prescriptions
6. **MedicalRecord** - Patient vital signs and health data
7. **Room** - Hospital rooms and beds
8. **RoomReservation** - Room booking management
9. **ScanDocument** - Patient scans (X-Ray, MRI, etc.)
10. **PaymentRecord** - Payment tracking
11. **ContactInquiry** - Contact form submissions

---

## Next Steps

1. Create additional templates for all views (see templates/hospital/ folder)
2. Add more doctors and departments via admin
3. Customize styling to match your hospital branding
4. Add payment gateway integration
5. Implement email notifications
6. Deploy to production server

---

## Support

For issues or questions, check Django documentation at https://docs.djangoproject.com/
