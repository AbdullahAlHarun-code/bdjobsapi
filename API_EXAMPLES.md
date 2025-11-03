# 🎯 API Usage Examples

## Real-World Use Cases for Your Smart Job API

---

## 🔥 **Example 1: n8n Daily Job Report**

### **Workflow:**
Every day at 8am, get today's jobs and send email.

### **n8n Nodes:**

1. **Schedule Trigger:** Daily at 8:00 AM

2. **HTTP Request Node:**
   ```
   Method: GET
   URL: https://abdullah007ie.pythonanywhere.com/n8n/get-data/today/
   ```

3. **Function Node:** Format data
   ```javascript
   const jobs = $input.item.json.jobs;
   const count = $input.item.json.count;
   
   return {
     subject: `${count} New Jobs Today`,
     body: jobs.map(j => 
       `${j.company_name} - ${j.position}\n${j.job_url}`
     ).join('\n\n')
   };
   ```

4. **Send Email Node:** Send formatted report

---

## 🔥 **Example 2: BRAC Bank Job Alert**

### **Workflow:**
Check every hour for new BRAC Bank jobs.

### **n8n Nodes:**

1. **Cron Trigger:** Every hour

2. **HTTP Request:**
   ```
   GET /n8n/get-data/?company=BRAC&days=1
   ```

3. **IF Node:** Check if count > 0

4. **Slack/Telegram:** Send notification

---

## 🔥 **Example 3: Engineering Jobs Tracker**

### **Workflow:**
Track engineering positions daily.

### **HTTP Request:**
```
GET /n8n/get-data/?position=Engineer&days=7
GET /n8n/get-data/?position=Developer&days=7
GET /n8n/get-data/?position=Software&days=7
```

### **Combine Results:**
Merge all engineering-related jobs and create weekly report.

---

## 🔥 **Example 4: Compare This Week vs Last Week**

### **Workflow:**

**This Week:**
```javascript
fetch('/n8n/get-data/?days=7')
```

**Last Week (8-14 days ago):**
```javascript
// Calculate dates
const today = new Date();
const weekAgo = new Date(today - 7*24*60*60*1000);
const twoWeeksAgo = new Date(today - 14*24*60*60*1000);

fetch(`/n8n/get-data/?start=${formatDate(twoWeeksAgo)}&end=${formatDate(weekAgo)}`)
```

**Compare counts and trends**

---

## 🔥 **Example 5: Monthly Analytics Dashboard**

### **Data Points:**

```javascript
// Total jobs this month
GET /n8n/get-data/month/

// Group by company (do in code after fetching)
const jobs = response.jobs;
const byCompany = jobs.reduce((acc, job) => {
  acc[job.company_name] = (acc[job.company_name] || 0) + 1;
  return acc;
}, {});

// Top companies
const topCompanies = Object.entries(byCompany)
  .sort((a, b) => b[1] - a[1])
  .slice(0, 10);
```

---

## 🔥 **Example 6: Job Position Trends**

### **Track Popular Positions:**

```javascript
// Get last 30 days
GET /n8n/get-data/?days=30

// Analyze positions
const positions = {};
jobs.forEach(job => {
  const pos = job.position.toLowerCase();
  if (pos.includes('manager')) positions.manager++;
  if (pos.includes('engineer')) positions.engineer++;
  if (pos.includes('developer')) positions.developer++;
  // etc.
});
```

---

## 🔥 **Example 7: Custom Date Range Report**

### **Monthly Report (Nov 1-30):**
```
GET /n8n/get-data/?start=2025-11-01&end=2025-11-30
```

### **Quarterly Report (Q4):**
```
GET /n8n/get-data/?start=2025-10-01&end=2025-12-31
```

### **Specific Week:**
```
GET /n8n/get-data/?start=2025-11-01&end=2025-11-07
```

---

## 🔥 **Example 8: Company Watchlist**

### **Monitor Multiple Companies:**

```python
import requests

companies = ['BRAC', 'Square', 'ACI', 'Healthcare']

for company in companies:
    resp = requests.get(
        'https://abdullah007ie.pythonanywhere.com/n8n/get-data/',
        params={'company': company, 'days': 1}
    )
    data = resp.json()
    
    if data['count'] > 0:
        print(f"🔔 {company}: {data['count']} new jobs!")
        # Send notification
```

---

## 🔥 **Example 9: Position Alert System**

### **Keywords to Track:**
```python
keywords = ['Python', 'Django', 'JavaScript', 'Manager', 'Director']

for keyword in keywords:
    resp = requests.get(
        'https://abdullah007ie.pythonanywhere.com/n8n/get-data/today/',
        params={'position': keyword}
    )
    data = resp.json()
    
    if data['count'] > 0:
        # Send alert for matching jobs
        send_email(f"{keyword} Jobs Alert", data['jobs'])
```

---

## 🔥 **Example 10: Deduplication Check**

### **Before Scraping:**
```python
# Check if job already exists
import requests

def job_exists(job_url):
    resp = requests.get(
        'https://abdullah007ie.pythonanywhere.com/n8n/get-data/',
        params={'days': 30}
    )
    jobs = resp.json()['jobs']
    
    return any(j['job_url'] == job_url for j in jobs)

# Use in scraper
if not job_exists(new_job_url):
    scrape_and_send(new_job)
```

---

## 📊 **Performance Tips**

### **Fast Queries:**
```
✅ /get-data/today/           Fast - single day
✅ /get-data/yesterday/        Fast - single day
✅ /get-data/?days=7          Fast - limited range
⚠️ /get-data/?days=365        Slow - large dataset
⚠️ /get-data/                Slowest - all data
```

### **Optimize:**
- Use specific date ranges
- Filter by company/position when possible
- Cache results if querying frequently
- Use pagination (can add if needed)

---

## 🎨 **Frontend Integration**

### **JavaScript/React:**
```javascript
// Fetch today's jobs
const response = await fetch(
  'https://abdullah007ie.pythonanywhere.com/n8n/get-data/today/'
);
const data = await response.json();

// Display
<div>
  <h2>Today's Jobs: {data.count}</h2>
  {data.jobs.map(job => (
    <JobCard 
      company={job.company_name}
      position={job.position}
      url={job.job_url}
    />
  ))}
</div>
```

### **jQuery:**
```javascript
$.get('/n8n/get-data/today/', function(data) {
  $('#job-count').text(data.count);
  data.jobs.forEach(function(job) {
    $('#job-list').append(`
      <div class="job-card">
        <h3>${job.company_name}</h3>
        <p>${job.position}</p>
        <a href="${job.job_url}">Apply</a>
      </div>
    `);
  });
});
```

---

## 📱 **Mobile App Integration**

### **Android/iOS:**
```kotlin
// Kotlin example
val url = "https://abdullah007ie.pythonanywhere.com/n8n/get-data/today/"
val request = Request.Builder().url(url).build()

client.newCall(request).execute().use { response ->
    val jobs = response.body?.string()
    // Parse JSON and display
}
```

---

## 🎯 **Common Patterns**

### **Pattern 1: Daily Digest**
```
GET /get-data/today/  →  Email at 8am
```

### **Pattern 2: Weekly Summary**
```
GET /get-data/week/   →  Email every Monday
```

### **Pattern 3: Real-time Alerts**
```
GET /get-data/?days=1&position=X  →  Check hourly
```

### **Pattern 4: Historical Analysis**
```
GET /get-data/?start=X&end=Y  →  Generate reports
```

---

## ✅ **Testing Checklist**

After deployment, test these:

- [ ] `GET /get-data/` - All jobs
- [ ] `GET /get-data/today/` - Today's jobs
- [ ] `GET /get-data/yesterday/` - Yesterday's jobs
- [ ] `GET /get-data/week/` - This week
- [ ] `GET /get-data/month/` - This month
- [ ] `GET /get-data/date/2025-11-03/` - Specific date
- [ ] `GET /get-data/?days=7` - Last 7 days
- [ ] `GET /get-data/?company=BRAC` - Company filter
- [ ] `GET /get-data/?position=Engineer` - Position filter
- [ ] `GET /get-data/?days=7&company=BRAC` - Combined

---

**All examples are ready to use!** 🎉

**Base URL:** `https://abdullah007ie.pythonanywhere.com/n8n/`

