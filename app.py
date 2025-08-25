import os
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

@app.get("/")
def health():
    return {"status": "ok", "service": "whatsapp-education-bot"}

@app.post("/whatsapp")
def whatsapp_bot():
    incoming_msg = (request.values.get("Body") or "").strip().lower()
    resp = MessagingResponse()
    msg = resp.message()

    if any(greet in incoming_msg for greet in ["hi", "hello", "hey"]):
        reply = (
            "👋 Hello! Welcome to EduBot.\n"
            "How can I assist you today?\n\n"
            "1️⃣ Admissions Info\n"
            "2️⃣ Exam Schedule\n"
            "3️⃣ Fee Payment\n"
            "4️⃣ Contact Support"
        )
    elif incoming_msg in ["1", "admissions", "admission"]:
        reply = (
            "📘 Admission Details:\n\n"
            "✅ MBA Admissions open till *10th Sept 2025*.\n"
            "✅ Apply: https://example.com/apply\n"
            "Would you like me to share the brochure? (yes/no)"
        )
    elif incoming_msg in ["2", "exam", "exams", "schedule"]:
        reply = (
            "📝 Upcoming Exam Schedule:\n\n"
            "📅 MBA Sem-1: 15th Sept 2025\n"
            "📅 BCA Sem-3: 18th Sept 2025\n"
            "📅 BBA Sem-5: 20th Sept 2025\n"
            "Do you want me to set a reminder? (yes/no)"
        )
    elif incoming_msg in ["3", "fees", "fee", "payment"]:
        reply = (
            "💳 Fee Payment Info:\n\n"
            "Outstanding Fees: ₹ 45,000\n"
            "Due Date: 31st Aug 2025\n\n"
            "👉 Pay here: https://example.com/fees\n"
            "After payment, the receipt will be sent automatically ✅"
        )
    elif incoming_msg in ["4", "support", "help"]:
        reply = (
            "📞 Contact Support:\n"
            "For academic queries: academic-support@example.com\n"
            "For technical issues: tech-support@example.com\n"
            "Helpline: +91-9876543210"
        )
    else:
        reply = (
            "⚠️ Sorry, I didn’t understand that.\n"
            "Please reply with:\n"
            "1️⃣ Admissions\n2️⃣ Exam Schedule\n3️⃣ Fee Payment\n4️⃣ Support"
        )

    msg.body(reply)
    return str(resp)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)