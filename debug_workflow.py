#!/usr/bin/env python3
"""
Debug and fix the n8n workflow routing issue
"""
import sqlite3
import json

def debug_workflow():
    conn = sqlite3.connect('/Users/sarthak/.n8n/database.sqlite')
    cursor = conn.cursor()
    
    # Get the workflow
    cursor.execute('SELECT id, name, nodes, connections FROM workflow_entity WHERE id = "honk2YIbukF3Nftj"')
    result = cursor.fetchone()
    
    if not result:
        print("❌ Workflow not found")
        return
    
    workflow_id, name, nodes, connections = result
    print(f"📋 Workflow: {name} (ID: {workflow_id})")
    
    # Parse the data
    nodes_data = json.loads(nodes)
    connections_data = json.loads(connections) if connections else {}
    
    print(f"🔗 Total nodes: {len(nodes_data)}")
    print(f"🔗 Connections: {len(connections_data)} root connections")
    
    # Check the routing logic
    print("\n🔍 Analyzing routing logic...")
    
    # Find Message Router connections
    message_router_connections = connections_data.get('Message Router', {})
    print(f"Message Router connections: {message_router_connections}")
    
    # Find FAQ Checker connections  
    faq_checker_connections = connections_data.get('FAQ Checker', {})
    print(f"FAQ Checker connections: {faq_checker_connections}")
    
    # Check if nodes have proper IDs
    node_names = [node.get('name') for node in nodes_data]
    print(f"\n📋 Node names: {node_names}")
    
    # The issue might be in the node IDs vs names in connections
    print("\n🔧 Checking node ID mapping...")
    for node in nodes_data:
        node_id = node.get('id')
        node_name = node.get('name')
        print(f"  {node_name}: {node_id}")
    
    conn.close()

def fix_workflow_routing():
    """Fix the workflow routing by ensuring proper connections"""
    conn = sqlite3.connect('/Users/sarthak/.n8n/database.sqlite')
    cursor = conn.cursor()
    
    # Get current workflow
    cursor.execute('SELECT id, nodes FROM workflow_entity WHERE id = "honk2YIbukF3Nftj"')
    result = cursor.fetchone()
    
    if not result:
        print("❌ Workflow not found")
        return
    
    workflow_id, nodes = result
    nodes_data = json.loads(nodes)
    
    # Create proper connections mapping using actual node IDs
    node_id_map = {}
    for node in nodes_data:
        node_id = node.get('id')
        node_name = node.get('name')
        if node_id and node_name:
            node_id_map[node_name] = node_id
    
    print(f"🗺️  Node ID mapping: {node_id_map}")
    
    # Create the correct connections using node IDs
    corrected_connections = {
        node_id_map.get('WhatsApp Webhook Trigger', 'webhook-trigger'): {
            "main": [
                [
                    {"node": node_id_map.get('Analytics Logger', 'analytics-logger'), "type": "main", "index": 0},
                    {"node": node_id_map.get('Message Router', 'message-router'), "type": "main", "index": 0}
                ]
            ]
        },
        node_id_map.get('Message Router', 'message-router'): {
            "main": [
                [
                    {"node": node_id_map.get('Main Menu Generator', 'main-menu-generator'), "type": "main", "index": 0}
                ],
                [
                    {"node": node_id_map.get('FAQ Checker', 'faq-checker'), "type": "main", "index": 0}
                ]
            ]
        },
        node_id_map.get('FAQ Checker', 'faq-checker'): {
            "main": [
                [
                    {"node": node_id_map.get('FAQ Generator', 'faq-generator'), "type": "main", "index": 0}
                ],
                [
                    {"node": node_id_map.get('Resources Checker', 'resources-checker'), "type": "main", "index": 0}
                ]
            ]
        },
        node_id_map.get('Resources Checker', 'resources-checker'): {
            "main": [
                [
                    {"node": node_id_map.get('Resources Generator', 'resources-generator'), "type": "main", "index": 0}
                ],
                [
                    {"node": node_id_map.get('Updates Checker', 'updates-checker'), "type": "main", "index": 0}
                ]
            ]
        },
        node_id_map.get('Updates Checker', 'updates-checker'): {
            "main": [
                [
                    {"node": node_id_map.get('Updates Generator', 'updates-generator'), "type": "main", "index": 0}
                ],
                [
                    {"node": node_id_map.get('Support Checker', 'support-checker'), "type": "main", "index": 0}
                ]
            ]
        },
        node_id_map.get('Support Checker', 'support-checker'): {
            "main": [
                [
                    {"node": node_id_map.get('Support Generator', 'support-generator'), "type": "main", "index": 0}
                ],
                [
                    {"node": node_id_map.get('Fallback Generator', 'fallback-generator'), "type": "main", "index": 0}
                ]
            ]
        },
        node_id_map.get('Main Menu Generator', 'main-menu-generator'): {
            "main": [
                [
                    {"node": node_id_map.get('Twilio TwiML Generator', 'twilio-response-generator'), "type": "main", "index": 0}
                ]
            ]
        },
        node_id_map.get('FAQ Generator', 'faq-generator'): {
            "main": [
                [
                    {"node": node_id_map.get('Twilio TwiML Generator', 'twilio-response-generator'), "type": "main", "index": 0}
                ]
            ]
        },
        node_id_map.get('Resources Generator', 'resources-generator'): {
            "main": [
                [
                    {"node": node_id_map.get('Twilio TwiML Generator', 'twilio-response-generator'), "type": "main", "index": 0}
                ]
            ]
        },
        node_id_map.get('Updates Generator', 'updates-generator'): {
            "main": [
                [
                    {"node": node_id_map.get('Twilio TwiML Generator', 'twilio-response-generator'), "type": "main", "index": 0}
                ]
            ]
        },
        node_id_map.get('Support Generator', 'support-generator'): {
            "main": [
                [
                    {"node": node_id_map.get('Twilio TwiML Generator', 'twilio-response-generator'), "type": "main", "index": 0}
                ]
            ]
        },
        node_id_map.get('Fallback Generator', 'fallback-generator'): {
            "main": [
                [
                    {"node": node_id_map.get('Twilio TwiML Generator', 'twilio-response-generator'), "type": "main", "index": 0}
                ]
            ]
        },
        node_id_map.get('Twilio TwiML Generator', 'twilio-response-generator'): {
            "main": [
                [
                    {"node": node_id_map.get('Webhook Response', 'webhook-response'), "type": "main", "index": 0}
                ]
            ]
        }
    }
    
    # Update the connections in the database
    connections_json = json.dumps(corrected_connections)
    cursor.execute('UPDATE workflow_entity SET connections = ? WHERE id = ?', (connections_json, workflow_id))
    
    conn.commit()
    conn.close()
    
    print("✅ Workflow connections fixed!")
    return True

if __name__ == "__main__":
    print("🔍 Debugging n8n workflow...")
    debug_workflow()
    
    print("\n🔧 Fixing workflow connections...")
    fix_workflow_routing()
    
    print("\n✅ Workflow debugging and fix complete!")