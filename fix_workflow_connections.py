#!/usr/bin/env python3
"""
Fix n8n Workflow Connections
This script reimports the corrected workflow to fix broken connections
"""

import json
import requests
import sys

def reimport_workflow():
    """Reimport the corrected workflow to n8n"""
    
    # n8n API endpoint (assuming running on localhost:5678)
    n8n_url = "http://localhost:5678"
    
    try:
        # Load the corrected workflow
        with open('n8n-workflow.json', 'r') as f:
            workflow_data = json.load(f)
        
        print("✅ Loaded corrected workflow file")
        
        # Check if n8n is accessible
        try:
            health_response = requests.get(f"{n8n_url}/rest/health", timeout=5)
            if health_response.status_code == 200:
                print("✅ n8n is accessible")
            else:
                print(f"❌ n8n health check failed: {health_response.status_code}")
                return False
        except requests.exceptions.ConnectionError:
            print("❌ Cannot connect to n8n. Make sure it's running on localhost:5678")
            return False
        
        # Check current workflows
        try:
            workflows_response = requests.get(f"{n8n_url}/rest/workflows", timeout=10)
            if workflows_response.status_code == 200:
                workflows = workflows_response.json()
                print(f"✅ Found {len(workflows)} existing workflows")
                
                # Find existing workflow by name
                existing_workflow = None
                for wf in workflows:
                    if wf.get('name') == workflow_data.get('name'):
                        existing_workflow = wf
                        break
                
                if existing_workflow:
                    print(f"📝 Found existing workflow: {existing_workflow['name']} (ID: {existing_workflow['id']})")
                    
                    # Update existing workflow
                    update_payload = {
                        **workflow_data,
                        'id': existing_workflow['id']
                    }
                    
                    update_response = requests.put(
                        f"{n8n_url}/rest/workflows/{existing_workflow['id']}", 
                        json=update_payload,
                        timeout=30
                    )
                    
                    if update_response.status_code == 200:
                        print("✅ Successfully updated workflow with fixed connections!")
                        return True
                    else:
                        print(f"❌ Failed to update workflow: {update_response.status_code}")
                        print(f"Response: {update_response.text}")
                        return False
                else:
                    print("📝 No existing workflow found, creating new one...")
                    
                    # Create new workflow
                    create_response = requests.post(
                        f"{n8n_url}/rest/workflows", 
                        json=workflow_data,
                        timeout=30
                    )
                    
                    if create_response.status_code == 201:
                        print("✅ Successfully created new workflow with fixed connections!")
                        return True
                    else:
                        print(f"❌ Failed to create workflow: {create_response.status_code}")
                        print(f"Response: {create_response.text}")
                        return False
            else:
                print(f"❌ Failed to get workflows: {workflows_response.status_code}")
                return False
                
        except requests.exceptions.RequestException as e:
            print(f"❌ API request failed: {e}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Main function"""
    print("🔧 Fixing n8n Workflow Connections...")
    print("=" * 50)
    
    if reimport_workflow():
        print("\n✅ Workflow connections fixed successfully!")
        print("\n📋 Next steps:")
        print("1. Go to n8n editor: http://localhost:5678")
        print("2. Verify the workflow is properly connected")
        print("3. Ensure the workflow is ACTIVATED (toggle the Active switch)")
        print("4. Test with Twilio webhook URL: https://76cf70ad9d0a.ngrok-free.app/webhook/n8n-whatsapp-webhook")
    else:
        print("\n❌ Failed to fix workflow connections")
        print("💡 Manual steps:")
        print("1. Open n8n editor: http://localhost:5678")
        print("2. Import the n8n-workflow.json file manually")
        print("3. Connect Main Menu Generator → Twilio TwiML Generator")
        print("4. Activate the workflow")
        sys.exit(1)

if __name__ == "__main__":
    main()