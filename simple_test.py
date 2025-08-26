#!/usr/bin/env python3
"""
Simple test to validate the workflow fix
"""
import requests
import time

def test_workflow():
    print("🧪 Testing fixed n8n workflow...")
    
    # Test data
    test_cases = [
        ("hi", "Welcome to Student Support Bot"),
        ("fees", "Fee Structure"),
        ("courses", "Available Courses"),
        ("help", "Student Support Contact"),
        ("unknown", "didn't quite understand")
    ]
    
    base_url = "http://localhost:5678/webhook/n8n-whatsapp-webhook"
    
    for message, expected in test_cases:
        print(f"\n🔍 Testing: '{message}'")
        
        data = {
            "Body": message,
            "From": "whatsapp:+917019345031",
            "To": "whatsapp:+14155238886"
        }
        
        try:
            response = requests.post(base_url, data=data, timeout=10)
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 200:
                content = response.text[:200]
                print(f"   Response: {content}...")
                
                if expected.lower() in content.lower():
                    print("   ✅ PASS: Expected content found")
                else:
                    print("   ❌ FAIL: Expected content not found")
            else:
                print(f"   ❌ FAIL: HTTP {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            print(f"   ❌ ERROR: {e}")
    
    print("\n🎯 Test complete!")

if __name__ == "__main__":
    test_workflow()