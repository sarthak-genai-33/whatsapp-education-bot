# WhatsApp Education Bot - System Flowchart

## Complete User Interaction Flow

```mermaid
flowchart TD
    A[User sends message to WhatsApp] --> B{Message Type?}
    
    B -->|Text Message| C[Extract message body]
    B -->|Voice Message| D[Download audio file]
    
    D --> E[Speech-to-Text conversion]
    E --> F[Process transcribed text]
    F --> C
    
    C --> G[Convert to lowercase & trim]
    G --> H{Is greeting?}
    
    H -->|Yes: hi, hello, hey| I[Show Main Menu]
    H -->|No| J{Check message content}
    
    I --> K[Display 7 Service Categories]
    K --> L[Wait for user selection]
    
    J -->|1 or 'student'| M[Student Support & FAQs]
    J -->|2 or 'admissions'| N[Admissions & Enrollment]
    J -->|3 or 'attendance'| O[Attendance & Performance]
    J -->|4 or 'exams'| P[Exams & Assessments]
    J -->|5 or 'fees'| Q[Fee Management]
    J -->|6 or 'parent'| R[Parent-Teacher Communication]
    J -->|7 or 'learning'| S[EdTech & Learning Support]
    J -->|Unknown| T[Fallback Message]
    
    M --> M1{Sub-option?}
    M1 -->|library| M2[Library Hours & Info]
    M1 -->|hostel| M3[Accommodation Details]
    M1 -->|transport| M4[Bus Routes & Timings]
    M1 -->|placement| M5[Career & Placement Info]
    M1 -->|syllabus| M6[Course Materials]
    M1 -->|notes| M7[Study Resources]
    
    N --> N1{Sub-option?}
    N1 -->|mba/bca/bba| N2[Program Details]
    N1 -->|brochure| N3[Send Brochure]
    N1 -->|status| N4[Application Status]
    
    O --> O1{Sub-option?}
    O1 -->|absent| O2[Report Absence]
    O1 -->|report| O3[Progress Report]
    O1 -->|tips| O4[Improvement Tips]
    
    P --> P1{Sub-option?}
    P1 -->|register| P2[Exam Registration]
    P1 -->|results| P3[Check Results]
    P1 -->|reminder| P4[Set Reminders]
    
    Q --> Q1{Sub-option?}
    Q1 -->|paynow| Q2[Online Payment]
    Q1 -->|installment| Q3[EMI Options]
    Q1 -->|receipt| Q4[Payment History]
    Q1 -->|breakdown| Q5[Fee Structure]
    
    R --> R1{Sub-option?}
    R1 -->|ptm| R2[PTM Details]
    R1 -->|homework| R3[Assignments]
    R1 -->|feedback| R4[Share Feedback]
    
    S --> S1{Sub-option?}
    S1 -->|module| S2[Learning Module]
    S1 -->|quiz| S3[Interactive Quiz]
    S1 -->|doubt| S4[AI Q&A]
    S1 -->|videos| S5[Video Library]
    
    M2 --> U[Generate Text Response]
    M3 --> U
    M4 --> U
    M5 --> U
    M6 --> U
    M7 --> U
    N2 --> U
    N3 --> U
    N4 --> U
    O2 --> U
    O3 --> U
    O4 --> U
    P2 --> U
    P3 --> U
    P4 --> U
    Q2 --> U
    Q3 --> U
    Q4 --> U
    Q5 --> U
    R2 --> U
    R3 --> U
    R4 --> U
    S2 --> U
    S3 --> U
    S4 --> U
    S5 --> U
    T --> U
    
    U --> V{Voice Enabled?}
    V -->|Yes| W[Generate Voice Response]
    V -->|No| X[Send Text Response]
    
    W --> Y[Clean text for TTS]
    Y --> Z[Convert to Speech]
    Z --> AA[Send Voice + Text]
    
    X --> BB[Create TwiML Response]
    AA --> BB
    
    BB --> CC[Send to Twilio]
    CC --> DD[Deliver to User via WhatsApp]
    
    DD --> EE[Wait for next message]
    EE --> A
```

## System Architecture Flow

```mermaid
flowchart LR
    A[WhatsApp User] -->|Sends Message| B[Twilio WhatsApp API]
    B -->|Webhook POST| C[Flask Application]
    
    C --> D[Message Processor]
    D --> E{Message Type}
    
    E -->|Text| F[Text Handler]
    E -->|Voice| G[Voice Processor]
    
    G --> H[Speech Recognition]
    H --> I[Google Speech API]
    I --> J[Transcribed Text]
    J --> F
    
    F --> K[Command Matcher]
    K --> L[Response Generator]
    
    L --> M{Voice Response?}
    M -->|Yes| N[Text-to-Speech]
    M -->|No| O[Text Response]
    
    N --> P[Google TTS API]
    P --> Q[Audio Generation]
    Q --> R[TwiML Response]
    
    O --> R
    R --> S[Twilio API]
    S --> T[WhatsApp Delivery]
    T --> A
```

## Deployment Flow

```mermaid
flowchart TD
    A[Developer] -->|git push| B[GitHub Repository]
    B --> C{Branch?}
    
    C -->|main| D[Railway Deployment]
    C -->|voice-bot-feature| E[Feature Branch]
    
    D --> F[Build Process]
    F --> G[Install Dependencies]
    G --> H[Start Gunicorn Server]
    H --> I[Production App]
    
    I --> J[Health Endpoints]
    I --> K[WhatsApp Webhook]
    I --> L[Voice API Endpoints]
    
    E --> M[Pull Request]
    M --> N[Code Review]
    N --> O[Merge to Main]
    O --> D
```