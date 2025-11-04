"""
Test script for BD Government Jobs API
Run this after setting up the bdgovjob app to verify it works correctly.

Usage:
    python test_bdgovjob_api.py
"""

import requests
import json
from datetime import datetime

# API Base URL (change if needed)
API_BASE = "http://localhost:8000/bdgovjob"

# Colors for terminal output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'

def print_success(msg):
    print(f"{Colors.GREEN}✅ {msg}{Colors.END}")

def print_error(msg):
    print(f"{Colors.RED}❌ {msg}{Colors.END}")

def print_info(msg):
    print(f"{Colors.BLUE}ℹ  {msg}{Colors.END}")

def print_warning(msg):
    print(f"{Colors.YELLOW}⚠  {msg}{Colors.END}")

def test_stats_endpoint():
    """Test the /stats/ endpoint"""
    print_info("Testing stats endpoint...")
    
    try:
        response = requests.get(f"{API_BASE}/stats/")
        if response.status_code == 200:
            data = response.json()
            print_success(f"Stats endpoint working! Total jobs: {data['total_jobs']}")
            return True
        else:
            print_error(f"Stats endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Stats endpoint error: {e}")
        return False

def test_send_data():
    """Test sending data to the API"""
    print_info("Testing send data endpoint...")
    
    test_job = {
        "job_title": "Test Government Job Circular 2025",
        "job_url": f"https://test.bdgovtjob.net/test-job-{datetime.now().timestamp()}/",
        "vacancies": "100",
        "deadline": "31 December 2025",
        "posted_date": "3 November, 2025",
        "scraped_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    try:
        response = requests.post(
            f"{API_BASE}/send-data/",
            json=test_job,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code in [200, 201]:
            data = response.json()
            print_success(f"Data sent successfully! Created: {data['total_created']}, Updated: {data['total_updated']}")
            return True
        else:
            print_error(f"Send data failed: {response.status_code}")
            print(response.text)
            return False
    except Exception as e:
        print_error(f"Send data error: {e}")
        return False

def test_bulk_send():
    """Test sending multiple jobs at once"""
    print_info("Testing bulk send...")
    
    test_jobs = [
        {
            "job_title": f"Bulk Test Job {i}",
            "job_url": f"https://test.bdgovtjob.net/bulk-job-{datetime.now().timestamp()}-{i}/",
            "vacancies": str(10 * i),
            "deadline": "31 December 2025",
            "posted_date": "3 November, 2025",
            "scraped_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        for i in range(1, 6)
    ]
    
    try:
        response = requests.post(
            f"{API_BASE}/send-data/",
            json=test_jobs,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code in [200, 201]:
            data = response.json()
            print_success(f"Bulk send successful! Created: {data['total_created']}, Updated: {data['total_updated']}")
            return True
        else:
            print_error(f"Bulk send failed: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Bulk send error: {e}")
        return False

def test_get_data():
    """Test retrieving data"""
    print_info("Testing get data endpoint...")
    
    try:
        response = requests.get(f"{API_BASE}/get-data/")
        if response.status_code == 200:
            data = response.json()
            print_success(f"Get data working! Found {data['count']} jobs")
            return True
        else:
            print_error(f"Get data failed: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Get data error: {e}")
        return False

def test_get_today():
    """Test getting today's data"""
    print_info("Testing today's data endpoint...")
    
    try:
        response = requests.get(f"{API_BASE}/get-data/today/")
        if response.status_code == 200:
            data = response.json()
            print_success(f"Today's data working! Found {data['count']} jobs for {data['date']}")
            return True
        else:
            print_error(f"Today's data failed: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Today's data error: {e}")
        return False

def test_filters():
    """Test filtering"""
    print_info("Testing filters...")
    
    try:
        # Test title filter
        response = requests.get(f"{API_BASE}/get-data/?title=Test")
        if response.status_code == 200:
            data = response.json()
            print_success(f"Title filter working! Found {data['count']} jobs with 'Test' in title")
            return True
        else:
            print_error(f"Filter test failed: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Filter test error: {e}")
        return False

def test_update_existing():
    """Test updating an existing job"""
    print_info("Testing update of existing job...")
    
    job_url = f"https://test.bdgovtjob.net/update-test-{datetime.now().timestamp()}/"
    
    # First, create a job
    original_job = {
        "job_title": "Original Title",
        "job_url": job_url,
        "vacancies": "50",
        "deadline": "31 December 2025",
        "posted_date": "3 November, 2025",
        "scraped_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    try:
        response1 = requests.post(f"{API_BASE}/send-data/", json=original_job)
        if response1.status_code not in [200, 201]:
            print_error("Failed to create original job")
            return False
        
        # Now update it
        updated_job = {
            "job_title": "Updated Title",
            "job_url": job_url,  # Same URL
            "vacancies": "100",  # Changed
            "deadline": "31 December 2025",
            "posted_date": "3 November, 2025",
            "scraped_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        response2 = requests.post(f"{API_BASE}/send-data/", json=updated_job)
        if response2.status_code in [200, 201]:
            data = response2.json()
            if data['total_updated'] > 0:
                print_success(f"Update working! Updated: {data['total_updated']}")
                return True
            else:
                print_warning("Expected update but got creation instead")
                return False
        else:
            print_error(f"Update failed: {response2.status_code}")
            return False
    except Exception as e:
        print_error(f"Update test error: {e}")
        return False

def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("🧪 BD Government Jobs API Test Suite")
    print("="*60 + "\n")
    
    tests = [
        ("Stats Endpoint", test_stats_endpoint),
        ("Send Data (Single)", test_send_data),
        ("Send Data (Bulk)", test_bulk_send),
        ("Get Data", test_get_data),
        ("Get Today's Data", test_get_today),
        ("Filters", test_filters),
        ("Update Existing Job", test_update_existing),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n{'─'*60}")
        print(f"Test: {test_name}")
        print('─'*60)
        
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print_error(f"Test crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "="*60)
    print("📊 Test Results Summary")
    print("="*60 + "\n")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    print(f"\n{'─'*60}")
    print(f"Total: {passed}/{total} tests passed")
    print('─'*60)
    
    if passed == total:
        print_success("\n🎉 All tests passed! API is working perfectly!")
    elif passed > 0:
        print_warning(f"\n⚠ {total - passed} tests failed. Check the output above.")
    else:
        print_error("\n❌ All tests failed. Is the server running?")
        print_info("Start the server with: python manage.py runserver")
    
    print()

if __name__ == "__main__":
    main()

