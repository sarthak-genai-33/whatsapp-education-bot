#!/bin/bash
echo "🧪 Testing fixed n8n workflow..."

# Test data
declare -a tests=(
    "hi|Welcome to Student Support Bot"
    "fees|Fee Structure"  
    "courses|Available Courses"
    "help|Student Support Contact"
    "unknown|didn't quite understand"
)

for test in "${tests[@]}"; do
    IFS='|' read -r message expected <<< "$test"
    echo ""
    echo "🔍 Testing: '$message'"
    
    response=$(curl -s -X POST "http://localhost:5678/webhook/n8n-whatsapp-webhook" \
        -H "Content-Type: application/x-www-form-urlencoded" \
        -d "Body=$message&From=whatsapp:+917019345031&To=whatsapp:+14155238886")
    
    if [[ -n "$response" ]]; then
        echo "   Response length: ${#response} chars"
        echo "   First 100 chars: ${response:0:100}..."
        
        if [[ "$response" == *"$expected"* ]]; then
            echo "   ✅ PASS: Expected content found"
        else
            echo "   ❌ FAIL: Expected content not found"
        fi
    else
        echo "   ❌ FAIL: Empty response"
    fi
done

echo ""
echo "🎯 Test complete!"