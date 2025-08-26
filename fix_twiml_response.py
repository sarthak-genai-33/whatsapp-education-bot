#!/usr/bin/env python3
"""
Fix the TwiML generator and webhook response in the n8n workflow
"""
import sqlite3
import json

def fix_twiml_and_response():
    conn = sqlite3.connect('/Users/sarthak/.n8n/database.sqlite')
    cursor = conn.cursor()
    
    # Get the current workflow
    cursor.execute('SELECT nodes FROM workflow_entity WHERE id = "honk2YIbukF3Nftj"')
    result = cursor.fetchone()
    
    if not result:
        print("❌ Workflow not found")
        return
    
    nodes_data = json.loads(result[0])
    
    # Fix the TwiML Generator node
    for i, node in enumerate(nodes_data):
        if node.get('name') == 'Twilio TwiML Generator':
            print("🔧 Fixing TwiML Generator node...")
            
            # Updated JavaScript code for TwiML generation
            updated_code = '''// Twilio TwiML Response Generator
const message = $json.message || 'Hello from Student Support Bot!';

// Escape XML characters properly
function escapeXml(unsafe) {
    if (typeof unsafe !== 'string') {
        unsafe = String(unsafe);
    }
    return unsafe.replace(/[<>&'"]/g, function (c) {
        switch (c) {
            case '<': return '&lt;';
            case '>': return '&gt;';
            case '&': return '&amp;';
            case '\\'': return '&apos;';
            case '"': return '&quot;';
            default: return c;
        }
    });
}

// Generate clean TwiML response
const escapedMessage = escapeXml(message);
const twimlResponse = `<?xml version="1.0" encoding="UTF-8"?>
<Response>
<Message>${escapedMessage}</Message>
</Response>`;

return [{
  json: {
    twimlResponse,
    message: escapedMessage,
    contentType: 'text/xml; charset=utf-8',
    timestamp: new Date().toISOString()
  }
}];'''
            
            nodes_data[i]['parameters']['jsCode'] = updated_code
            print("   ✅ TwiML Generator code updated")
            break
    
    # Fix the Webhook Response node
    for i, node in enumerate(nodes_data):
        if node.get('name') == 'Webhook Response':
            print("🔧 Fixing Webhook Response node...")
            
            # Update webhook response configuration
            nodes_data[i]['parameters'] = {
                "respondWith": "text",
                "responseBody": "={{ $json.twimlResponse }}",
                "options": {
                    "responseHeaders": {
                        "entries": [
                            {
                                "name": "Content-Type",
                                "value": "text/xml; charset=utf-8"
                            }
                        ]
                    }
                }
            }
            print("   ✅ Webhook Response configuration updated")
            break
    
    # Update the workflow in the database
    updated_nodes = json.dumps(nodes_data)
    cursor.execute('UPDATE workflow_entity SET nodes = ? WHERE id = ?', (updated_nodes, 'honk2YIbukF3Nftj'))
    
    conn.commit()
    conn.close()
    
    print("✅ TwiML generator and webhook response fixed!")
    return True

if __name__ == "__main__":
    print("🔧 Fixing TwiML generator and webhook response...")
    if fix_twiml_and_response():
        print("🎉 Fix complete! Restart n8n to apply changes.")
    else:
        print("❌ Fix failed!")