# 🏥 Hospital Information System (HIS) - Surgery Department

A complete, production-ready Django-based Hospital Information System for managing patients, doctors, appointments, medical records, and hospital operations.

## ✨ Features

### 👥 For Patients
- ✅ Easy registration and profile setup
- ✅ Browse available doctors by specialty
- ✅ Book and manage appointments
- ✅ Cancel appointments with refunds
- ✅ Access complete medical records
- ✅ View prescriptions
- ✅ View medical scans (X-Ray, MRI, CT, etc.)
- ✅ Profile management

### 👨‍⚕️ For Doctors
- ✅ Professional registration with credentials
- ✅ Manage patient appointments
- ✅ View assigned patients
- ✅ Record patient medical data
- ✅ Write and manage prescriptions
- ✅ Upload patient medical scans
- ✅ Track patient history
- ✅ View ratings and reviews

## 🚀 Quick Start

```powershell
cd "d:\UNI\Database Systems\DB_Project\DB-Project"
..\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Then visit: http://localhost:8000/

See **RUN_INSTRUCTIONS.md** for detailed setup guide.
See **PROJECT_SUMMARY.md** for complete features overview.

## 📱 Access Points

- **Home**: http://localhost:8000/
- **Patient Register**: http://localhost:8000/patient/register/
- **Doctor Register**: http://localhost:8000/doctor/register/
- **Login**: http://localhost:8000/login/
- **Doctors List**: http://localhost:8000/doctors/
- **Admin**: http://localhost:8000/admin/

## 🎨 Stack

- Backend: Django 5.2
- Database: MySQL
- Frontend: Bootstrap 5 + HTML/CSS/JS
- Forms: Django Crispy Forms

## 📁 Documentation

- `RUN_INSTRUCTIONS.md` - Complete setup & run guide
- `SETUP_GUIDE.md` - Database configuration
- `PROJECT_SUMMARY.md` - Features & architecture

**Ready to launch in 5 minutes!** 🚀
