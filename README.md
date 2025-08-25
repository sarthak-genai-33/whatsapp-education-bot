# WhatsApp Education Bot (Basic)

A minimal WhatsApp bot for the Education domain using **Python (Flask)** and **Twilio's WhatsApp API**.
Covers: Admissions info, Exam schedules, Fee payment info, and Support.

---

## Features
- Keyword-based flow: *Admissions*, *Exams*, *Fees*, *Support*
- Simple, stateless replies using TwiML
- Ready for local testing (ngrok) and deployment (Heroku/any PaaS)

## Tech
- Python 3.9+
- Flask
- Twilio (WhatsApp Sandbox)
- Gunicorn (for deployment)

---

## Quickstart (Local)

1) **Clone / extract** this project and enter the folder:
```bash
cd whatsapp-education-bot
```

2) **Create a virtual environment** and install deps:
```bash
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

3) **Run the server**:
```bash
python app.py
```
The app listens on `http://localhost:5000`.

4) **Expose locally** with ngrok (or any tunnel):
```bash
ngrok http 5000
```
Note the HTTPS forwarding URL, e.g. `https://abcd-1234.ngrok-free.app`.

5) **Connect Twilio WhatsApp Sandbox**:
   - In Twilio Console → Messaging → **Try it out** → **Send a WhatsApp message**.
   - Join the sandbox by sending the provided *join code* to the given WhatsApp number.
   - Set the **WHEN A MESSAGE COMES IN** webhook (for the sandbox) to:
     ```
     https://YOUR-NGROK-ID.ngrok-free.app/whatsapp
     ```

6) **Test** by messaging your sandbox WhatsApp number:
   - Send `hi` to see the menu.
   - Send `1`, `2`, `3`, or `4` for the respective sections.

---

## Deploy (Example: Heroku)

```bash
# Ensure you have a Git repo
git init
heroku create whatsapp-education-bot-basic
git add .
git commit -m "Initial commit: WhatsApp Education Bot (basic)"
git push heroku main

# Or for older stacks/flows:
git push heroku HEAD:main
```

Then set your WhatsApp webhook in Twilio to your deployed URL:
```
https://your-app.herokuapp.com/whatsapp
```

---

## Manual Webhook Test (without Twilio)

You can simulate Twilio's webhook (basic test of routing/logic) using curl:
```bash
curl -X POST http://localhost:5000/whatsapp \      --data-urlencode "Body=hi"
```

---

## Next Steps / Enhancements
- Persist sessions & user profiles in a DB (MySQL/MongoDB)
- Add reminders and notifications
- Integrate with LMS/ERP
- Add AI Q&A for academic FAQs