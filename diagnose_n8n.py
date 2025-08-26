#!/usr/bin/env python3
"""
n8n Workflow Diagnostic and Fix Script
This script tests the n8n workflow and provides detailed diagnostics
"""

import json
import requests
import time
import sys

def test_webhook_response():
    """Test the n8n webhook and analyze the response"""
    
    webhook_url = "https://76cf70ad9d0a.ngrok-free.app/webhook/n8n-whatsapp-webhook"
    
    test_data = {
        "Body": "hi",
        "From": "whatsapp:+917019345031", 
        "To": "whatsapp:+14155238886"
    }
    
    print("🧪 Testing n8n Webhook Response...")
    print(f"URL: {webhook_url}")
    print(f"Data: {test_data}")
    print("-" * 50)
    
    try:
        response = requests.post(
            webhook_url,
            data=test_data,
            headers={
                "Content-Type": "application/x-www-form-urlencoded",
                "ngrok-skip-browser-warning": "true"
            },
            timeout=10
        )
        
        print(f"✅ Status Code: {response.status_code}")
        print(f"📋 Headers: {dict(response.headers)}")
        print(f"📄 Content: {response.text[:500]}...")
        
        # Check if response is TwiML
        if "text/xml" in response.headers.get("content-type", "").lower():
            print("✅ Response is XML (TwiML)")
            if "<Response>" in response.text and "<Message>" in response.text:
                print("✅ Valid TwiML structure detected")
                return True
            else:
                print("❌ Invalid TwiML structure")
                return False
        else:
            print("❌ Response is not XML - workflow may not be active")
            return False
            
    except Exception as e:
        print(f"❌ Error testing webhook: {e}")
        return False

def check_n8n_health():
    """Check if n8n is healthy and accessible"""
    
    n8n_url = "http://localhost:5678"
    
    print("🏥 Checking n8n Health...")
    
    try:
        # Test n8n health endpoint
        health_response = requests.get(f"{n8n_url}/rest/health", timeout=5)
        if health_response.status_code == 200:
            print("✅ n8n is healthy")
        else:
            print(f"❌ n8n health check failed: {health_response.status_code}")
            return False
            
        # Check workflows
        workflows_response = requests.get(f"{n8n_url}/rest/workflows", timeout=10)
        if workflows_response.status_code == 200:
            workflows = workflows_response.json()
            print(f"📋 Found {len(workflows)} workflows")
            
            for wf in workflows:
                status = "🟢 ACTIVE" if wf.get('active') else "🔴 INACTIVE"
                print(f"   - {wf.get('name', 'Unknown')}: {status}")
                
            return True
        else:
            print(f"❌ Failed to get workflows: {workflows_response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to n8n. Is it running on localhost:5678?")
        return False
    except Exception as e:
        print(f"❌ Error checking n8n: {e}")
        return False

def activate_workflow():
    """Try to activate the workflow if it exists"""
    
    n8n_url = "http://localhost:5678"
    
    print("🔄 Attempting to activate workflow...")
    
    try:
        # Get workflows
        workflows_response = requests.get(f"{n8n_url}/rest/workflows", timeout=10)
        workflows = workflows_response.json()
        
        # Find the WhatsApp workflow
        target_workflow = None
        for wf in workflows:
            if "whatsapp" in wf.get('name', '').lower() or "education" in wf.get('name', '').lower():
                target_workflow = wf
                break
                
        if not target_workflow:
            print("❌ No WhatsApp/Education workflow found")
            return False
            
        workflow_id = target_workflow['id']
        workflow_name = target_workflow['name']
        
        if target_workflow.get('active'):
            print(f"✅ Workflow '{workflow_name}' is already active")
            return True
            
        # Activate the workflow
        activate_response = requests.patch(
            f"{n8n_url}/rest/workflows/{workflow_id}",
            json={"active": True},
            timeout=10
        )
        
        if activate_response.status_code == 200:
            print(f"✅ Successfully activated workflow '{workflow_name}'")
            return True
        else:
            print(f"❌ Failed to activate workflow: {activate_response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error activating workflow: {e}")
        return False

def create_simple_test_workflow():
    """Create a simple test workflow if none exists"""
    
    n8n_url = "http://localhost:5678"
    
    simple_workflow = {
        "name": "Simple WhatsApp Test",
        "nodes": [
            {
                "parameters": {
                    "httpMethod": "POST",
                    "path": "test-webhook",
                    "responseMode": "responseNode"
                },
                "id": "webhook-test",
                "name": "Webhook Test",
                "type": "n8n-nodes-base.webhook",
                "typeVersion": 1,
                "position": [240, 300]
            },
            {
                "parameters": {
                    "respondWith": "text",
                    "responseBody": "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<Response>\n  <Message>Hello from n8n Test!</Message>\n</Response>",
                    "options": {
                        "responseHeaders": {
                            "entries": [
                                {
                                    "name": "Content-Type",
                                    "value": "text/xml"
                                }
                            ]
                        }
                    }
                },
                "id": "respond-test",
                "name": "Respond Test",
                "type": "n8n-nodes-base.respondToWebhook",
                "typeVersion": 1,
                "position": [460, 300]
            }
        ],
        "connections": {
            "webhook-test": {
                "main": [
                    [
                        {
                            "node": "respond-test",
                            "type": "main",
                            "index": 0
                        }
                    ]
                ]
            }
        },
        "active": True
    }
    
    print("🛠️ Creating simple test workflow...")
    
    try:
        create_response = requests.post(
            f"{n8n_url}/rest/workflows",
            json=simple_workflow,
            timeout=15
        )
        
        if create_response.status_code == 201:
            print("✅ Test workflow created successfully")
            return True
        else:
            print(f"❌ Failed to create test workflow: {create_response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error creating test workflow: {e}")
        return False

def main():
    """Main diagnostic and fix function"""
    
    print("🔧 n8n Workflow Diagnostic Tool")
    print("=" * 50)
    
    # Step 1: Check n8n health
    if not check_n8n_health():
        print("\n❌ n8n is not healthy. Please check if it's running.")
        sys.exit(1)
    
    print()
    
    # Step 2: Test current webhook
    webhook_working = test_webhook_response()
    
    print()
    
    if not webhook_working:
        print("🔄 Webhook not working properly. Attempting fixes...")
        
        # Step 3: Try to activate existing workflow
        if activate_workflow():
            print("\n🧪 Testing webhook again after activation...")
            time.sleep(2)
            webhook_working = test_webhook_response()
        
        # Step 4: If still not working, create simple test workflow
        if not webhook_working:
            print("\n🛠️ Creating simple test workflow...")
            if create_simple_test_workflow():
                print("\n✅ Test workflow created. Try this URL:")
                print("https://76cf70ad9d0a.ngrok-free.app/webhook/test-webhook")
    
    print("\n" + "=" * 50)
    if webhook_working:
        print("✅ Webhook is working correctly!")
        print("🎯 Your Twilio webhook URL: https://76cf70ad9d0a.ngrok-free.app/webhook/n8n-whatsapp-webhook")
    else:
        print("❌ Webhook still not working. Manual intervention needed:")
        print("1. Go to http://localhost:5678")
        print("2. Check if workflow is imported and ACTIVE")
        print("3. Verify webhook path matches: n8n-whatsapp-webhook")
        print("4. Ensure TwiML response is properly configured")

if __name__ == "__main__":
    main()