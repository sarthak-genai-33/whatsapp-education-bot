# Quick Start: n8n WhatsApp Bot Integration

## 🚀 5-Minute Setup Guide

This guide helps you quickly set up the n8n workflow for your WhatsApp Education Bot.

## Prerequisites
- ✅ Existing WhatsApp Education Bot running
- ✅ WhatsApp Business API access
- ✅ Docker or Node.js installed

## Step 1: Install n8n

### Option A: Docker (Recommended)
```bash
docker run -d \
  --name n8n \
  -p 5678:5678 \
  -v ~/.n8n:/home/node/.n8n \
  n8nio/n8n
```

### Option B: npm
```bash
npm install n8n -g
n8n start
```

## Step 2: Import Workflow

1. Open http://localhost:5678
2. Click "+" → "Import from file"
3. Select `n8n-workflow.json`
4. Click "Import"

## Step 3: Configure Environment

Set these environment variables:
```bash
export WHATSAPP_ACCESS_TOKEN="your_token_here"
export WHATSAPP_PHONE_NUMBER_ID="your_phone_id_here"
export FLASK_APP_URL="http://localhost:5001"
```

## Step 4: Update Webhook URLs

### For Development:
1. Start ngrok: `ngrok http 5678`
2. Copy ngrok URL
3. In Twilio Console, set webhook to: `https://your-ngrok-url.ngrok-free.app/webhook/n8n-whatsapp-webhook`

### For Production:
1. Deploy n8n to your server
2. Set webhook to: `https://your-n8n-domain.com/webhook/n8n-whatsapp-webhook`

## Step 5: Configure WhatsApp Sender Node

1. In n8n workflow, click "WhatsApp Message Sender" node
2. Replace `YOUR_WHATSAPP_ACCESS_TOKEN` with your actual token
3. Replace `YOUR_PHONE_NUMBER_ID` with your phone number ID
4. Save the workflow

## Step 6: Test the Integration

1. Activate the workflow in n8n
2. Send "hi" to your WhatsApp number
3. Check n8n execution logs
4. Verify response is received

## Common Configuration Values

```json
{
  "whatsapp_access_token": "EAAxxxxxxxxxx",
  "phone_number_id": "123456789012345",
  "flask_app_url": "http://localhost:5001",
  "n8n_webhook_path": "n8n-whatsapp-webhook"
}
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Webhook not triggered | Check ngrok URL in Twilio settings |
| WhatsApp send fails | Verify access token and phone number ID |
| Flask bridge fails | Ensure Flask app is running on port 5001 |

## Next Steps

1. ✅ Monitor analytics in n8n execution logs
2. ✅ Customize response messages in generator nodes
3. ✅ Add additional message categories
4. ✅ Set up production deployment

## Production Checklist

- [ ] Deploy n8n to production server
- [ ] Configure HTTPS for webhooks
- [ ] Set up environment variables
- [ ] Enable n8n authentication
- [ ] Update Twilio webhook URL
- [ ] Test end-to-end flow
- [ ] Monitor execution logs

For detailed setup instructions, see `N8N_SETUP.md`.