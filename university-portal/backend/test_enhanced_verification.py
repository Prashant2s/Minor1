"""
Enhanced test for certificate verification with CGPA/SGPA comparison.
Tests field-by-field comparison and mismatch detection.
"""

import requests
import json

API_BASE = "http://localhost:3000/api"

def print_result(test_name, result):
    """Pretty print verification result."""
    print(f"\n{'='*60}")
    print(f"{test_name}")
    print(f"{'='*60}")
    print(f"Verified: {result.get('verified')}")
    print(f"Status: {result.get('status', 'N/A')}")
    print(f"Confidence: {result.get('confidence_score')}")
    
    if result.get('field_comparisons'):
        print(f"\nField Comparisons:")
        for comp in result['field_comparisons']:
            match_symbol = "✅" if comp['match'] else "❌" if comp['match'] is False else "⚠️"
            print(f"  {match_symbol} {comp['field']}: {comp['extracted']} vs {comp['database']}")
    
    if result.get('mismatches'):
        print(f"\n❌ Mismatches Found:")
        for mm in result['mismatches']:
            print(f"  - {mm['field']}: {mm['extracted']} ≠ {mm['database']}")
    
    print()


def test_enhanced_verification():
    """Run enhanced verification tests."""
    
    print("\n" + "="*60)
    print("ENHANCED CERTIFICATE VERIFICATION TEST")
    print("="*60)
    
    # Test 1: Perfect match with CGPA and SGPA
    print("\n[TEST 1] Perfect match with CGPA and SGPA")
    test_data = {
        "student_name": "Prashant Singh",
        "enrollment_number": "231B225",
        "cgpa": "6.1",
        "sgpa": "6.1"
    }
    
    try:
        response = requests.post(f"{API_BASE}/verify", json=test_data, timeout=5)
        result = response.json()
        print_result("Perfect Match Test", result)
        
        if result.get('verified') and result.get('status') == 'VERIFIED':
            print("✅ PASSED: Perfect match verified")
        else:
            print("❌ FAILED: Should verify with perfect match")
    except Exception as e:
        print(f"❌ ERROR: {e}")
    
    # Test 2: CGPA mismatch
    print("\n[TEST 2] CGPA Mismatch - tampering detection")
    test_data = {
        "student_name": "Prashant Singh",
        "enrollment_number": "231B225",
        "cgpa": "9.5",  # Tampered value
        "sgpa": "6.1"
    }
    
    try:
        response = requests.post(f"{API_BASE}/verify", json=test_data, timeout=5)
        result = response.json()
        print_result("CGPA Mismatch Test", result)
        
        if not result.get('verified') and result.get('status') == 'MISMATCH':
            print("✅ PASSED: CGPA mismatch detected correctly")
        else:
            print("❌ FAILED: Should detect CGPA mismatch")
    except Exception as e:
        print(f"❌ ERROR: {e}")
    
    # Test 3: SGPA mismatch
    print("\n[TEST 3] SGPA Mismatch")
    test_data = {
        "student_name": "Prashant Singh",
        "enrollment_number": "231B225",
        "cgpa": "6.1",
        "sgpa": "8.5"  # Wrong SGPA
    }
    
    try:
        response = requests.post(f"{API_BASE}/verify", json=test_data, timeout=5)
        result = response.json()
        print_result("SGPA Mismatch Test", result)
        
        if not result.get('verified') and result.get('status') == 'MISMATCH':
            print("✅ PASSED: SGPA mismatch detected correctly")
        else:
            print("❌ FAILED: Should detect SGPA mismatch")
    except Exception as e:
        print(f"❌ ERROR: {e}")
    
    # Test 4: Rounding tolerance (6.10 vs 6.1)
    print("\n[TEST 4] Rounding tolerance test")
    test_data = {
        "student_name": "Prashant Singh",
        "enrollment_number": "231B225",
        "cgpa": "6.10",  # Should match 6.1
        "sgpa": "6.05"   # Should match 6.1 within tolerance
    }
    
    try:
        response = requests.post(f"{API_BASE}/verify", json=test_data, timeout=5)
        result = response.json()
        print_result("Rounding Tolerance Test", result)
        
        if result.get('verified'):
            print("✅ PASSED: Rounding tolerance works")
        else:
            print("⚠️  Note: Check if 0.1 tolerance is acceptable")
    except Exception as e:
        print(f"❌ ERROR: {e}")
    
    # Test 5: Without CGPA/SGPA (should still verify name and enrollment)
    print("\n[TEST 5] Verification without CGPA/SGPA")
    test_data = {
        "student_name": "Prashant Singh",
        "enrollment_number": "231B225"
    }
    
    try:
        response = requests.post(f"{API_BASE}/verify", json=test_data, timeout=5)
        result = response.json()
        print_result("Basic Verification Test", result)
        
        if result.get('verified'):
            print("✅ PASSED: Basic verification without grades works")
        else:
            print("❌ FAILED: Should verify name and enrollment")
    except Exception as e:
        print(f"❌ ERROR: {e}")
    
    print("\n" + "="*60)
    print("TEST COMPLETE")
    print("="*60)


if __name__ == "__main__":
    print("\nEnsure Flask server is running on http://localhost:3000")
    print("Starting tests in 2 seconds...\n")
    
    import time
    time.sleep(2)
    
    test_enhanced_verification()
