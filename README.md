# WhatsApp Education Voice Bot (Comprehensive)

A comprehensive **Voice-Enabled** WhatsApp bot for the Education domain using **Python (Flask)**, **Twilio's WhatsApp API**, and **Speech Processing**.
Covers all 7 major educational use cases with **Speech-to-Text** and **Text-to-Speech** capabilities.

---

## 🎤 **Voice Features**

### **🔊 Voice Input Processing**
- **Speech Recognition**: Converts voice messages to text using Google Speech API
- **Multi-language Support**: English (US/India) with intelligent fallback
- **Command Matching**: Smart matching of voice commands to bot functions
- **Noise Handling**: Automatic ambient noise adjustment

### **🎵 Voice Output Generation**
- **Text-to-Speech**: Converts bot responses to natural voice
- **Clean Audio**: Emoji and formatting removal for better TTS
- **Multiple Formats**: MP3 audio generation and streaming
- **Voice Confirmation**: Transcription confirmation for accuracy

### **🎯 Voice Commands**
- Say **"Hello"** or **"Hi"** → Voice welcome message
- Say **"Menu"** or **"Options"** → Voice menu navigation
- Say **"Fees"** or **"Payment"** → Fee management via voice
- Say **"Exams"** or **"Tests"** → Exam information via voice
- Say **"One"** to **"Seven"** → Navigate main service categories
- Send voice messages → Automatic transcription and processing

---

## 🚀 Features

### 1. **Student Engagement & Support**
- ❓ Answer FAQs about courses, fees, admission process, results, schedules
- 📱 Share personalized updates (exam timetables, class reminders, assignment deadlines)
- 📚 Provide instant academic resources (syllabus, notes, recorded lectures, e-books)
- 🏠 Campus facilities info (library, hostel, transport, placement)

### 2. **Admissions & Enrollments**
- 🔄 Automate inquiries from prospective students
- 📋 Collect basic details via conversational forms
- 📄 Send brochures, admission guidelines, and application links
- ⏰ Provide real-time status updates on applications

### 3. **Attendance & Performance Tracking**
- ⚠️ Auto-reminders to parents if student is absent
- 📊 Share progress reports directly over WhatsApp
- 💡 Send personalized tips to improve weak subjects
- 📈 Track attendance percentage and academic performance

### 4. **Exams & Assessments**
- 📅 Push exam schedules and venue details
- ✅ Allow students to register for exams via bot
- 🎓 Share results securely after verification
- 🔔 Set automatic exam reminders

### 5. **Fee Management**
- 💰 Automated fee reminders and digital payment links
- 🧾 Payment receipts shared instantly on WhatsApp
- 📊 Fee structure breakdown and EMI options
- 🔄 Auto-payment setup for convenience

### 6. **Teacher & Parent Communication**
- 📞 Parent-teacher meeting notifications
- 📢 Teachers can broadcast homework updates to parents
- 💬 Quick feedback collection after sessions/events
- 📅 Schedule meetings and send confirmations

### 7. **EdTech & Learning Support**
- 🎯 Micro-learning modules delivered daily (5-min lessons)
- 🧠 Quiz-based assessments via WhatsApp
- 🤖 AI-driven doubt resolution (basic Q&A, linking to resources)
- 📹 Access to recorded lecture library

---

## 💻 Tech Stack
- **Backend**: Python 3.9+, Flask 3.0.3
- **Messaging**: Twilio WhatsApp API (9.3.5)
- **Voice Processing**: Google Speech Recognition, gTTS (Google Text-to-Speech)
- **Audio Processing**: PyDub, SpeechRecognition
- **Deployment**: Gunicorn 22.0.0, Railway/Heroku compatible
- **Data**: In-memory structures (easily extensible to databases)
- **Features**: Real-time messaging, Voice I/O, Rich media support, Interactive menus

---

## 💬 Example Conversation Flows

### **Student Inquiry:**
```
Student: "What is the last date for MBA admissions?"
Bot: "Admissions for MBA close on 10th Sept 2025. Would you like me to share the brochure or application link?"
```

### **Parent Communication:**
```
Parent: "When is the parent-teacher meeting?"
Bot: "The next PTM for Class 9 is scheduled on 25th Aug 2025 at 10 AM in the school auditorium."
```

### **Fee Payment:**
```
Student: "Can I pay my fees here?"
Bot: "Yes, you can. Please click the link below to complete payment: [Pay Now]. A receipt will be sent once done ✅"
```

### **Interactive Learning:**
```
Student: "Start quiz"
Bot: "🧠 Quick Quiz - Photosynthesis
❓ What gas do plants release during photosynthesis?
A) Carbon dioxide B) Oxygen C) Nitrogen D) Hydrogen
💡 Reply with A, B, C, or D"
```

---

## 🏆 Benefits
- **24x7 availability** for students & parents
- **Reduced admin workload** (less phone calls, fewer emails)
- **Increased enrollment & retention** via instant communication
- **Improved transparency** between institute, students, and parents
- **Enhanced learning experience** with interactive features
- **Cost-effective** compared to full mobile app development

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
   - Send `hi` to see the comprehensive menu
   - Send `1-7` for main service categories
   - Try keywords like `fees`, `exams`, `admissions`, `quiz`, etc.
   - Explore sub-features like `paynow`, `homework`, `module`, etc.

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

You can simulate Twilio's webhook (test all features) using curl:

**Test Main Menu:**
```bash
curl -X POST http://localhost:5001/whatsapp --data-urlencode "Body=hi"
```

**Test Student Support:**
```bash
curl -X POST http://localhost:5001/whatsapp --data-urlencode "Body=1"
```

**Test Fee Management:**
```bash
curl -X POST http://localhost:5001/whatsapp --data-urlencode "Body=fees"
```

**Test EdTech Features:**
```bash
curl -X POST http://localhost:5001/whatsapp --data-urlencode "Body=quiz"
```

**Test Voice Features:**
```bash
# Test voice generation
curl -X GET http://localhost:5001/test-voice

# Check voice system status
curl -X GET http://localhost:5001/voice-status

# Generate custom voice response
curl -X POST http://localhost:5001/voice-response \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello, this is a test voice message"}'
```

**Test Voice Messages:**
```bash
# Test voice message processing (simulated)
curl -X POST http://localhost:5001/whatsapp \
  --data-urlencode "Body=hi" \
  --data-urlencode "MediaUrl0=https://example.com/voice.ogg" \
  --data-urlencode "MediaContentType0=audio/ogg" \
  -H "Content-Type: application/x-www-form-urlencoded"
```

---

## Next Steps / Enhancements
- **Database Integration**: Persist sessions & user profiles (MySQL/PostgreSQL/MongoDB)
- **Authentication**: Add user verification and role-based access
- **AI Integration**: Advanced natural language processing with OpenAI/Dialogflow
- **LMS Integration**: Connect with existing Learning Management Systems
- **Analytics**: Track user engagement and conversation analytics
- **Multi-language Support**: Support for regional languages
- **Voice Messages**: Handle audio messages and voice-to-text
- **Rich Media**: Image, video, and document sharing capabilities
- **Notification System**: Scheduled reminders and push notifications
- **Admin Dashboard**: Web interface for managing bot responses and data