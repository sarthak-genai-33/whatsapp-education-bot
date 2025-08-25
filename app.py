import os
import json
from datetime import datetime, timedelta
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

# Sample data structures for enhanced features
student_data = {
    "fees": {
        "outstanding": 45000,
        "due_date": "31st Aug 2025",
        "payment_link": "https://example.com/fees"
    },
    "exams": [
        {"course": "MBA Sem-1", "date": "15th Sept 2025", "venue": "Main Hall"},
        {"course": "BCA Sem-3", "date": "18th Sept 2025", "venue": "Lab-2"},
        {"course": "BBA Sem-5", "date": "20th Sept 2025", "venue": "Room-301"}
    ],
    "attendance": {"current_month": "85%", "target": "90%"},
    "grades": {"last_semester": "8.5 CGPA", "rank": "15th in class"}
}

admission_data = {
    "mba": {"deadline": "10th Sept 2025", "link": "https://example.com/mba-apply"},
    "bca": {"deadline": "5th Sept 2025", "link": "https://example.com/bca-apply"},
    "bba": {"deadline": "8th Sept 2025", "link": "https://example.com/bba-apply"}
}

faq_data = {
    "library": "📚 Library Hours: Mon-Fri 8AM-8PM, Sat 9AM-5PM",
    "hostel": "🏠 Hostel facilities available with AC/Non-AC rooms. Contact: hostel@example.com",
    "transport": "🚌 College bus service available from major locations. Route details: transport@example.com",
    "placement": "💼 Placement cell provides training & job opportunities. Contact: placements@example.com"
}

def get_main_menu():
    return (
        "🎓 Welcome to EduBot - Your Educational Assistant!\n"
        "How can I help you today?\n\n"
        "📚 *Main Services:*\n"
        "1️⃣ Student Support & FAQs\n"
        "2️⃣ Admissions & Enrollment\n"
        "3️⃣ Attendance & Performance\n"
        "4️⃣ Exams & Assessments\n"
        "5️⃣ Fee Management\n"
        "6️⃣ Parent-Teacher Communication\n"
        "7️⃣ Learning & EdTech Support\n\n"
        "💡 *Quick Access:*\n"
        "• Type 'fees' for fee info\n"
        "• Type 'exams' for exam schedule\n"
        "• Type 'help' for support\n"
        "• Type 'menu' to see this again"
    )

@app.get("/")
def health():
    return {"status": "ok", "service": "whatsapp-education-bot", "version": "2.0"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "whatsapp-education-bot"}

@app.post("/whatsapp")
def whatsapp_bot():
    incoming_msg = (request.values.get("Body") or "").strip().lower()
    resp = MessagingResponse()
    print(f"Incoming: {incoming_msg}")

    # Main menu and greetings
    if any(greet in incoming_msg for greet in ["hi", "hello", "hey", "start", "menu"]):
        reply = get_main_menu()
    
    # 1. Student Support & FAQs
    elif incoming_msg in ["1", "student", "support", "faq", "faqs"]:
        reply = (
            "📚 *Student Support & FAQs*\n\n"
            "What would you like to know about?\n\n"
            "🔹 Type 'library' - Library timings & facilities\n"
            "🔹 Type 'hostel' - Accommodation details\n"
            "🔹 Type 'transport' - Bus routes & timings\n"
            "🔹 Type 'placement' - Career & placement info\n"
            "🔹 Type 'syllabus' - Course materials\n"
            "🔹 Type 'notes' - Study resources\n\n"
            "💡 Or ask me anything else!"
        )
    elif incoming_msg in list(faq_data.keys()):
        reply = faq_data[incoming_msg]
    elif incoming_msg in ["syllabus", "course", "materials"]:
        reply = (
            "📖 *Course Materials Available:*\n\n"
            "📚 Complete syllabus for all semesters\n"
            "📝 Lecture notes & presentations\n"
            "📹 Recorded lectures & e-books\n\n"
            "📥 Download: https://example.com/resources\n"
            "📧 Email: academics@example.com"
        )
    elif incoming_msg in ["notes", "study", "resources"]:
        reply = (
            "📝 *Study Resources:*\n\n"
            "✅ Chapter-wise notes available\n"
            "✅ Previous year question papers\n"
            "✅ Reference books & journals\n\n"
            "🔗 Access: https://example.com/study-materials"
        )
    
    # 2. Admissions & Enrollments
    elif incoming_msg in ["2", "admissions", "admission", "enrollment", "apply"]:
        reply = (
            "🎓 *Admissions & Enrollment*\n\n"
            "📅 *Current Openings:*\n"
            "• MBA - Deadline: 10th Sept 2025\n"
            "• BCA - Deadline: 5th Sept 2025\n"
            "• BBA - Deadline: 8th Sept 2025\n\n"
            "📋 *What do you need?*\n"
            "🔹 Type 'mba' for MBA details\n"
            "🔹 Type 'bca' for BCA details\n"
            "🔹 Type 'bba' for BBA details\n"
            "🔹 Type 'brochure' for program brochure\n"
            "🔹 Type 'status' for application status"
        )
    elif incoming_msg in ["mba", "bca", "bba"]:
        course_info = admission_data.get(incoming_msg, {})
        reply = (
            f"📘 *{incoming_msg.upper()} Program Details:*\n\n"
            f"📅 Application Deadline: {course_info.get('deadline', 'TBA')}\n"
            f"📝 Apply Online: {course_info.get('link', 'https://example.com/apply')}\n\n"
            "📋 *Required Documents:*\n"
            "• Academic transcripts\n"
            "• Entrance exam scores\n"
            "• Identity proof\n\n"
            "Would you like the detailed brochure? (yes/no)"
        )
    elif incoming_msg in ["brochure", "yes"]:
        reply = (
            "📄 *Program Brochure Sent!*\n\n"
            "✅ Download link: https://example.com/brochure\n"
            "📧 Also sent to your registered email\n\n"
            "Need application form? Type 'application'"
        )
    
    # 3. Attendance & Performance
    elif incoming_msg in ["3", "attendance", "performance", "progress"]:
        reply = (
            f"📊 *Your Academic Performance*\n\n"
            f"📈 *Attendance:* {student_data['attendance']['current_month']} (Target: {student_data['attendance']['target']})\n"
            f"🎯 *Last Semester:* {student_data['grades']['last_semester']}\n"
            f"🏆 *Class Rank:* {student_data['grades']['rank']}\n\n"
            "📋 *Quick Actions:*\n"
            "🔹 Type 'absent' - Report absence\n"
            "🔹 Type 'report' - Detailed progress report\n"
            "🔹 Type 'tips' - Performance improvement tips"
        )
    elif incoming_msg in ["absent", "absence"]:
        reply = (
            "⚠️ *Report Absence*\n\n"
            "Your absence has been noted for today.\n"
            "📧 Notification sent to parents\n\n"
            "📋 Reason (optional): Reply with reason\n"
            "🏥 Medical certificate required for 3+ days"
        )
    
    # 4. Exams & Assessments
    elif incoming_msg in ["4", "exam", "exams", "schedule", "assessment"]:
        reply = (
            "📝 *Exams & Assessments*\n\n"
            "📅 *Upcoming Exams:*\n"
        )
        for exam in student_data["exams"]:
            reply += f"• {exam['course']}: {exam['date']} ({exam['venue']})\n"
        reply += (
            "\n📋 *Quick Actions:*\n"
            "🔹 Type 'register' - Register for exams\n"
            "🔹 Type 'results' - Check exam results\n"
            "🔹 Type 'reminder' - Set exam reminders"
        )
    elif incoming_msg in ["results", "result"]:
        reply = (
            "🏆 *Exam Results*\n\n"
            "📊 *Latest Results:*\n"
            "• Mid-term: 85% (A grade)\n"
            "• Assignment-1: 92% (A+ grade)\n"
            "• Quiz-3: 78% (B+ grade)\n\n"
            "📈 Overall Performance: Excellent\n"
            "📧 Detailed scorecard sent to email"
        )
    
    # 5. Fee Management
    elif incoming_msg in ["5", "fees", "fee", "payment", "pay"]:
        reply = (
            f"💳 *Fee Management*\n\n"
            f"💰 *Outstanding Amount:* ₹{student_data['fees']['outstanding']:,}\n"
            f"📅 *Due Date:* {student_data['fees']['due_date']}\n\n"
            "📋 *Payment Options:*\n"
            "🔹 Type 'paynow' - Pay online instantly\n"
            "🔹 Type 'installment' - EMI options\n"
            "🔹 Type 'receipt' - Previous receipts\n"
            "🔹 Type 'breakdown' - Fee structure\n\n"
            "💡 *Auto-payment available* - Type 'autopay'"
        )
    elif incoming_msg in ["paynow", "pay now"]:
        reply = (
            f"💳 *Pay Now - ₹{student_data['fees']['outstanding']:,}*\n\n"
            f"🔗 *Secure Payment Link:*\n{student_data['fees']['payment_link']}\n\n"
            "💳 *Accepted Methods:*\n"
            "• Credit/Debit Cards\n"
            "• UPI & Digital Wallets\n"
            "• Net Banking\n\n"
            "📧 Receipt will be emailed instantly ✅\n"
            "📱 SMS confirmation will be sent"
        )
    
    # 6. Parent-Teacher Communication
    elif incoming_msg in ["6", "parent", "teacher", "communication", "ptm"]:
        reply = (
            "👨‍👩‍👧‍👦 *Parent-Teacher Communication*\n\n"
            "📅 *Upcoming Events:*\n"
            "• Parent-Teacher Meeting: 25th Aug 2025 at 10 AM\n"
            "• Annual Day Celebration: 15th Sep 2025\n\n"
            "📋 *Quick Actions:*\n"
            "🔹 Type 'ptm' - PTM details & booking\n"
            "🔹 Type 'feedback' - Share feedback\n"
            "🔹 Type 'homework' - Today's homework\n"
            "🔹 Type 'meeting' - Schedule teacher meeting"
        )
    elif incoming_msg in ["homework", "assignments"]:
        reply = (
            "📚 *Today's Homework & Assignments*\n\n"
            "📝 *Mathematics:* Complete Chapter 5 exercises\n"
            "🔬 *Science:* Lab report submission\n"
            "📖 *English:* Essay on 'Digital Education'\n"
            "🌍 *Social Studies:* Map work - Indian states\n\n"
            "📅 *Due Date:* Tomorrow before 9 AM\n"
            "📧 Details sent to parents via email"
        )
    
    # 7. EdTech & Learning Support
    elif incoming_msg in ["7", "learning", "edtech", "quiz", "study"]:
        reply = (
            "🚀 *EdTech & Learning Support*\n\n"
            "📱 *Digital Learning Features:*\n"
            "• Micro-learning modules (5-min lessons)\n"
            "• Interactive quizzes & assessments\n"
            "• AI-powered doubt resolution\n"
            "• Recorded lecture library\n\n"
            "📋 *Try Now:*\n"
            "🔹 Type 'module' - Start a micro-lesson\n"
            "🔹 Type 'quiz' - Take a quick quiz\n"
            "🔹 Type 'doubt' - Ask any question\n"
            "🔹 Type 'videos' - Access video library"
        )
    elif incoming_msg in ["module", "lesson"]:
        reply = (
            "📚 *5-Minute Learning Module*\n\n"
            "🎯 *Today's Topic:* Photosynthesis Basics\n\n"
            "🌱 *Quick Facts:*\n"
            "• Plants make food using sunlight\n"
            "• Chlorophyll gives green color\n"
            "• Oxygen is released as by-product\n\n"
            "🎥 *Watch Video:* https://example.com/video\n"
            "❓ *Quiz:* Type 'quiz' to test your knowledge"
        )
    elif incoming_msg in ["quiz", "test"]:
        reply = (
            "🧠 *Quick Quiz - Photosynthesis*\n\n"
            "❓ *Question 1/3:*\n"
            "What gas do plants release during photosynthesis?\n\n"
            "A) Carbon dioxide\n"
            "B) Oxygen\n"
            "C) Nitrogen\n"
            "D) Hydrogen\n\n"
            "💡 Reply with A, B, C, or D"
        )
    elif incoming_msg in ["b", "oxygen"]:
        reply = (
            "✅ *Correct Answer!*\n\n"
            "🎉 Plants release oxygen during photosynthesis\n\n"
            "🏆 *Your Score:* 1/3\n"
            "📈 *Progress:* +10 learning points\n\n"
            "➡️ *Next Question:* Type 'next'\n"
            "🔄 *Restart Quiz:* Type 'quiz'"
        )
    
    # Contact and Support (enhanced)
    elif incoming_msg in ["contact", "support", "helpline"]:
        reply = (
            "📞 *Contact & Support*\n\n"
            "🎓 *Academic Support:*\n"
            "📧 academic-support@example.com\n"
            "📞 +91-9876543210\n\n"
            "💻 *Technical Support:*\n"
            "📧 tech-support@example.com\n"
            "📞 +91-9876543211\n\n"
            "👨‍💼 *Admissions Office:*\n"
            "📧 admissions@example.com\n"
            "📞 +91-9876543212\n\n"
            "🕒 *Office Hours:* Mon-Fri 9AM-6PM"
        )
    
    # Fallback for unrecognized input
    else:
        reply = (
            "🤔 I didn't quite understand that.\n\n"
            "📋 *Try these commands:*\n"
            "• Type 'menu' for main options\n"
            "• Type 'help' for support\n"
            "• Type 'fees' for fee info\n"
            "• Type 'exams' for exam schedule\n\n"
            "💡 *Quick Access:* 1-7 for main services"
        )

    resp.message(reply)
    return str(resp)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)