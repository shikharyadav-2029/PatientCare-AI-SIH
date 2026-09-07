# PatientCare AI — SIH 2026 Internal Prototype
**Smart India Hackathon 2026 | Problem Statement #47: Patient Case Tracking**
*Sub-theme: AI-Assisted Intelligent Patient Case-Taking System*

---

## 🌟 What's New in this Version

Based on your requirements, the application has been updated with:
1. **Opens with Patient Registration & Language Selection**:
   - The opening screen is a clean, friendly Patient Registration Card.
   - Choose language upfront in native script: **English, हिन्दी (Hindi), தமிழ் (Tamil), తెలుగు (Telugu), বাংলা (Bengali), मराठी (Marathi), ગુજરાતી (Gujarati)**.
   - Demographics (Name, Age, Gender, Mobile Number).
2. **Accessible Pointer Questions (No Long Describing)**:
   - Instead of typing long essays, questions are presented as clean **pointers** with **Big YES 👍 / NO 👎 buttons**:
     - *Pointer 1*: Visual symptom selector (🫀 Chest Pain, 🤰 Stomach Burning, 🌡️ Fever & Cough, 🤕 Headache, etc.)
     - *Pointer 2*: Duration (< 24 Hours, 2-4 Days, 1-2 Weeks, > 1 Month)
     - *Pointer 3*: *"Are you a Sugar (Diabetes) patient?"* ➔ **[ 👍 YES ] [ 👎 NO ]**
     - *Pointer 4*: *"Do you have High Blood Pressure (BP)?"* ➔ **[ 👍 YES ] [ 👎 NO ]**
     - *Pointer 5*: *"Are you taking daily medicines or pain relief pills?"* ➔ **[ 👍 YES ] [ 👎 NO ]**
     - *Pointer 6*: *"Do you have any drug allergy?"* ➔ **[ 👍 YES ] [ 👎 NO ]**
3. **Features Built for Illiterate / Rural Patients**:
   - 🔊 **Voice Read-Aloud (Text-to-Speech)**: An audio speaker button next to every question reads aloud the question in the patient's mother tongue.
   - 🖼️ **Large Visual Icons**: High-contrast, recognizable medical emojis & icons for quick recognition without reading.
   - 🎙️ **Voice Speech-to-Text**: Illiterate patients can tap the big microphone button and speak their answers.
   - 👍 / 👎 **Clear Color Cues**: Green (Thumbs Up / Yes) and Red (Thumbs Down / No).
4. **Doctor Login & Clinical Review**:
   - Direct **"👨‍⚕️ Doctor Login"** button in top right header.
   - Quick 1-click demo login for hackathon presentation (`dr.sharma@hospital.in` / `admin123`).
   - Side-by-side verification, contradiction alerts, editable clinical notes, and PDF print sheet.

---

## 🚀 How to Open and Run

### Link 1: Local Server
👉 **http://localhost:5000**  
*(Server is running live in the background).*

### Link 2: Direct Double-Click
👉 Double-click **`index.html`** in Windows Explorer. Works 100% offline with browser local storage!

---

## 🎤 How to Present to the SIH Judges

1. **Step 1: The Registration & Language Choice**
   - *"Notice our prototype opens with an inclusive registration screen supporting 7 regional languages. For rural and illiterate patients, we provide an Assisted Voice Mode."*
2. **Step 2: Pointer Questions & Voice Assistance**
   - *"Instead of asking patients to write complex medical terms, we ask structured pointer questions. Notice how each question can be read aloud in Hindi or vernacular language by clicking the speaker 🔊 button. Patients simply tap big Yes 👍 or No 👎 buttons."*
3. **Step 3: Real-Time Contradiction Detection**
   - *"When a patient with stomach burning clicks 'YES' to taking daily painkillers like Ibuprofen, our AI immediately triggers a clinical contradiction flag: NSAID-induced peptic ulcer risk!"*
4. **Step 4: Doctor Login & Sign-off**
   - *"Click 'Doctor Login' at the top. The doctor inspects the case, reviews the contradiction, enters diagnosis/prescription, and signs off with a digital verification badge."*
