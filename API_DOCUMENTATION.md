# 📚 BDJobs API - Complete Documentation

## 🌟 Smart Filtering API

Your API now supports smart filtering by date, time periods, company, and position!

---

## 📡 **API Endpoints**

Base URL: `https://abdullah007ie.pythonanywhere.com/n8n/`

---

## 📤 **1. Send Data (POST)**

### **Endpoint:**
```
POST /n8n/send-data/
```

### **Purpose:**
Receive scraped job data from your scraper.

### **Request Body:**
```json
[
  {
    "company_name": "BRAC Bank PLC",
    "company_logo_url": "https://hotjobs.bdjobs.com/logos/bracbank300-min.png",
    "position": "ESG Analyst, ESG and Sustainable Finance",
    "job_url": "https://hotjobs.bdjobs.com/jobs/bracbank/bracbank859.htm",
    "scraped_date": "2025-11-03 12:00:00"
  }
]
```

### **Response:**
```json
{
  "created": [...],  // Newly created jobs
  "skipped": [...],  // Duplicate jobs
  "errors": [...]    // Validation errors (if any)
}
```

---

## 📥 **2. Get All Data (with Filters)**

### **Endpoint:**
```
GET /n8n/get-data/
```

### **Query Parameters:**

| Parameter | Type | Example | Description |
|-----------|------|---------|-------------|
| `days` | integer | `?days=7` | Last N days |
| `start` | date | `?start=2025-11-01` | From date (YYYY-MM-DD) |
| `end` | date | `?end=2025-11-03` | To date (YYYY-MM-DD) |
| `company` | string | `?company=BRAC` | Company name contains |
| `position` | string | `?position=Engineer` | Position contains |

### **Examples:**

#### **All jobs (no filter):**
```
GET /n8n/get-data/
```

#### **Last 7 days:**
```
GET /n8n/get-data/?days=7
```

#### **Date range:**
```
GET /n8n/get-data/?start=2025-11-01&end=2025-11-03
```

#### **Filter by company:**
```
GET /n8n/get-data/?company=BRAC
```

#### **Filter by position:**
```
GET /n8n/get-data/?position=Engineer
```

#### **Combine filters:**
```
GET /n8n/get-data/?days=7&company=BRAC&position=Manager
```

### **Response:**
```json
{
  "filters": {
    "days": "7",
    "start_date": null,
    "end_date": null,
    "company": "BRAC",
    "position": "Manager"
  },
  "count": 15,
  "jobs": [
    {
      "id": 123,
      "company_name": "BRAC Bank PLC",
      "company_logo_url": "https://...",
      "position": "Manager, ESG and Sustainable Finance",
      "job_url": "https://...",
      "scraped_date": "2025-11-03T12:00:00Z",
      "created_at": "2025-11-03T12:05:30Z"
    }
  ]
}
```

---

## 📅 **3. Get Today's Jobs**

### **Endpoint:**
```
GET /n8n/get-data/today/
```

### **Example:**
```
GET https://abdullah007ie.pythonanywhere.com/n8n/get-data/today/
```

### **Response:**
```json
{
  "date": "2025-11-03",
  "count": 242,
  "jobs": [...]
}
```

---

## 📅 **4. Get Yesterday's Jobs**

### **Endpoint:**
```
GET /n8n/get-data/yesterday/
```

### **Example:**
```
GET https://abdullah007ie.pythonanywhere.com/n8n/get-data/yesterday/
```

### **Response:**
```json
{
  "date": "2025-11-02",
  "count": 238,
  "jobs": [...]
}
```

---

## 📅 **5. Get This Week's Jobs**

### **Endpoint:**
```
GET /n8n/get-data/week/
```

### **Description:**
Returns jobs from the last 7 days.

### **Example:**
```
GET https://abdullah007ie.pythonanywhere.com/n8n/get-data/week/
```

### **Response:**
```json
{
  "period": "last_7_days",
  "from": "2025-10-27",
  "to": "2025-11-03",
  "count": 1680,
  "jobs": [...]
}
```

---

## 📅 **6. Get This Month's Jobs**

### **Endpoint:**
```
GET /n8n/get-data/month/
```

### **Description:**
Returns all jobs from the current month (Nov 1 - Nov 30).

### **Example:**
```
GET https://abdullah007ie.pythonanywhere.com/n8n/get-data/month/
```

### **Response:**
```json
{
  "period": "current_month",
  "month": "November 2025",
  "from": "2025-11-01",
  "to": "2025-11-03",
  "count": 720,
  "jobs": [...]
}
```

---

## 📅 **7. Get Specific Date**

### **Endpoint:**
```
GET /n8n/get-data/date/<YYYY-MM-DD>/
```

### **Examples:**
```
GET /n8n/get-data/date/2025-11-03/
GET /n8n/get-data/date/2025-11-01/
GET /n8n/get-data/date/2025-10-15/
```

### **Response:**
```json
{
  "date": "2025-11-03",
  "count": 242,
  "jobs": [...]
}
```

### **Error Response (Invalid Date):**
```json
{
  "error": "Invalid date format. Use YYYY-MM-DD (e.g., 2025-11-03)"
}
```

---

## 🎯 **Use Cases**

### **Use Case 1: n8n Workflow - Get Today's Jobs**
```
HTTP Request Node:
  Method: GET
  URL: https://abdullah007ie.pythonanywhere.com/n8n/get-data/today/
  
Response:
  {{ $json.jobs }}  → Array of today's jobs
  {{ $json.count }} → Number of jobs
```

### **Use Case 2: Dashboard - Last Week's Jobs**
```
GET /n8n/get-data/week/

Show in dashboard:
- Total jobs this week: 1680
- Chart of jobs per day
- Company breakdown
```

### **Use Case 3: Search for Specific Company**
```
GET /n8n/get-data/?company=BRAC&days=30

Results:
- All BRAC jobs from last 30 days
- Can filter further by position
```

### **Use Case 4: Job Alerts by Position**
```
GET /n8n/get-data/?position=Developer&days=1

Results:
- All developer jobs from today
- Send email alert with these jobs
```

---

## 🔍 **Filter Combinations**

### **Popular Queries:**

#### **Today's engineering jobs:**
```
GET /n8n/get-data/today/?position=Engineer
```

#### **BRAC jobs this month:**
```
GET /n8n/get-data/month/?company=BRAC
```

#### **Last 3 days, specific company:**
```
GET /n8n/get-data/?days=3&company=Square
```

#### **Date range for specific position:**
```
GET /n8n/get-data/?start=2025-11-01&end=2025-11-03&position=Manager
```

---

## 📊 **Response Format**

### **Filtered Endpoint Response:**
```json
{
  "filters": {
    "days": "7",
    "start_date": null,
    "end_date": null,
    "company": "BRAC",
    "position": null
  },
  "count": 25,
  "jobs": [
    {
      "id": 1,
      "company_name": "BRAC Bank PLC",
      "company_logo_url": "https://hotjobs.bdjobs.com/logos/bracbank300-min.png",
      "position": "ESG Analyst, ESG and Sustainable Finance",
      "job_url": "https://hotjobs.bdjobs.com/jobs/bracbank/bracbank859.htm",
      "scraped_date": "2025-11-03T12:00:00Z",
      "created_at": "2025-11-03T12:05:30.123456Z"
    }
  ]
}
```

### **Time-Based Endpoint Response:**
```json
{
  "date": "2025-11-03",  // or "period", "month"
  "count": 242,
  "jobs": [...]
}
```

---

## 🔧 **Testing the API**

### **Using curl:**

```bash
# Get today's jobs
curl https://abdullah007ie.pythonanywhere.com/n8n/get-data/today/

# Get yesterday's jobs
curl https://abdullah007ie.pythonanywhere.com/n8n/get-data/yesterday/

# Get last 7 days
curl https://abdullah007ie.pythonanywhere.com/n8n/get-data/?days=7

# Filter by company
curl "https://abdullah007ie.pythonanywhere.com/n8n/get-data/?company=BRAC"

# Specific date
curl https://abdullah007ie.pythonanywhere.com/n8n/get-data/date/2025-11-03/
```

### **Using Python:**

```python
import requests

# Get today's jobs
response = requests.get('https://abdullah007ie.pythonanywhere.com/n8n/get-data/today/')
data = response.json()
print(f"Today's jobs: {data['count']}")

# Filter by company
response = requests.get('https://abdullah007ie.pythonanywhere.com/n8n/get-data/', 
                       params={'company': 'BRAC', 'days': 7})
data = response.json()
print(f"BRAC jobs (last 7 days): {data['count']}")
```

### **Using Browser:**
```
https://abdullah007ie.pythonanywhere.com/n8n/get-data/today/
https://abdullah007ie.pythonanywhere.com/n8n/get-data/?days=7
https://abdullah007ie.pythonanywhere.com/n8n/get-data/?company=BRAC
```

---

## 📋 **Quick Reference**

### **All Endpoints:**

| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/send-data/` | Submit scraped jobs |
| GET | `/get-data/` | Get all (with optional filters) |
| GET | `/get-data/today/` | Today's jobs |
| GET | `/get-data/yesterday/` | Yesterday's jobs |
| GET | `/get-data/week/` | Last 7 days |
| GET | `/get-data/month/` | Current month |
| GET | `/get-data/date/YYYY-MM-DD/` | Specific date |

---

## 🚀 **Deployment**

### **On PythonAnywhere:**

1. Upload updated files via Files tab:
   - `api_views.py`
   - `urls.py`

2. Reload your web app:
   - Go to Web tab
   - Click "Reload" button

3. Test new endpoints:
   ```
   https://abdullah007ie.pythonanywhere.com/n8n/get-data/today/
   ```

---

## 💡 **Best Practices**

### **For n8n Workflows:**
- Use `/get-data/today/` for daily reports
- Use `/get-data/?days=7&company=X` for targeted searches
- Cache results to avoid repeated queries

### **For Dashboards:**
- Use `/get-data/week/` for charts
- Use `/get-data/?position=X` for job alerts
- Poll `/get-data/today/` every hour for new jobs

### **For Analytics:**
- Use `/get-data/month/` for monthly reports
- Use date ranges for custom periods
- Combine filters for detailed analysis

---

## ⚠️ **Important Notes**

1. **Timezone:** All times are in server timezone (UTC or configured)
2. **created_at:** When job was saved to database
3. **scraped_date:** When scraper found the job (from scraper)
4. **Deduplication:** Uses `job_url` to avoid duplicates
5. **Case-insensitive:** Company and position filters ignore case

---

## 🎉 **What Changed:**

### **Before:**
```
GET /get-data/  →  Returns ALL jobs (thousands!)
```

### **After:**
```
GET /get-data/today/          →  Only today's ~240 jobs
GET /get-data/?days=7         →  Last week's jobs
GET /get-data/?company=BRAC   →  Only BRAC jobs
```

**Much smarter and faster!** 🚀

---

## 📞 **Support**

For issues or questions:
- Check Django logs
- Test with curl or browser
- Verify date formats (YYYY-MM-DD)
- Check timezone settings

---

**Your API is now production-ready with smart filtering!** ✅

