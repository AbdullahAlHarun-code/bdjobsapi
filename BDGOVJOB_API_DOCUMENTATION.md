# 🏛️ BD Government Jobs API Documentation

## 📊 Overview

API for managing Bangladesh Government Job circulars scraped from **bdgovtjob.net**.

**Base URL:** `http://your-domain.com/bdgovjob/`

---

## 📋 Data Model

### GovtJob Fields

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `id` | Integer | Unique ID | `1` |
| `job_title` | Text | Full job circular title | "Planning Division Job Circular 2025 plandiv.teletalk.com.bd" |
| `job_url` | URL | Link to job circular (unique) | "https://bdgovtjob.net/planning-division-job-circular/" |
| `vacancies` | String | Number of positions | "65" |
| `deadline` | String | Application deadline | "25 November 2025 at 5:00 PM" |
| `posted_date` | String | When job was posted | "3 November, 2025" |
| `scraped_at` | DateTime | When data was scraped | "2025-11-03 23:12:47" |
| `created_at` | DateTime | When record was created | "2025-11-03T23:15:00Z" |
| `updated_at` | DateTime | Last update time | "2025-11-03T23:15:00Z" |

---

## 🔌 API Endpoints

### 1. **POST /bdgovjob/send-data/**

Send scraped government job data to the API.

**Request Body:**

```json
{
  "job_title": "Ministry of Home Affairs MOHA Job Circular 2025 – moha.teletalk.com.bd",
  "job_url": "https://bdgovtjob.net/moha-job-circular/",
  "vacancies": "85",
  "deadline": "23 November 2025 at 5:00 PM",
  "posted_date": "3 November, 2025",
  "scraped_at": "2025-11-03 23:12:47"
}
```

**Or send multiple jobs:**

```json
[
  {
    "job_title": "Planning Division Job Circular 2025",
    "job_url": "https://bdgovtjob.net/planning-division-job-circular/",
    "vacancies": "65",
    "deadline": "25 November 2025 at 5:00 PM",
    "posted_date": "3 November, 2025",
    "scraped_at": "2025-11-03 10:30:00"
  },
  {
    "job_title": "Bangladesh Bank Job Circular 2025",
    "job_url": "https://bdgovtjob.net/bangladesh-bank-job-circular/",
    "vacancies": "125",
    "deadline": "30 November 2025",
    "posted_date": "2 November, 2025",
    "scraped_at": "2025-11-03 10:30:15"
  }
]
```

**Response (201 Created):**

```json
{
  "created": [
    {
      "id": 1,
      "job_title": "Planning Division Job Circular 2025",
      "job_url": "https://bdgovtjob.net/planning-division-job-circular/",
      "vacancies": "65",
      "deadline": "25 November 2025 at 5:00 PM",
      "posted_date": "3 November, 2025",
      "scraped_at": "2025-11-03T10:30:00Z",
      "created_at": "2025-11-03T23:15:00Z",
      "updated_at": "2025-11-03T23:15:00Z"
    }
  ],
  "updated": [],
  "skipped": [],
  "total_created": 1,
  "total_updated": 0,
  "total_errors": 0
}
```

**Features:**
- ✅ Creates new jobs
- ✅ Updates existing jobs (based on `job_url`)
- ✅ Deduplication by `job_url`
- ✅ Bulk upload support

---

### 2. **GET /bdgovjob/get-data/**

Retrieve government jobs with optional filters.

**Query Parameters:**

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `days` | Integer | Last N days | `?days=7` |
| `start` | Date | Start date (YYYY-MM-DD) | `?start=2025-11-01` |
| `end` | Date | End date (YYYY-MM-DD) | `?end=2025-11-30` |
| `title` | String | Search in job title | `?title=Planning` |
| `vacancies` | String | Filter by vacancies | `?vacancies=65` |
| `deadline` | String | Search in deadline | `?deadline=November` |

**Examples:**

```bash
# Get all jobs
GET /bdgovjob/get-data/

# Get jobs from last 7 days
GET /bdgovjob/get-data/?days=7

# Get jobs with "Bank" in title
GET /bdgovjob/get-data/?title=Bank

# Get jobs with specific vacancy count
GET /bdgovjob/get-data/?vacancies=100

# Get jobs with deadline in November
GET /bdgovjob/get-data/?deadline=November

# Combine filters
GET /bdgovjob/get-data/?days=7&title=Bank&vacancies=100
```

**Response (200 OK):**

```json
{
  "filters": {
    "days": "7",
    "start_date": null,
    "end_date": null,
    "title": "Bank",
    "vacancies": null,
    "deadline": null
  },
  "count": 3,
  "jobs": [
    {
      "id": 7,
      "job_title": "Bangladesh Bank Job Circular 2025",
      "job_url": "https://bdgovtjob.net/bangladesh-bank-job-circular/",
      "vacancies": "1,017",
      "deadline": "10 November 2025",
      "posted_date": "3 November, 2025",
      "scraped_at": "2025-11-03T10:30:00Z",
      "created_at": "2025-11-03T23:15:00Z",
      "updated_at": "2025-11-03T23:15:00Z"
    }
  ]
}
```

---

### 3. **GET /bdgovjob/get-data/today/**

Get jobs scraped today.

**Response:**

```json
{
  "date": "2025-11-03",
  "count": 50,
  "jobs": [...]
}
```

---

### 4. **GET /bdgovjob/get-data/yesterday/**

Get jobs scraped yesterday.

**Response:**

```json
{
  "date": "2025-11-02",
  "count": 45,
  "jobs": [...]
}
```

---

### 5. **GET /bdgovjob/get-data/week/**

Get jobs scraped in the last 7 days.

**Response:**

```json
{
  "period": "last_7_days",
  "from": "2025-10-27",
  "to": "2025-11-03",
  "count": 200,
  "jobs": [...]
}
```

---

### 6. **GET /bdgovjob/get-data/month/**

Get jobs scraped this month.

**Response:**

```json
{
  "period": "current_month",
  "month": "November 2025",
  "from": "2025-11-01",
  "to": "2025-11-03",
  "count": 150,
  "jobs": [...]
}
```

---

### 7. **GET /bdgovjob/get-data/date/{date}/**

Get jobs scraped on a specific date.

**Example:**

```bash
GET /bdgovjob/get-data/date/2025-11-03/
```

**Response:**

```json
{
  "date": "2025-11-03",
  "count": 200,
  "jobs": [...]
}
```

---

### 8. **GET /bdgovjob/stats/**

Get statistics about government jobs.

**Response:**

```json
{
  "total_jobs": 500,
  "today": 50,
  "this_week": 200,
  "this_month": 450,
  "with_vacancies": 480,
  "with_deadlines": 495,
  "last_updated": "2025-11-03T23:15:00Z"
}
```

---

## 🔧 Integration Examples

### Python (from bdgovtjob scraper)

```python
import requests
import json

# Send scraped data to API
def send_to_api(jobs_data):
    api_url = "http://your-domain.com/bdgovjob/send-data/"
    
    response = requests.post(
        api_url,
        json=jobs_data,
        headers={'Content-Type': 'application/json'}
    )
    
    return response.json()

# Example usage
with open('bdgovtjob_data.json', 'r', encoding='utf-8') as f:
    jobs = json.load(f)

result = send_to_api(jobs)
print(f"Created: {result['total_created']}")
print(f"Updated: {result['total_updated']}")
```

### cURL

```bash
# Send single job
curl -X POST http://your-domain.com/bdgovjob/send-data/ \
  -H "Content-Type: application/json" \
  -d '{
    "job_title": "Planning Division Job Circular 2025",
    "job_url": "https://bdgovtjob.net/planning-division-job-circular/",
    "vacancies": "65",
    "deadline": "25 November 2025 at 5:00 PM",
    "posted_date": "3 November, 2025",
    "scraped_at": "2025-11-03 23:12:47"
  }'

# Get today's jobs
curl http://your-domain.com/bdgovjob/get-data/today/

# Get jobs with filters
curl "http://your-domain.com/bdgovjob/get-data/?title=Bank&days=7"
```

### JavaScript (fetch)

```javascript
// Send data
async function sendGovtJobs(jobsData) {
  const response = await fetch('http://your-domain.com/bdgovjob/send-data/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(jobsData)
  });
  
  return await response.json();
}

// Get data with filters
async function getGovtJobs(filters = {}) {
  const params = new URLSearchParams(filters);
  const response = await fetch(`http://your-domain.com/bdgovjob/get-data/?${params}`);
  return await response.json();
}

// Usage
const result = await sendGovtJobs([
  {
    job_title: "Planning Division Job Circular 2025",
    job_url: "https://bdgovtjob.net/planning-division-job-circular/",
    vacancies: "65",
    deadline: "25 November 2025 at 5:00 PM",
    posted_date: "3 November, 2025",
    scraped_at: "2025-11-03 23:12:47"
  }
]);

const todayJobs = await getGovtJobs({ days: 1 });
```

---

## 🚀 Setup & Deployment

### 1. Run Migrations

```bash
cd bdjob_api_restframework/django-n8n-api
python manage.py makemigrations bdgovjob
python manage.py migrate
```

### 2. Create Superuser (optional)

```bash
python manage.py createsuperuser
```

### 3. Run Server

```bash
python manage.py runserver 0.0.0.0:8000
```

### 4. Access Admin Panel

```
http://your-domain.com/admin/
```

---

## 📊 Comparison: n8n vs bdgovjob

| Feature | n8n (Hot Jobs) | bdgovjob (Govt Jobs) |
|---------|----------------|----------------------|
| **Base URL** | `/n8n/` | `/bdgovjob/` |
| **Model** | `HotJob` | `GovtJob` |
| **Source** | bdjobs.com | bdgovtjob.net |
| **Fields** | 5 (company, logo, position, url, date) | 6 (title, url, vacancies, deadline, posted, scraped) |
| **Unique Key** | `job_url` | `job_url` |
| **Stats Endpoint** | ❌ No | ✅ Yes |
| **Update Support** | ❌ No | ✅ Yes |

---

## 🎯 Best Practices

### 1. Deduplication

The API uses `job_url` as a unique identifier:
- **First POST:** Creates new record
- **Subsequent POST (same URL):** Updates existing record
- No manual duplicate checking needed!

### 2. Batch Processing

Send up to 200 jobs per request for optimal performance:

```python
# Good: Batch upload
requests.post(api_url, json=jobs[0:200])

# Less optimal: One by one
for job in jobs:
    requests.post(api_url, json=job)
```

### 3. Error Handling

Always check the response for errors:

```python
response = requests.post(api_url, json=jobs_data)
result = response.json()

if result.get('total_errors', 0) > 0:
    print("Errors:", result['errors'])
```

### 4. Filtering

Use specific filters for better performance:

```bash
# Good: Specific filter
/bdgovjob/get-data/?days=7&title=Bank

# Less optimal: Get all then filter client-side
/bdgovjob/get-data/  # Returns all records
```

---

## 🔄 Integration with Scraper

Update your `bdgovtjob.py` scraper to send data to the API:

```python
def send_jobs_to_api(self, api_url):
    """Send scraped jobs to Django API"""
    if not self.all_jobs:
        print("⚠ No jobs to send")
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
            print(f"✅ API Response:")
            print(f"   Created: {result['total_created']}")
            print(f"   Updated: {result['total_updated']}")
            print(f"   Errors: {result['total_errors']}")
            return True
        else:
            print(f"❌ API Error: {response.status_code}")
            print(response.text)
            return False
            
    except Exception as e:
        print(f"❌ Failed to send to API: {e}")
        return False

# Usage in main()
if jobs:
    api_url = os.environ.get('API_URL', 'http://localhost:8000/bdgovjob/send-data/')
    scraper.send_jobs_to_api(api_url)
```

---

## ✅ Testing

```bash
# Run tests
python manage.py test apps.bdgovjob

# Check API is working
curl http://localhost:8000/bdgovjob/stats/
```

---

## 📚 Related Documentation

- [BD Hot Jobs API](./API_DOCUMENTATION.md) - For n8n integration
- [Scraper Guide](../../github_bdjob/BDGOVTJOB_README.md) - How to use the scraper
- [Deployment Guide](./DEPLOYMENT_PYTHONANYWHERE.md) - Deploy to PythonAnywhere

---

**API is ready to use!** 🎉

Start scraping and sending data:
```bash
cd github_bdjob
python bdgovtjob.py
```

