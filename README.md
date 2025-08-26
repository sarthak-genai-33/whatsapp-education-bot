# WhatsApp Student Support Bot

A focused WhatsApp bot for **Student Engagement & Support** using **Python (Flask)** and **Twilio's WhatsApp API**.
Specialized in answering FAQs, providing academic resources, and sharing personalized student updates.

---

## 🚀 Features

### **Student Engagement & Support**
- ❓ **Answer FAQs** about courses, fees, admission process, results, schedules
- 📱 **Share personalized updates** (exam timetables, class reminders, assignment deadlines)
- 📚 **Provide instant academic resources** (syllabus, notes, recorded lectures, e-books)
- 🏠 **Campus facilities info** (library, hostel, transport)

### **🤖 n8n Workflow Integration** (NEW!)
- 🔄 **Advanced Automation**: Intelligent message routing and processing
- 📊 **Real-time Analytics**: Message tracking and user interaction analytics
- ⚡ **Enhanced Response Generation**: Modular and dynamic content generation
- 📈 **Scalable Architecture**: Support for high-volume message processing
- 🌐 **Multi-channel Ready**: Foundation for Telegram, Discord, and Slack integration
- 🔗 **Seamless Integration**: Works alongside existing Flask application

#### **Core Capabilities:**

**📋 FAQ Categories:**
- 📘 Course information and programs
- 💰 Fee structure and payment details
- 🎓 Admission process and requirements
- 📊 Results and academic performance
- 📅 Academic schedules and timings
- 📚 Library services and hours
- 🏠 Hostel facilities and accommodation
- 🚌 Transport services and routes

**📚 Academic Resources:**
- 📖 Complete course syllabus and materials
- 📝 Chapter-wise study notes
- 🎥 Recorded video lectures by faculty
- 📱 E-books and digital library access

**📅 Personalized Updates:**
- 📋 Weekly exam timetables with venues
- 🔔 Class reminders and important events
- 📝 Assignment deadlines and submissions

---

## 💻 Tech Stack
- **Backend**: Python 3.9+, Flask 3.0.3
- **Messaging**: Twilio WhatsApp API (9.3.5)
- **Deployment**: Gunicorn 22.0.0
- **Automation**: n8n workflow engine (optional)
- **Data**: In-memory structures (easily extensible to databases)
- **Features**: Real-time messaging, Rich text responses, Keyword-based navigation
- **Analytics**: Built-in message tracking and user analytics

---

## 💬 Example Conversation Flows

### **Course Inquiry:**
```
Student: "courses"
Bot: "📚 Available Courses:
• MBA (2 years) - Management Studies
• BCA (3 years) - Computer Applications
• BBA (3 years) - Business Administration
📧 Details: courses@example.com"
```

### **Fee Information:**
```
Student: "fees"
Bot: "💰 Fee Structure:
• MBA: ₹2,50,000 per year
• BCA: ₹80,000 per year
• BBA: ₹90,000 per year
📧 Finance office: fees@example.com"
```

### **Academic Resources:**
```
Student: "notes"
Bot: "📝 Study Notes:
• Chapter-wise notes
• Faculty-prepared materials
• Previous year papers
🔗 Access: https://example.com/notes"
```

### **Personalized Updates:**
```
Student: "timetable"
Bot: "📅 This Week's Exam Timetable:
• Monday: Mathematics (9 AM - 12 PM)
• Wednesday: Science (2 PM - 5 PM)
• Friday: English (10 AM - 1 PM)
📍 Venue: Main Examination Hall"
```

---

## 🏆 Benefits
- **24x7 availability** for students to get instant academic support
- **Reduced admin workload** with automated FAQ responses
- **Enhanced student experience** with quick access to resources
- **Improved communication** between students and faculty
- **Centralized information** hub for all academic queries
- **Cost-effective** solution compared to full portal development

---

## 🚀 Quickstart (Local)

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

3) **Run the server** (using port 5001 to avoid conflicts):
```bash
PORT=5001 python app.py
```
The app listens on `http://localhost:5001`.

4) **Expose locally** with ngrok (or any tunnel):
```bash
ngrok http 5001
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
   - Send `hi` to see the student support menu
   - Try keywords like `courses`, `fees`, `library`, `notes`
   - Ask for resources: `syllabus`, `lectures`, `ebooks`
   - Get updates: `timetable`, `assignments`, `reminders`
   - Explore facilities: `hostel`, `transport`

### 🤖 Optional: Advanced n8n Workflow Setup

For enhanced automation and analytics:

```bash
# Quick n8n setup with Docker
docker run -d --name n8n -p 5678:5678 -v ~/.n8n:/home/node/.n8n n8nio/n8n

# Or install via npm
npm install n8n -g
n8n start
```

1. Open http://localhost:5678
2. Import `n8n-workflow.json` from this project
3. Configure WhatsApp Business API credentials
4. Set webhook in Twilio to n8n endpoint instead of Flask
5. Activate workflow for enhanced features

📖 **Detailed Setup**: See [`QUICK_START.md`](QUICK_START.md) for complete n8n integration guide.

---

## 🚀 Deploy (Example: Railway)

```bash
# Ensure you have a Git repo
git init
git add .
git commit -m "Student Support WhatsApp Bot"
git push origin main

# Deploy to Railway (connects to GitHub automatically)
# Visit https://railway.app and connect your repository
```

Then set your WhatsApp webhook in Twilio to your deployed URL:
```
https://your-app.up.railway.app/whatsapp
```

---

## 🔧 Manual Webhook Test (without Twilio)

You can test all student support features using curl:

**Test Main Menu:**
```bash
curl -X POST http://localhost:5001/whatsapp --data-urlencode "Body=hi"
```

**Test FAQ Categories:**
```bash
curl -X POST http://localhost:5001/whatsapp --data-urlencode "Body=courses"
curl -X POST http://localhost:5001/whatsapp --data-urlencode "Body=fees"
curl -X POST http://localhost:5001/whatsapp --data-urlencode "Body=library"
```

**Test Academic Resources:**
```bash
curl -X POST http://localhost:5001/whatsapp --data-urlencode "Body=resources"
curl -X POST http://localhost:5001/whatsapp --data-urlencode "Body=notes"
curl -X POST http://localhost:5001/whatsapp --data-urlencode "Body=syllabus"
```

**Test Personalized Updates:**
```bash
curl -X POST http://localhost:5001/whatsapp --data-urlencode "Body=updates"
curl -X POST http://localhost:5001/whatsapp --data-urlencode "Body=timetable"
curl -X POST http://localhost:5001/whatsapp --data-urlencode "Body=assignments"
```

---

## 🔄 Next Steps / Enhancements

### **Immediate Improvements**
- **Database Integration**: Store student data persistently (MySQL/PostgreSQL/MongoDB)
- **User Authentication**: Add student ID verification system
- **Enhanced Resources**: PDF downloads, video streaming capabilities
- **Search Functionality**: Allow students to search through resources

### **Advanced Features**
- **AI Integration**: Natural language processing for better query understanding
- **Multi-language Support**: Support for regional languages
- **Rich Media**: Image, document, and video sharing capabilities
- **Analytics Dashboard**: Track popular queries and user engagement

### **Integration Options**
- **LMS Integration**: Connect with existing Learning Management Systems
- **Student Portal**: Sync with existing student information systems
- **Notification System**: Scheduled reminders and announcements
- **Mobile App**: Dedicated companion app with WhatsApp integration
- **n8n Workflow Enhancement**: Advanced automation with analytics and multi-channel support

### **n8n Workflow Files**
- 🔄 **[n8n-workflow.json](n8n-workflow.json)**: Complete workflow configuration
- 📖 **[N8N_SETUP.md](N8N_SETUP.md)**: Comprehensive setup and configuration guide
- ⚡ **[QUICK_START.md](QUICK_START.md)**: 5-minute quick start guide
- 📈 **[WORKFLOW_ARCHITECTURE.md](WORKFLOW_ARCHITECTURE.md)**: Visual diagrams and architecture

---

## 📞 Support & Contact

For technical support or questions about the Student Support Bot:
- **Email**: support@example.com
- **Issues**: Create a GitHub issue for bug reports
- **Documentation**: Refer to code comments and this README

---

## 📋 License

MIT License - free to use for educational institutions and commercial purposes.

---

**Built with ❤️ for Students**

*Enhancing student experience through intelligent WhatsApp automation.*