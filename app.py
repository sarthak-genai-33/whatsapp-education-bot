import os
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

# Student Support Data
faq_data = {
    "courses": "📚 *Available Courses:*\n• MBA (2 years) - Management Studies\n• BCA (3 years) - Computer Applications\n• BBA (3 years) - Business Administration\n• M.Tech (2 years) - Engineering Specializations\n📧 Details: courses@example.com",
    "fees": "💰 *Fee Structure:*\n• MBA: ₹2,50,000 per year\n• BCA: ₹80,000 per year\n• BBA: ₹90,000 per year\n• M.Tech: ₹1,20,000 per year\n📧 Finance office: fees@example.com",
    "admission": "🎓 *Admission Process:*\n• Application: Online portal\n• Entrance Test: Subject-specific\n• Interview: Final selection\n• Documents: Academic transcripts required\n📧 Admissions: admissions@example.com",
    "results": "📊 *Results Information:*\n• Semester results: Published online\n• Grade sheets: Available for download\n• Transcripts: Apply through student portal\n📧 Academics: results@example.com",
    "schedule": "📅 *Academic Schedule:*\n• Classes: 9 AM - 4 PM (Mon-Fri)\n• Exams: End of each semester\n• Holidays: As per academic calendar\n📧 Schedule queries: schedule@example.com",
    "library": "📚 *Library Services:*\n• Hours: Mon-Fri 8AM-8PM, Sat 9AM-5PM\n• Books: 50,000+ collection\n• Digital resources: E-books & journals\n📧 Library: library@example.com",
    "hostel": "🏠 *Hostel Facilities:*\n• AC/Non-AC rooms available\n• Mess facility included\n• Wi-Fi & study rooms\n📧 Hostel: hostel@example.com",
    "transport": "🚌 *Transport Services:*\n• College bus from major locations\n• Route timings: 7 AM - 6 PM\n• Monthly pass available\n📧 Transport: transport@example.com"
}

# Academic Resources
academic_resources = {
    "syllabus": "📖 *Syllabus & Course Materials:*\n• Complete syllabus for all courses\n• Unit-wise breakdown available\n• Learning objectives included\n🔗 Download: https://example.com/syllabus",
    "notes": "📝 *Study Notes:*\n• Chapter-wise notes\n• Faculty-prepared materials\n• Previous year papers\n🔗 Access: https://example.com/notes",
    "lectures": "🎥 *Recorded Lectures:*\n• Video lectures by faculty\n• Subject-wise categorization\n• HD quality recordings\n🔗 Portal: https://example.com/lectures",
    "ebooks": "📱 *E-Books & Resources:*\n• Digital library access\n• Reference books\n• Research journals\n🔗 Library: https://example.com/ebooks"
}

# Personalized Updates
student_updates = {
    "timetable": "📅 *This Week's Exam Timetable:*\n• Monday: Mathematics (9 AM - 12 PM)\n• Wednesday: Science (2 PM - 5 PM)\n• Friday: English (10 AM - 1 PM)\n📍 Venue: Main Examination Hall",
    "reminders": "🔔 *Class Reminders:*\n• Tomorrow: Advanced Programming Lab\n• Thursday: Marketing Strategy Seminar\n• Friday: Project Submission Deadline\n⏰ Don't forget to attend!",
    "assignments": "📋 *Assignment Deadlines:*\n• Data Structures Assignment: 25th Aug\n• Marketing Case Study: 28th Aug\n• Research Paper: 30th Aug\n📧 Submit via student portal"
}

def get_main_menu():
    return (
        "🎓 Welcome to Student Support Bot!\n"
        "Your one-stop solution for academic information.\n\n"
        "📚 *What can I help you with?*\n\n"
        "🔹 *FAQs:* courses, fees, admission, results, schedule\n"
        "🔹 *Resources:* syllabus, notes, lectures, ebooks\n"
        "🔹 *Updates:* timetable, reminders, assignments\n"
        "🔹 *Facilities:* library, hostel, transport\n\n"
        "💡 *Quick Commands:*\n"
        "• Type any keyword (e.g., 'courses', 'fees', 'notes')\n"
        "• Type 'resources' for academic materials\n"
        "• Type 'updates' for personalized information\n"
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
    
    # FAQ Categories
    elif incoming_msg in list(faq_data.keys()):
        reply = faq_data[incoming_msg]
    
    # Academic Resources
    elif incoming_msg in ["resources", "materials", "study"]:
        reply = (
            "📚 *Academic Resources*\n\n"
            "What type of resource do you need?\n\n"
            "🔹 Type 'syllabus' - Course syllabus & materials\n"
            "🔹 Type 'notes' - Study notes & papers\n"
            "🔹 Type 'lectures' - Recorded video lectures\n"
            "🔹 Type 'ebooks' - Digital books & journals\n\n"
            "💡 Or directly type the resource name!"
        )
    elif incoming_msg in list(academic_resources.keys()):
        reply = academic_resources[incoming_msg]
    
    # Personalized Updates
    elif incoming_msg in ["updates", "personal", "my"]:
        reply = (
            "📅 *Personalized Updates*\n\n"
            "What updates would you like to see?\n\n"
            "🔹 Type 'timetable' - This week's exam schedule\n"
            "🔹 Type 'reminders' - Class & event reminders\n"
            "🔹 Type 'assignments' - Assignment deadlines\n\n"
            "💡 Stay updated with your academic schedule!"
        )
    elif incoming_msg in list(student_updates.keys()):
        reply = student_updates[incoming_msg]
    
    # Contact and Support
    elif incoming_msg in ["contact", "support", "help", "helpline"]:
        reply = (
            "📞 *Student Support Contact*\n\n"
            "🎓 *Academic Support:*\n"
            "📧 academic-support@example.com\n"
            "📞 +91-9876543210\n\n"
            "💻 *Technical Support:*\n"
            "📧 tech-support@example.com\n"
            "📞 +91-9876543211\n\n"
            "📚 *Library Support:*\n"
            "📧 library@example.com\n"
            "📞 +91-9876543212\n\n"
            "🕒 *Office Hours:* Mon-Fri 9AM-6PM"
        )
    
    # Quick access shortcuts
    elif "fee" in incoming_msg or "cost" in incoming_msg or "price" in incoming_msg:
        reply = faq_data["fees"]
    elif "course" in incoming_msg or "program" in incoming_msg:
        reply = faq_data["courses"]
    elif "exam" in incoming_msg or "test" in incoming_msg:
        reply = student_updates["timetable"]
    elif "class" in incoming_msg or "reminder" in incoming_msg:
        reply = student_updates["reminders"]
    elif "assignment" in incoming_msg or "homework" in incoming_msg:
        reply = student_updates["assignments"]
    
    # Fallback for unrecognized input
    else:
        reply = (
            "🤔 I didn't quite understand that.\n\n"
            "📋 *Try these commands:*\n"
            "• Type 'menu' for main options\n"
            "• Type 'courses' for course information\n"
            "• Type 'fees' for fee structure\n"
            "• Type 'resources' for study materials\n"
            "• Type 'updates' for personalized info\n"
            "• Type 'help' for support\n\n"
            "💡 *Quick tip:* Use keywords like 'library', 'hostel', 'notes', etc."
        )

    resp.message(reply)
    return str(resp)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)