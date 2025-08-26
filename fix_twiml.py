#!/usr/bin/env python3
"""
Fix TwiML XML formatting for Twilio compatibility
"""
import sqlite3
import json

def fix_twiml_formatting():
    # Connect to database
    conn = sqlite3.connect('/Users/sarthak/.n8n/database.sqlite')
    cursor = conn.cursor()
    
    # Get current workflow
    cursor.execute("SELECT nodes FROM workflow_entity WHERE id = 'honk2YIbukF3Nftj'")
    result = cursor.fetchone()
    
    if not result:
        print("❌ Workflow not found")
        return
    
    nodes = json.loads(result[0])
    
    # Find and fix the TwiML Generator node
    for node in nodes:
        if node.get('name') == 'Twilio TwiML Generator':
            print("🔧 Fixing TwiML Generator...")
            # Update the JavaScript code to escape XML properly
            node['parameters']['jsCode'] = '''// Twilio TwiML Response Generator
const message = $json.message || 'Hello from Student Support Bot!';

// Escape XML characters properly
function escapeXml(unsafe) {
    return unsafe.replace(/[<>&'"]/g, function (c) {
        switch (c) {
            case '<': return '&lt;';
            case '>': return '&gt;';
            case '&': return '&amp;';
            case '\\'': return '&apos;';
            case '"': return '&quot;';
        }
    });
}

// Generate clean TwiML response
const cleanMessage = escapeXml(message);
const twimlResponse = `<?xml version="1.0" encoding="UTF-8"?>
<Response>
<Message>${cleanMessage}</Message>
</Response>`;

return [{
  json: {
    twimlResponse,
    message: cleanMessage,
    contentType: 'text/xml',
    timestamp: new Date().toISOString()
  }
}];'''
        
        # Find and fix the Webhook Response node
        elif node.get('name') == 'Webhook Response':
            print("🔧 Fixing Webhook Response...")
            node['parameters'] = {
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
    
    # Update the workflow in database
    updated_nodes = json.dumps(nodes)
    cursor.execute(
        "UPDATE workflow_entity SET nodes = ? WHERE id = 'honk2YIbukF3Nftj'",
        (updated_nodes,)
    )
    
    conn.commit()
    conn.close()
    
    print("✅ TwiML formatting fixed!")
    print("🔄 Restart n8n to apply changes")

if __name__ == "__main__":
    fix_twiml_formatting()