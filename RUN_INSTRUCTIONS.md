# Hospital Information System - Complete Run Instructions

## Quick Start (5 Minutes)

### 1. Install Dependencies

Open PowerShell in VS Code and run:

```powershell
# Make sure you're in the project directory
cd "d:\UNI\Database Systems\DB_Project\DB-Project"

# Activate virtual environment
..\venv\Scripts\Activate.ps1

# Install all packages
pip install -r requirements.txt
```

### 2. Configure Database

Open `his_config/settings.py` (line ~80) and update:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'hospital_db',
        'USER': 'root',  # ← Your MySQL username
        'PASSWORD': '',  # ← Your MySQL password (empty if no password)
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

### 3. Create Database in MySQL

Open MySQL Command Line or MySQL Workbench and run:

```sql
CREATE DATABASE hospital_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 4. Run Migrations

```powershell
python manage.py makemigrations
python manage.py migrate
```

### 5. Create Admin Account

```powershell
python manage.py createsuperuser
```

When prompted:
- Username: `admin`
- Email: `admin@hospital.com`
- Password: Choose your password and confirm

### 6. Create Initial Department

```powershell
python manage.py shell
```

Then paste this:

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

### 7. Run Server

```powershell
python manage.py runserver
```

You should see:
```
Starting development server at http://127.0.0.1:8000/
```

---

## Access the Application

Open your browser and go to:

### Main Pages
- **Home**: http://localhost:8000/
- **Doctors List**: http://localhost:8000/doctors/
- **Admin Panel**: http://localhost:8000/admin/
- **Contact**: http://localhost:8000/contact/

### User Registration
- **Patient Register**: http://localhost:8000/patient/register/
- **Doctor Register**: http://localhost:8000/doctor/register/
- **Login**: http://localhost:8000/login/

---

## Test the System

### Create a Patient Account

1. Go to http://localhost:8000/patient/register/
2. Fill the form:
   - First Name: John
   - Last Name: Doe
   - Email: john@example.com
   - Password: testpass123

3. Complete profile with:
   - Patient Number: PAT001
   - SSN: 123-45-6789
   - Blood Type: O+
   - Gender: Male

4. Go to Dashboard: http://localhost:8000/patient/dashboard/

### Create a Doctor Account

1. Go to http://localhost:8000/doctor/register/
2. Fill the form with doctor details
3. Complete profile with:
   - License Number: LIC123456
   - Specialty: General Surgery
   - Department: Surgery Department

### Create Sample Data via Admin

1. Go to http://localhost:8000/admin/
2. Login with credentials you created
3. Add:
   - **Rooms**: Click "Rooms" → Add Room
   - **Doctors**: Already created (via registration)
   - **Patients**: Already created (via registration)

### Book an Appointment

1. Login as Patient
2. Click "Book New Appointment"
3. Select doctor and date
4. Confirm booking

---

## Project Structure Overview

```
hospital/
├── models.py              # Database models
├── views.py              # All view logic
├── urls.py               # URL routing
├── forms.py              # Django forms
├── admin.py              # Admin interface setup
└── migrations/           # Database migrations

his_config/
├── settings.py           # Django settings (EDIT DATABASE HERE)
├── urls.py               # Main URL config
└── wsgi.py              # WSGI config

templates/
└── hospital/
    ├── base.html         # Base template (navigation, footer)
    ├── home.html         # Home page
    ├── login.html        # Login page
    ├── patient_register.html
    ├── doctor_register.html
    ├── patient_dashboard.html
    ├── doctor_dashboard.html
    ├── doctors_list.html
    └── ... (other templates)

static/                   # CSS, JS, images
media/                    # User uploads
```

---

## Database Schema

### Main Models

1. **Department**
   - department_code (unique)
   - name (unique)
   - chairman (link to Doctor)
   - location
   - contact_number

2. **Patient**
   - Links to User
   - patient_number (unique)
   - social_security_number (unique)
   - phone, address
   - birthdate, gender, blood_type
   - medical_history
   - admission_date

3. **Doctor**
   - Links to User
   - license_number (unique)
   - specialty (General Surgery, Orthopedic, etc.)
   - department (links to Department)
   - consultation_fee
   - rating

4. **Appointment**
   - patient (links to Patient)
   - doctor (links to Doctor)
   - appointment_date
   - status (SCHEDULED, CONFIRMED, COMPLETED, CANCELLED)
   - cost

5. **Prescription**
   - doctor, patient
   - medication_name
   - dosage, frequency
   - start_date, end_date

6. **MedicalRecord**
   - patient
   - blood_pressure, heart_rate, temperature
   - weight, height

7. **Room**
   - room_number (unique)
   - room_type (GENERAL, PRIVATE, ICU, OPERATION)
   - beds_available
   - daily_rate

8. **RoomReservation**
   - patient, room, doctor
   - check_in_date, check_out_date
   - status

9. **ScanDocument**
   - patient, doctor
   - scan_type (XRAY, MRI, CT, etc.)
   - scan_file, report

---

## Common Tasks

### To Stop the Server
Press `Ctrl + C` in the terminal

### To Reset the Database
```powershell
# ⚠️ WARNING: This deletes all data!
python manage.py migrate zero hospital
python manage.py migrate
python manage.py createsuperuser
```

### To Create a Superuser
```powershell
python manage.py createsuperuser
```

### To Access Django Shell
```powershell
python manage.py shell

# Example commands:
from hospital.models import Doctor
doctors = Doctor.objects.all()
print(doctors)
exit()
```

### To View Database via MySQL
```sql
USE hospital_db;
SELECT * FROM patients;
SELECT * FROM doctors;
SELECT * FROM appointments;
```

---

## Troubleshooting

### Error: "ModuleNotFoundError: No module named 'MySQLdb'"

**Solution**: Install mysqlclient
```powershell
pip install mysqlclient==2.2.6
```

### Error: "Can't connect to MySQL server"

**Solution**: 
1. Make sure MySQL is running (Services or MySQL Workbench)
2. Check username/password in settings.py
3. Verify database name exists

### Error: "No module named 'crispy_forms'"

**Solution**:
```powershell
pip install -r requirements.txt
```

### Error: "TemplateDoesNotExist"

**Solution**: Make sure templates folder exists at:
`d:\UNI\Database Systems\DB_Project\DB-Project\templates\hospital\`

### Page Not Loading / 404 Error

**Solution**:
1. Check URL is correct
2. Check views.py for the view function
3. Check urls.py for URL pattern
4. Restart server

---

## Creating Test Data with Django Shell

```powershell
python manage.py shell
```

```python
from django.contrib.auth.models import User
from hospital.models import Doctor, Patient, Department
from datetime import date

# Create department (if not exists)
dept, _ = Department.objects.get_or_create(
    department_code='SURG001',
    defaults={'name': 'Surgery Department', 'location': 'Building A'}
)

# Create a doctor user and profile
doctor_user = User.objects.create_user(
    username='dralice',
    first_name='Alice',
    last_name='Johnson',
    email='alice@hospital.com',
    password='pass123'
)

doctor = Doctor.objects.create(
    user=doctor_user,
    license_number='LIC789',
    social_security_number='123-45-6789',
    birthdate=date(1980, 5, 15),
    gender='F',
    specialty='SURGERY',
    degree='MD',
    department=dept
)

print(f"Doctor created: Dr. {doctor.user.first_name}")
exit()
```

---

## Performance Tips

1. **Caching**: Add Django cache for frequently accessed data
2. **Database Indexing**: Already configured in models
3. **Static Files**: Collect static files before deployment
4. **Image Optimization**: Resize images before upload

---

## Security Notes

⚠️ **For Development Only!**

Before deploying to production:
1. Change `DEBUG = False` in settings.py
2. Change `SECRET_KEY` to a secure value
3. Set proper `ALLOWED_HOSTS`
4. Enable HTTPS
5. Use environment variables for secrets
6. Set secure database password

---

## Next Steps

1. ✅ Complete template files for all views
2. ✅ Add email notifications
3. ✅ Implement payment gateway
4. ✅ Add analytics dashboard
5. ✅ Deploy to production server
6. ✅ Setup automated backups

---

## Support Resources

- Django Documentation: https://docs.djangoproject.com/
- Bootstrap Documentation: https://getbootstrap.com/docs/
- MySQL Documentation: https://dev.mysql.com/doc/
- Django Forms: https://docs.djangoproject.com/en/stable/topics/forms/

---

**Ready to run? Start with Step 1 above!** 🚀
