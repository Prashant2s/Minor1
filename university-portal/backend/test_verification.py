"""
Test script to verify certificate verification logic.
Tests the /api/verify endpoint with sample data from database.
"""

import requests
import json

# Test configuration
API_BASE = "http://localhost:3000/api"

def test_verification():
    """Test certificate verification with database records."""
    
    print("=" * 60)
    print("CERTIFICATE VERIFICATION TEST")
    print("=" * 60)
    
    # Test Case 1: Exact match (should verify)
    print("\n[TEST 1] Exact match - should VERIFY")
    test_data_1 = {
        "student_name": "Prashant Singh",
        "enrollment_number": "231B225"
    }
    
    try:
        response = requests.post(
            f"{API_BASE}/verify",
            json=test_data_1,
            headers={'Content-Type': 'application/json'},
            timeout=5
        )
        
        result = response.json()
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(result, indent=2)}")
        
        if result.get('verified'):
            print("✅ PASSED: Certificate verified successfully")
            print(f"   Confidence: {result.get('confidence_score')}")
            matched = result.get('matched_certificate', {})
            print(f"   Matched: {matched.get('student_name')} ({matched.get('enrollment_number')})")
            print(f"   CGPA: {matched.get('cgpa')}")
        else:
            print("❌ FAILED: Certificate should have been verified")
            
    except Exception as e:
        print(f"❌ ERROR: {e}")
    
    # Test Case 2: Case insensitive match
    print("\n[TEST 2] Case insensitive - should VERIFY")
    test_data_2 = {
        "student_name": "prashant singh",
        "enrollment_number": "231b225"
    }
    
    try:
        response = requests.post(
            f"{API_BASE}/verify",
            json=test_data_2,
            headers={'Content-Type': 'application/json'},
            timeout=5
        )
        
        result = response.json()
        print(f"Status Code: {response.status_code}")
        
        if result.get('verified'):
            print("✅ PASSED: Case insensitive match works")
        else:
            print("❌ FAILED: Case insensitive match should work")
            print(f"Response: {json.dumps(result, indent=2)}")
            
    except Exception as e:
        print(f"❌ ERROR: {e}")
    
    # Test Case 3: Wrong enrollment number (should NOT verify)
    print("\n[TEST 3] Wrong enrollment - should NOT VERIFY")
    test_data_3 = {
        "student_name": "Prashant Singh",
        "enrollment_number": "999X999"
    }
    
    try:
        response = requests.post(
            f"{API_BASE}/verify",
            json=test_data_3,
            headers={'Content-Type': 'application/json'},
            timeout=5
        )
        
        result = response.json()
        print(f"Status Code: {response.status_code}")
        
        if not result.get('verified'):
            print("✅ PASSED: Correctly rejected invalid enrollment")
        else:
            print("❌ FAILED: Should not verify wrong enrollment")
            print(f"Response: {json.dumps(result, indent=2)}")
            
    except Exception as e:
        print(f"❌ ERROR: {e}")
    
    # Test Case 4: Check database contents
    print("\n[TEST 4] Database contents")
    try:
        response = requests.get(
            f"{API_BASE}/certificates",
            timeout=5
        )
        
        result = response.json()
        if result.get('success'):
            certs = result.get('certificates', [])
            print(f"✅ Database has {len(certs)} certificate(s)")
            for i, cert in enumerate(certs, 1):
                print(f"   {i}. {cert.get('student_name')} - {cert.get('enrollment_number')} - CGPA: {cert.get('cgpa')}")
        else:
            print("❌ Failed to fetch certificates")
            
    except Exception as e:
        print(f"❌ ERROR: {e}")
    
    print("\n" + "=" * 60)
    print("TEST COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    print("\nMake sure the Flask server is running on http://localhost:3000")
    print("Starting tests in 2 seconds...\n")
    
    import time
    time.sleep(2)
    
    test_verification()
