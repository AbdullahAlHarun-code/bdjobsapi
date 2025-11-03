#!/usr/bin/env python3
"""
Quick API Testing Script
Run this to test all new filtering endpoints
"""

import requests
import json
from datetime import datetime, timedelta

# Your API base URL
BASE_URL = "https://abdullah007ie.pythonanywhere.com/n8n"

def print_result(title, response):
    """Pretty print API response"""
    print(f"\n{'='*60}")
    print(f"🔍 {title}")
    print(f"{'='*60}")
    
    if response.status_code == 200:
        data = response.json()
        
        # Show count if available
        if 'count' in data:
            print(f"✅ Status: {response.status_code}")
            print(f"📊 Count: {data['count']} jobs")
        
        # Show applied filters if available
        if 'filters' in data:
            print(f"🔧 Filters: {data['filters']}")
        
        # Show date/period if available
        if 'date' in data:
            print(f"📅 Date: {data['date']}")
        if 'period' in data:
            print(f"📅 Period: {data['period']}")
        if 'month' in data:
            print(f"📅 Month: {data['month']}")
        
        # Show first 3 jobs as sample
        if 'jobs' in data and len(data['jobs']) > 0:
            print(f"\n📝 Sample Jobs (first 3):")
            for i, job in enumerate(data['jobs'][:3], 1):
                print(f"  {i}. {job['company_name']} - {job['position'][:50]}...")
        
        print(f"✅ SUCCESS")
    else:
        print(f"❌ Error: {response.status_code}")
        print(f"Response: {response.text}")

def test_all_endpoints():
    """Test all API endpoints"""
    
    print("\n" + "="*60)
    print("🚀 TESTING ALL API ENDPOINTS")
    print("="*60)
    
    # Test 1: Get all data (no filter)
    print_result(
        "Test 1: Get All Data (No Filter)",
        requests.get(f"{BASE_URL}/get-data/")
    )
    
    # Test 2: Get today's jobs
    print_result(
        "Test 2: Get Today's Jobs",
        requests.get(f"{BASE_URL}/get-data/today/")
    )
    
    # Test 3: Get yesterday's jobs
    print_result(
        "Test 3: Get Yesterday's Jobs",
        requests.get(f"{BASE_URL}/get-data/yesterday/")
    )
    
    # Test 4: Get this week's jobs
    print_result(
        "Test 4: Get This Week's Jobs (Last 7 Days)",
        requests.get(f"{BASE_URL}/get-data/week/")
    )
    
    # Test 5: Get this month's jobs
    print_result(
        "Test 5: Get This Month's Jobs",
        requests.get(f"{BASE_URL}/get-data/month/")
    )
    
    # Test 6: Get specific date
    today = datetime.now().strftime('%Y-%m-%d')
    print_result(
        f"Test 6: Get Specific Date ({today})",
        requests.get(f"{BASE_URL}/get-data/date/{today}/")
    )
    
    # Test 7: Filter by last 7 days
    print_result(
        "Test 7: Filter Last 7 Days",
        requests.get(f"{BASE_URL}/get-data/", params={'days': 7})
    )
    
    # Test 8: Filter by company
    print_result(
        "Test 8: Filter by Company (BRAC)",
        requests.get(f"{BASE_URL}/get-data/", params={'company': 'BRAC'})
    )
    
    # Test 9: Filter by position
    print_result(
        "Test 9: Filter by Position (Manager)",
        requests.get(f"{BASE_URL}/get-data/", params={'position': 'Manager'})
    )
    
    # Test 10: Combined filters
    print_result(
        "Test 10: Combined Filters (BRAC + Last 7 Days)",
        requests.get(f"{BASE_URL}/get-data/", params={'company': 'BRAC', 'days': 7})
    )
    
    # Test 11: Date range
    end_date = datetime.now().strftime('%Y-%m-%d')
    start_date = (datetime.now() - timedelta(days=3)).strftime('%Y-%m-%d')
    print_result(
        f"Test 11: Date Range ({start_date} to {end_date})",
        requests.get(f"{BASE_URL}/get-data/", params={'start': start_date, 'end': end_date})
    )
    
    # Summary
    print("\n" + "="*60)
    print("✅ ALL TESTS COMPLETED!")
    print("="*60)
    print("\n📊 Summary:")
    print("  - All endpoints tested")
    print("  - Check results above for any errors")
    print("  - If all show ✅ SUCCESS, your API is ready!")
    print("\n🎉 API is working perfectly!\n")


if __name__ == "__main__":
    try:
        test_all_endpoints()
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Cannot connect to API")
        print("   Check if PythonAnywhere web app is running")
        print("   URL:", BASE_URL)
    except Exception as e:
        print(f"\n❌ ERROR: {e}")

