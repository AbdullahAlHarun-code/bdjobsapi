# 🚀 Deploy Updated API to PythonAnywhere

## 📝 What Changed

I've added **smart filtering endpoints** to your API:

✅ Get today's jobs  
✅ Get yesterday's jobs  
✅ Get this week's jobs  
✅ Get this month's jobs  
✅ Get specific date  
✅ Filter by company  
✅ Filter by position  
✅ Combine filters  

---

## 📁 Files Updated

1. ✅ `apps/n8n_integration/api_views.py` - Added 5 new view classes
2. ✅ `apps/n8n_integration/urls.py` - Added new URL patterns
3. ✅ `API_DOCUMENTATION.md` - Complete API docs
4. ✅ `API_EXAMPLES.md` - Usage examples

**No database changes needed!** Uses existing `HotJob` model.

---

## 🚀 Deploy to PythonAnywhere

### **Step 1: Upload Updated Files**

1. Go to: https://www.pythonanywhere.com
2. Login as: `abdullah007ie`
3. Go to: **Files** tab
4. Navigate to: `/home/abdullah007ie/django-n8n-api/apps/n8n_integration/`

5. **Upload these 2 files:**
   - `api_views.py` (updated)
   - `urls.py` (updated)

**Or use Git:**
```bash
# On PythonAnywhere Bash console
cd ~/django-n8n-api
git pull origin main
```

---

### **Step 2: Reload Web App**

1. Go to: **Web** tab
2. Find your app: `abdullah007ie.pythonanywhere.com`
3. Click: **Reload** button (green button)
4. Wait for reload to complete

---

### **Step 3: Test New Endpoints**

Open in browser or use curl:

```bash
# Test today's jobs
https://abdullah007ie.pythonanywhere.com/n8n/get-data/today/

# Test yesterday
https://abdullah007ie.pythonanywhere.com/n8n/get-data/yesterday/

# Test week
https://abdullah007ie.pythonanywhere.com/n8n/get-data/week/

# Test filtering
https://abdullah007ie.pythonanywhere.com/n8n/get-data/?company=BRAC
```

---

## ✅ **Verification**

### **Should See:**
```json
{
  "date": "2025-11-03",
  "count": 242,
  "jobs": [...]
}
```

### **If Error:**
- Check **Error Log** tab on PythonAnywhere
- Verify files uploaded correctly
- Make sure you reloaded the web app

---

## 🎯 **All New Endpoints:**

```
✅ GET /n8n/get-data/                      (with ?days=7 etc)
✅ GET /n8n/get-data/today/
✅ GET /n8n/get-data/yesterday/
✅ GET /n8n/get-data/week/
✅ GET /n8n/get-data/month/
✅ GET /n8n/get-data/date/2025-11-03/
```

---

## 📊 **Usage in n8n:**

### **HTTP Request Node Settings:**

**Get Today's Jobs:**
- Method: `GET`
- URL: `https://abdullah007ie.pythonanywhere.com/n8n/get-data/today/`

**Get Filtered Jobs:**
- Method: `GET`
- URL: `https://abdullah007ie.pythonanywhere.com/n8n/get-data/`
- Query Parameters:
  - `days`: `7`
  - `company`: `BRAC`

---

## 🔧 **Testing Commands:**

### **Using curl:**
```bash
# Today
curl https://abdullah007ie.pythonanywhere.com/n8n/get-data/today/

# Yesterday
curl https://abdullah007ie.pythonanywhere.com/n8n/get-data/yesterday/

# Last 7 days
curl https://abdullah007ie.pythonanywhere.com/n8n/get-data/?days=7

# Company filter
curl "https://abdullah007ie.pythonanywhere.com/n8n/get-data/?company=BRAC"

# Specific date
curl https://abdullah007ie.pythonanywhere.com/n8n/get-data/date/2025-11-03/
```

### **Using Python:**
```python
import requests

# Get today's jobs
r = requests.get('https://abdullah007ie.pythonanywhere.com/n8n/get-data/today/')
data = r.json()
print(f"Today: {data['count']} jobs")

# Get BRAC jobs from last week
r = requests.get('https://abdullah007ie.pythonanywhere.com/n8n/get-data/', 
                params={'company': 'BRAC', 'days': 7})
data = r.json()
print(f"BRAC (7 days): {data['count']} jobs")
```

---

## ⚠️ **Important Notes:**

1. **Timezone:** Server uses UTC or configured timezone
2. **created_at vs scraped_date:**
   - `created_at`: When saved to database
   - `scraped_date`: When scraper found it
3. **Filters are optional:** Can use any combination
4. **Case-insensitive:** Company and position searches ignore case

---

## 🎉 **That's It!**

Your API now supports:
- ✅ Time-based filtering (today, yesterday, week, month)
- ✅ Date range filtering (start/end dates)
- ✅ Last N days filtering
- ✅ Company filtering
- ✅ Position filtering
- ✅ Combined filters

**Upload files → Reload web app → Test!** 🚀

---

## 📞 **Troubleshooting:**

### **500 Internal Server Error:**
- Check Error Log on PythonAnywhere
- Verify imports are correct
- Make sure both files are uploaded

### **404 Not Found:**
- Check URL pattern is correct
- Verify you reloaded web app
- Check urls.py is updated

### **Empty Results:**
- Verify data exists in database
- Check date filters are correct
- Try without filters first

---

**Deployment Time: 2 minutes**  
**Files to Upload: 2**  
**Database Changes: None**  

✅ **Simple upgrade, powerful features!**

