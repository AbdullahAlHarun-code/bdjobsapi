# 🚀 Quick Setup Guide - BD Government Jobs API

## ✅ Step-by-Step Setup

### **Step 1: Navigate to Django Project**

```bash
cd bdjob_api_restframework/django-n8n-api
```

### **Step 2: Create Migrations**

```bash
python manage.py makemigrations bdgovjob
```

**Expected Output:**
```
Migrations for 'bdgovjob':
  apps/bdgovjob/migrations/0001_initial.py
    - Create model GovtJob
```

### **Step 3: Run Migrations**

```bash
python manage.py migrate
```

**Expected Output:**
```
Running migrations:
  Applying bdgovjob.0001_initial... OK
```

### **Step 4: Create Superuser (Optional)**

```bash
python manage.py createsuperuser
```

Follow prompts to create admin account.

### **Step 5: Start Server**

```bash
python manage.py runserver 0.0.0.0:8000
```

**Expected Output:**
```
Starting development server at http://0.0.0.0:8000/
Quit the server with CTRL-BREAK.
```

---

## 🧪 Test the API

### **1. Check Stats Endpoint**

```bash
curl http://localhost:8000/bdgovjob/stats/
```

**Expected Response:**
```json
{
  "total_jobs": 0,
  "today": 0,
  "this_week": 0,
  "this_month": 0,
  "with_vacancies": 0,
  "with_deadlines": 0,
  "last_updated": null
}
```

### **2. Send Test Data**

```bash
curl -X POST http://localhost:8000/bdgovjob/send-data/ \
  -H "Content-Type: application/json" \
  -d '{
    "job_title": "Planning Division Job Circular 2025",
    "job_url": "https://bdgovtjob.net/planning-division-job-circular/",
    "vacancies": "65",
    "deadline": "25 November 2025 at 5:00 PM",
    "posted_date": "3 November, 2025",
    "scraped_at": "2025-11-03 23:12:47"
  }'
```

**Expected Response:**
```json
{
  "created": [{
    "id": 1,
    "job_title": "Planning Division Job Circular 2025",
    ...
  }],
  "updated": [],
  "skipped": [],
  "total_created": 1,
  "total_updated": 0,
  "total_errors": 0
}
```

### **3. Get Today's Jobs**

```bash
curl http://localhost:8000/bdgovjob/get-data/today/
```

### **4. Check Stats Again**

```bash
curl http://localhost:8000/bdgovjob/stats/
```

**Expected Response:**
```json
{
  "total_jobs": 1,
  "today": 1,
  "this_week": 1,
  "this_month": 1,
  "with_vacancies": 1,
  "with_deadlines": 1,
  "last_updated": "2025-11-03T23:15:00Z"
}
```

---

## 📊 Admin Panel

### **1. Access Admin**

```
http://localhost:8000/admin/
```

### **2. Login**

Use the superuser credentials you created.

### **3. View Government Jobs**

Navigate to: **Home > Bdgovjob > Government Jobs**

You can:
- ✅ View all jobs
- ✅ Search by title, vacancies, deadline
- ✅ Filter by date
- ✅ Edit/Delete jobs

---

## 🔗 API Endpoints Summary

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/bdgovjob/send-data/` | POST | Submit job data |
| `/bdgovjob/get-data/` | GET | Get all jobs (with filters) |
| `/bdgovjob/get-data/today/` | GET | Today's jobs |
| `/bdgovjob/get-data/yesterday/` | GET | Yesterday's jobs |
| `/bdgovjob/get-data/week/` | GET | Last 7 days |
| `/bdgovjob/get-data/month/` | GET | This month |
| `/bdgovjob/get-data/date/2025-11-03/` | GET | Specific date |
| `/bdgovjob/stats/` | GET | Statistics |

---

## 🔧 Environment Variables (Optional)

Create `.env` file:

```env
# Django Settings
DJANGO_SECRET_KEY=your-secret-key-here
DJANGO_DEBUG=True

# Database (if using PostgreSQL/MySQL)
DJANGO_DB_ENGINE=django.db.backends.postgresql
DJANGO_DB_NAME=bdgovjob_db
DJANGO_DB_USER=your_db_user
DJANGO_DB_PASSWORD=your_db_password
DJANGO_DB_HOST=localhost
DJANGO_DB_PORT=5432
```

---

## 📁 Project Structure

```
bdjob_api_restframework/django-n8n-api/
├── apps/
│   ├── n8n_integration/          # Hot Jobs (BDJobs)
│   │   ├── models.py              # HotJob model
│   │   ├── api_views.py           # Hot jobs API
│   │   └── urls.py                # /n8n/ routes
│   │
│   └── bdgovjob/                  # Govt Jobs (NEW)
│       ├── models.py              # GovtJob model ✨
│       ├── api_views.py           # Govt jobs API ✨
│       ├── urls.py                # /bdgovjob/ routes ✨
│       ├── serializers.py         # Serializers ✨
│       ├── admin.py               # Admin config ✨
│       └── migrations/            # Database migrations ✨
│
├── api_project/
│   ├── settings.py                # ✅ Updated (added bdgovjob)
│   ├── urls.py                    # ✅ Updated (added /bdgovjob/)
│   └── wsgi.py
│
├── manage.py
├── BDGOVJOB_API_DOCUMENTATION.md  # ✨ API docs
└── SETUP_BDGOVJOB.md              # ✨ This file
```

---

## 🎯 Next Steps

### **1. Update Scraper to Send Data**

Edit `github_bdjob/bdgovtjob.py`:

```python
def send_jobs_to_api(self, api_url):
    """Send scraped jobs to Django API"""
    if not self.all_jobs:
        return False
    
    try:
        response = requests.post(
            api_url,
            json=self.all_jobs,
            headers={'Content-Type': 'application/json'},
            timeout=30
        )
        
        if response.status_code in [200, 201]:
            result = response.json()
            print(f"✅ Created: {result['total_created']}")
            print(f"✅ Updated: {result['total_updated']}")
            return True
        return False
    except Exception as e:
        print(f"❌ API Error: {e}")
        return False

# In main() function:
if jobs:
    scraper.save_to_csv()
    scraper.save_to_json()
    
    # Send to API
    api_url = os.environ.get(
        'API_URL',
        'http://localhost:8000/bdgovjob/send-data/'
    )
    scraper.send_jobs_to_api(api_url)
```

### **2. Test End-to-End**

```bash
# Terminal 1: Run Django server
cd bdjob_api_restframework/django-n8n-api
python manage.py runserver

# Terminal 2: Run scraper
cd github_bdjob
set API_URL=http://localhost:8000/bdgovjob/send-data/
python bdgovtjob.py
```

### **3. Deploy to Production**

See `DEPLOYMENT_PYTHONANYWHERE.md` for deployment instructions.

---

## ✅ Verification Checklist

- [ ] Migrations created and applied
- [ ] Server starts without errors
- [ ] `/bdgovjob/stats/` returns JSON
- [ ] Can POST test data successfully
- [ ] Admin panel accessible
- [ ] Can view jobs in admin
- [ ] Scraper can send data to API

---

## 🆘 Troubleshooting

### **Problem: ModuleNotFoundError: No module named 'apps.bdgovjob'**

**Solution:**
```bash
# Make sure you're in the correct directory
cd bdjob_api_restframework/django-n8n-api

# Restart the server
python manage.py runserver
```

### **Problem: Table doesn't exist**

**Solution:**
```bash
python manage.py makemigrations bdgovjob
python manage.py migrate
```

### **Problem: API returns 404**

**Solution:**
Check that URL is correct:
- ✅ `http://localhost:8000/bdgovjob/stats/`
- ❌ `http://localhost:8000/bdgovtjob/stats/` (wrong spelling)

### **Problem: CSRF Error when using POST**

**Solution:**
Add header: `-H "Content-Type: application/json"`

Or disable CSRF for API endpoints (add to middleware settings).

---

## 📚 Resources

- **API Documentation:** `BDGOVJOB_API_DOCUMENTATION.md`
- **Scraper Guide:** `../../github_bdjob/BDGOVTJOB_README.md`
- **Original API:** `API_DOCUMENTATION.md` (Hot Jobs)

---

**Setup Complete! 🎉**

Your BD Government Jobs API is ready to receive scraped data!

