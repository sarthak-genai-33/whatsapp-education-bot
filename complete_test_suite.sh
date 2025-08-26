#!/bin/bash

# Comprehensive End-to-End Test Suite for WhatsApp Education Bot
# Tests both n8n and Flask implementations

echo "🚀 WhatsApp Education Bot - Complete Test Suite"
echo "================================================"
echo "Testing Date: $(date)"
echo ""

# Configuration
N8N_URL="https://06945024e292.ngrok-free.app/webhook/n8n-whatsapp-webhook"
FLASK_URL="http://localhost:5001/whatsapp"
TEST_PHONE_FROM="whatsapp:+1234567890"
TEST_PHONE_TO="whatsapp:+0987654321"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Test function
run_test() {
    local url=$1
    local message=$2
    local test_name=$3
    local expected_content=$4
    
    echo -e "${BLUE}🧪 Testing: $test_name${NC}"
    echo "   Message: '$message'"
    echo "   URL: $url"
    
    response=$(curl -s -w "HTTP_CODE:%{http_code}" -X POST "$url" \
        -H "Content-Type: application/x-www-form-urlencoded" \
        -d "Body=$message&From=$TEST_PHONE_FROM&To=$TEST_PHONE_TO")
    
    http_code=$(echo "$response" | sed -n 's/.*HTTP_CODE:\([0-9]*\)$/\1/p')
    body=$(echo "$response" | sed 's/HTTP_CODE:[0-9]*$//')
    
    echo "   HTTP Status: $http_code"
    
    if [ "$http_code" = "200" ]; then
        if [ -n "$body" ] && [[ "$body" == *"$expected_content"* ]]; then
            echo -e "   ${GREEN}✅ PASS${NC}: Expected content found"
            echo "   Response: $(echo "$body" | head -c 100)..."
            return 0
        elif [ -z "$body" ]; then
            echo -e "   ${YELLOW}⚠️  EMPTY${NC}: No response body (workflow may not be activated)"
            return 1
        else
            echo -e "   ${RED}❌ FAIL${NC}: Expected '$expected_content' not found"
            echo "   Response: $(echo "$body" | head -c 100)..."
            return 1
        fi
    else
        echo -e "   ${RED}❌ FAIL${NC}: HTTP $http_code"
        return 1
    fi
    echo ""
}

# Service Health Checks
echo "🔍 Service Health Checks"
echo "========================"

# Check n8n
if curl -s http://localhost:5678/ > /dev/null; then
    echo -e "${GREEN}✅ n8n Service${NC}: Running on port 5678"
else
    echo -e "${RED}❌ n8n Service${NC}: Not accessible"
fi

# Check Flask
if curl -s http://localhost:5001/ > /dev/null; then
    echo -e "${GREEN}✅ Flask Service${NC}: Running on port 5001"
else
    echo -e "${RED}❌ Flask Service${NC}: Not accessible"
fi

# Check ngrok
if curl -s http://localhost:4040/api/tunnels > /dev/null; then
    echo -e "${GREEN}✅ ngrok Tunnel${NC}: Active"
    ngrok_url=$(curl -s http://localhost:4040/api/tunnels | grep -o '"public_url":"[^"]*' | cut -d'"' -f4 | grep https)
    echo "   Public URL: $ngrok_url"
else
    echo -e "${RED}❌ ngrok Tunnel${NC}: Not accessible"
fi
echo ""

# Test Messages Array
declare -a test_cases=(
    "hi|<Message>|Greeting Test"
    "menu|<Message>|Menu Test"
    "fees|Fee Structure|FAQ Fees Test"
    "courses|Available Courses|FAQ Courses Test"
    "admission|Admission Process|FAQ Admission Test"
    "library|Library Services|FAQ Library Test"
    "hostel|Hostel Facilities|FAQ Hostel Test"
    "notes|Study Notes|Resources Notes Test"
    "syllabus|Course Materials|Resources Syllabus Test"
    "help|Student Support|Support Test"
    "unknown_query|didn't quite understand|Fallback Test"
)

# Test n8n Endpoint
echo "🧪 Testing n8n Webhook Endpoint"
echo "================================"
n8n_pass_count=0
n8n_total_count=0

for test_case in "${test_cases[@]}"; do
    IFS='|' read -r message expected_content test_name <<< "$test_case"
    ((n8n_total_count++))
    if run_test "$N8N_URL" "$message" "$test_name (n8n)" "$expected_content"; then
        ((n8n_pass_count++))
    fi
done

echo -e "${BLUE}n8n Test Summary: $n8n_pass_count/$n8n_total_count tests passed${NC}"
echo ""

# Test Flask Endpoint
echo "🧪 Testing Flask Backup Endpoint"
echo "================================="
flask_pass_count=0
flask_total_count=0

for test_case in "${test_cases[@]}"; do
    IFS='|' read -r message expected_content test_name <<< "$test_case"
    ((flask_total_count++))
    if run_test "$FLASK_URL" "$message" "$test_name (Flask)" "$expected_content"; then
        ((flask_pass_count++))
    fi
done

echo -e "${BLUE}Flask Test Summary: $flask_pass_count/$flask_total_count tests passed${NC}"
echo ""

# Performance Tests
echo "⚡ Performance Tests"
echo "==================="

echo "Testing response times..."
for i in {1..5}; do
    response_time=$(curl -o /dev/null -s -w "%{time_total}" -X POST "$FLASK_URL" \
        -H "Content-Type: application/x-www-form-urlencoded" \
        -d "Body=hi&From=$TEST_PHONE_FROM&To=$TEST_PHONE_TO")
    echo "Test $i: ${response_time}s"
done
echo ""

# Generate Final Report
echo "📊 Final Test Report"
echo "===================="
echo "Test Date: $(date)"
echo "n8n Endpoint: $N8N_URL"
echo "Flask Endpoint: $FLASK_URL"
echo ""

if [ $n8n_pass_count -eq $n8n_total_count ]; then
    echo -e "${GREEN}✅ n8n Tests: ALL PASSED ($n8n_pass_count/$n8n_total_count)${NC}"
    n8n_status="READY"
else
    echo -e "${YELLOW}⚠️  n8n Tests: $n8n_pass_count/$n8n_total_count passed${NC}"
    if [ $n8n_pass_count -eq 0 ]; then
        echo -e "${RED}❌ n8n workflow likely NOT ACTIVATED${NC}"
        n8n_status="NEEDS_ACTIVATION"
    else
        n8n_status="PARTIAL"
    fi
fi

if [ $flask_pass_count -eq $flask_total_count ]; then
    echo -e "${GREEN}✅ Flask Tests: ALL PASSED ($flask_pass_count/$flask_total_count)${NC}"
    flask_status="READY"
else
    echo -e "${RED}❌ Flask Tests: $flask_pass_count/$flask_total_count passed${NC}"
    flask_status="ISSUES"
fi

echo ""
echo "🎯 Next Steps:"
if [ "$n8n_status" = "NEEDS_ACTIVATION" ]; then
    echo "1. 🔧 Activate n8n workflow at http://localhost:5678"
    echo "2. 🔄 Re-run this test: ./complete_test_suite.sh"
    echo "3. 📱 Update Twilio webhook to n8n URL"
elif [ "$n8n_status" = "READY" ]; then
    echo "1. ✅ n8n is ready - update Twilio webhook"
    echo "2. 📱 Test with real WhatsApp messages"
    echo "3. 📊 Monitor n8n executions for analytics"
else
    echo "1. 🔧 Check n8n workflow configuration"
    echo "2. 🔄 Verify webhook endpoint setup"
fi

if [ "$flask_status" = "READY" ]; then
    echo "4. ✅ Flask backup is working perfectly"
else
    echo "4. 🚨 Check Flask app issues"
fi

echo ""
echo "🔗 Useful Links:"
echo "   n8n Interface: http://localhost:5678"
echo "   ngrok Monitor: http://localhost:4040"
echo "   Test Script: ./complete_test_suite.sh"

# Save results to file
cat > test_results.json << EOF
{
  "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "n8n": {
    "url": "$N8N_URL",
    "passed": $n8n_pass_count,
    "total": $n8n_total_count,
    "status": "$n8n_status"
  },
  "flask": {
    "url": "$FLASK_URL",
    "passed": $flask_pass_count,
    "total": $flask_total_count,
    "status": "$flask_status"
  },
  "services": {
    "n8n_running": $(curl -s http://localhost:5678/ > /dev/null && echo true || echo false),
    "flask_running": $(curl -s http://localhost:5001/ > /dev/null && echo true || echo false),
    "ngrok_active": $(curl -s http://localhost:4040/api/tunnels > /dev/null && echo true || echo false)
  }
}
EOF

echo ""
echo "📄 Test results saved to: test_results.json"