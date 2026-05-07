# ⚡ QUICK REFERENCE GUIDE

## 🎯 What Was Created

### Backend (Django)
✅ 11 Database Models with 50+ fields
✅ 25+ View Functions (auth, patient, doctor, admin)
✅ 12 Django Forms (registration, appointments, etc.)
✅ Complete Admin Interface
✅ URL Routing for all features
✅ MySQL Database Configuration

### Frontend (HTML/CSS)
✅ Professional Bootstrap 5 Design
✅ 8+ Complete Templates
✅ Responsive Mobile Layout
✅ Icon-based UI
✅ Modern Color Scheme
✅ Navigation & Footer

### Configuration
✅ Django Settings (settings.py)
✅ URL Configuration (urls.py)
✅ Admin Setup (admin.py)
✅ Requirements.txt with all dependencies

---

## 🚀 START HERE (Copy-Paste Commands)

### Step 1: Setup Environment
```powershell
cd "d:\UNI\Database Systems\DB_Project"
.\venv\Scripts\Activate.ps1
cd DB-Project
```

### Step 2: Install Dependencies
```powershell
pip install -r requirements.txt
```

### Step 3: Create Database
In MySQL or MySQL Workbench:
```sql
CREATE DATABASE hospital_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### Step 4: Update Database Credentials
Edit: `his_config/settings.py` (around line 80)

Change these lines:
```python
'NAME': 'hospital_db',      # Your database name
'USER': 'root',              # Your MySQL username
'PASSWORD': 'your_password', # Your MySQL password
```

### Step 5: Run Migrations
```powershell
python manage.py makemigrations
python manage.py migrate
```

### Step 6: Create Admin User
```powershell
python manage.py createsuperuser
```

When prompted, enter:
- Username: admin
- Email: admin@hospital.com
- Password: (choose one)

### Step 7: Create Department
```powershell
python manage.py shell
```

Then copy-paste:
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

### Step 8: Start Server
```powershell
python manage.py runserver
```

### Step 9: Open Browser
Visit: **http://localhost:8000/**

---

## 📖 Files to Read

In order of importance:

1. **RUN_INSTRUCTIONS.md** - How to setup and run
2. **PROJECT_SUMMARY.md** - What's included
3. **SETUP_GUIDE.md** - Detailed database setup
4. **README.md** - Project overview

---

## 📁 Key Files to Know

```
his_config/settings.py   <- EDIT DATABASE HERE
hospital/models.py       <- Database models
hospital/views.py        <- All functionality
hospital/forms.py        <- Form definitions
templates/hospital/      <- HTML pages
requirements.txt         <- Python packages
manage.py               <- Django management
```

---

## 🌐 URLs to Remember

| What | URL |
|------|-----|
| Main Site | http://localhost:8000/ |
| Admin Panel | http://localhost:8000/admin/ |
| Patient Register | http://localhost:8000/patient/register/ |
| Doctor Register | http://localhost:8000/doctor/register/ |
| Login | http://localhost:8000/login/ |
| Doctors | http://localhost:8000/doctors/ |

---

## 🧪 Test the System

### Create Test Patient
1. Go to http://localhost:8000/patient/register/
2. Fill form and register
3. Complete profile
4. Go to dashboard

### Create Test Doctor
1. Go to http://localhost:8000/doctor/register/
2. Fill form and register
3. Complete profile with credentials

### Book Appointment
1. Login as patient
2. Click "Book New Appointment"
3. Select doctor and date
4. Confirm

---

## 🐛 If Something Goes Wrong

### Error: "Can't connect to MySQL server"
- Check MySQL is running
- Verify credentials in settings.py
- Make sure database exists

### Error: "ModuleNotFoundError"
- Run: `pip install -r requirements.txt`

### Error: "TemplateDoesNotExist"
- Check templates folder exists
- Restart server

### Port 8000 already in use
- Run: `python manage.py runserver 8001`

---

## 💡 Pro Tips

1. Always activate venv before running commands
2. Restart server after changing settings.py
3. Use admin panel to view/manage all data
4. Check browser console (F12) for errors
5. Read error messages carefully - they help!

---

## ⏱️ Expected Time

- Install dependencies: 2 min
- Database setup: 2 min
- Run migrations: 1 min
- Start server: 30 sec

**Total: ~5-10 minutes to launch!**

---

## 📚 Documentation

- Django: https://docs.djangoproject.com/
- Bootstrap: https://getbootstrap.com/docs/
- MySQL: https://dev.mysql.com/doc/

---

## ✅ Checklist

Before starting:
- [ ] Python 3.8+ installed
- [ ] MySQL 5.7+ installed
- [ ] VS Code ready
- [ ] Terminal open

Ready to go? Start with Step 1 above! 🚀

---

## 🎯 Next Steps After Launch

1. ✅ Complete any remaining templates
2. ✅ Add sample doctors/rooms via admin
3. ✅ Test all features
4. ✅ Customize styling
5. ✅ Add email notifications
6. ✅ Deploy to production

---

**Questions?** Check the markdown files or Django documentation.

**Ready?** Go to Step 1 above and launch! 🚀
