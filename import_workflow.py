#!/usr/bin/env python3
"""
Quick script to import n8n workflow via API
"""
import json
import requests
import sys

def import_workflow():
    # Read the workflow JSON
    with open('n8n-workflow.json', 'r') as f:
        workflow_data = json.load(f)
    
    # Import via n8n API
    url = 'http://localhost:5678/rest/workflows'
    headers = {'Content-Type': 'application/json'}
    
    try:
        response = requests.post(url, json=workflow_data, headers=headers)
        if response.status_code == 200 or response.status_code == 201:
            print("✅ Workflow imported successfully!")
            result = response.json()
            print(f"Workflow ID: {result.get('id')}")
            print(f"Workflow Name: {result.get('name')}")
            return True
        else:
            print(f"❌ Import failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error importing workflow: {e}")
        return False

if __name__ == "__main__":
    if import_workflow():
        print("🎉 Workflow is ready!")
    else:
        print("💥 Import failed!")
        sys.exit(1)