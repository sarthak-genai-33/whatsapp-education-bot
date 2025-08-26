#!/usr/bin/env python3
"""
Fix n8n workflow connections in database
"""
import sqlite3
import json

def fix_workflow_connections():
    # Correct connections for the workflow
    connections = {
        "WhatsApp Webhook Trigger": {
            "main": [
                [
                    {"node": "Analytics Logger", "type": "main", "index": 0},
                    {"node": "Message Router", "type": "main", "index": 0}
                ]
            ]
        },
        "Message Router": {
            "main": [
                [{"node": "Main Menu Generator", "type": "main", "index": 0}],
                [{"node": "FAQ Checker", "type": "main", "index": 0}]
            ]
        },
        "FAQ Checker": {
            "main": [
                [{"node": "FAQ Generator", "type": "main", "index": 0}],
                [{"node": "Resources Checker", "type": "main", "index": 0}]
            ]
        },
        "Resources Checker": {
            "main": [
                [{"node": "Resources Generator", "type": "main", "index": 0}],
                [{"node": "Updates Checker", "type": "main", "index": 0}]
            ]
        },
        "Updates Checker": {
            "main": [
                [{"node": "Updates Generator", "type": "main", "index": 0}],
                [{"node": "Support Checker", "type": "main", "index": 0}]
            ]
        },
        "Support Checker": {
            "main": [
                [{"node": "Support Generator", "type": "main", "index": 0}],
                [{"node": "Fallback Generator", "type": "main", "index": 0}]
            ]
        },
        "Main Menu Generator": {
            "main": [
                [{"node": "Twilio TwiML Generator", "type": "main", "index": 0}]
            ]
        },
        "FAQ Generator": {
            "main": [
                [{"node": "Twilio TwiML Generator", "type": "main", "index": 0}]
            ]
        },
        "Resources Generator": {
            "main": [
                [{"node": "Twilio TwiML Generator", "type": "main", "index": 0}]
            ]
        },
        "Updates Generator": {
            "main": [
                [{"node": "Twilio TwiML Generator", "type": "main", "index": 0}]
            ]
        },
        "Support Generator": {
            "main": [
                [{"node": "Twilio TwiML Generator", "type": "main", "index": 0}]
            ]
        },
        "Fallback Generator": {
            "main": [
                [{"node": "Twilio TwiML Generator", "type": "main", "index": 0}]
            ]
        },
        "Twilio TwiML Generator": {
            "main": [
                [{"node": "Webhook Response", "type": "main", "index": 0}]
            ]
        }
    }
    
    # Connect to database
    conn = sqlite3.connect('/Users/sarthak/.n8n/database.sqlite')
    cursor = conn.cursor()
    
    # Update connections
    connections_json = json.dumps(connections)
    cursor.execute(
        "UPDATE workflow_entity SET connections = ? WHERE id = 'honk2YIbukF3Nftj'",
        (connections_json,)
    )
    
    conn.commit()
    conn.close()
    
    print("✅ Workflow connections fixed!")
    print("🔄 Restart n8n to apply changes")

if __name__ == "__main__":
    fix_workflow_connections()