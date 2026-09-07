"""
=============================================================================
PatientCare AI - Backend Server (SIH 2026 - Problem Statement #47)
AI-Assisted Intelligent Patient Case-Taking System
-----------------------------------------------------------------------------
Built for 1st Year Engineering Students:
- Uses ONLY Python built-in standard libraries (http.server, json, sqlite3, os)
- NO pip install or heavy frameworks required!
- Run simply with: python server.py
=============================================================================
"""

import http.server
import socketserver
import json
import sqlite3
import os
import urllib.parse
import mimetypes
from datetime import datetime

# Production & Deployment configuration
STATIC_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FILE = os.path.join(STATIC_DIR, "patientcare.db")
PORT = int(os.environ.get("PORT", 5000))
HOST = "0.0.0.0"

# Explicitly ensure correct MIME types for frontend assets
mimetypes.add_type("text/css", ".css")
mimetypes.add_type("application/javascript", ".js")
mimetypes.add_type("text/html", ".html")

def init_db():
    """Initializes the SQLite database with initial demo cases if empty."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # Create cases table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS patient_cases (
            id TEXT PRIMARY KEY,
            patient_name TEXT,
            age INTEGER,
            gender TEXT,
            contact TEXT,
            language TEXT,
            chief_complaint TEXT,
            symptoms TEXT,
            hpi TEXT,
            past_history TEXT,
            medications TEXT,
            allergies TEXT,
            lifestyle TEXT,
            triage_level TEXT,
            contradictions TEXT,
            missing_gaps TEXT,
            doctor_status TEXT,
            doctor_notes TEXT,
            doctor_diagnosis TEXT,
            doctor_rx TEXT,
            verified_by TEXT,
            verified_at TEXT,
            uploaded_document_name TEXT,
            uploaded_document_data TEXT,
            conversation_transcript TEXT,
            created_at TEXT
        )
    """)
    
    # In case table already existed, ensure columns are added
    try:
        cursor.execute("ALTER TABLE patient_cases ADD COLUMN uploaded_document_name TEXT")
    except Exception:
        pass
    try:
        cursor.execute("ALTER TABLE patient_cases ADD COLUMN uploaded_document_data TEXT")
    except Exception:
        pass

    conn.commit()

    # Insert default realistic demo cases if table is empty
    cursor.execute("SELECT COUNT(*) FROM patient_cases")
    count = cursor.fetchone()[0]
    
    if count == 0:
        demo_cases = [
            (
                "CAS-2026-001",
                "Rajesh Kumar",
                52,
                "Male",
                "+91 98765 43210",
                "Hindi / English",
                "Severe central chest tightness with breathlessness",
                "Substernal chest pressure, radiating to left arm, sweating, mild shortness of breath on exertion",
                "Symptoms started 3 hours ago during brisk walk. Pain is 8/10, crushing type. Aggravated by walking, relieved partially by rest.",
                "Hypertension diagnosed 4 years ago. Denies prior heart attacks or surgeries.",
                "Amlodipine 5mg OD, Aspirin 75mg (irregularly taken)",
                "No known drug allergies (NKDA)",
                "Non-smoker, moderate tea/coffee intake, sedentary work",
                "Emergency / High",
                json.dumps([
                    {
                        "severity": "high",
                        "title": "Medication Inconsistency",
                        "desc": "Patient reported taking Aspirin irregularly despite documented cardiac risk and hypertension."
                    }
                ]),
                json.dumps([
                    {
                        "severity": "medium",
                        "title": "Missing Family History",
                        "desc": "Family history of premature coronary artery disease was not clarified."
                    }
                ]),
                "Pending Review",
                "",
                "",
                "",
                "",
                "",
                json.dumps([
                    {"sender": "ai", "text": "Namaste Rajesh ji. Welcome to PatientCare AI. In what language would you prefer to converse today?"},
                    {"sender": "patient", "text": "English or Hindi is fine. I am having severe chest pressure since 3 hours."},
                    {"sender": "ai", "text": "I understand this must be distressing. Does the pain stay in the center, or does it spread to your left arm, neck, or jaw?"},
                    {"sender": "patient", "text": "It goes down into my left arm and I feel sweaty."},
                    {"sender": "ai", "text": "Are you currently taking any daily medicines for blood pressure, sugar, or heart?"},
                    {"sender": "patient", "text": "I take Amlodipine for BP. Doctor told me Aspirin also, but I only take it sometimes."}
                ]),
                datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            ),
            (
                "CAS-2026-002",
                "Sunita Devi",
                38,
                "Female",
                "+91 94123 78901",
                "Hindi",
                "Severe upper abdominal burning with nausea",
                "Epigastric burning pain, acid regurgitation, loss of appetite for 4 days",
                "Continuous burning in upper stomach. Patient stated it worsens 1 hour after meals. Tried home remedies without relief.",
                "Patient initially stated 'No past illnesses'.",
                "Self-medicating with Ibuprofen 400mg twice daily for knee pain over the last 3 weeks.",
                "No known drug allergies",
                "Vegetarian, irregular meal timings, high stress",
                "Priority / Moderate",
                json.dumps([
                    {
                        "severity": "high",
                        "title": "Direct Clinical Contradiction Detected",
                        "desc": "Patient stated 'no past stomach issues' but has been taking daily NSAID (Ibuprofen) which causes gastric mucosal erosion and peptic ulcer symptoms."
                    }
                ]),
                json.dumps([
                    {
                        "severity": "low",
                        "title": "Missing Stool Color Detail",
                        "desc": "Needs verification if patient has black tarry stools (melena) indicating bleeding."
                    }
                ]),
                "Pending Review",
                "",
                "",
                "",
                "",
                "",
                json.dumps([
                    {"sender": "ai", "text": "Namaste Sunita ji. Please describe what trouble you are facing today."},
                    {"sender": "patient", "text": "Mere pet ke upar wale hisse me bohot jalan aur dard ho raha hai 4 dino se."},
                    {"sender": "ai", "text": "Kya aapko ulti ya khana khane ke baad dard badhta hai? Aur kya aap koi dawa le rahe hain?"},
                    {"sender": "patient", "text": "Khane ke baad jalan badhti hai. Main ghutne ke dard ke liye Ibuprofen roz le rahi thi pichle 3 hafte se."},
                    {"sender": "ai", "text": "Noted. Kya aapko pehle kabhi acidity ya ulcer ki samasya rahi hai?"},
                    {"sender": "patient", "text": "Nahi, pehle kabhi nahi hua."}
                ]),
                datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            ),
            (
                "CAS-2026-003",
                "Aarav Patel",
                8,
                "Male",
                "+91 97234 11223",
                "Gujarati / English",
                "Recurrent high grade fever with dry cough",
                "Fever up to 102.4 F for 2 days, dry hacking cough, decreased oral intake",
                "Fever started 48 hours ago. Mother recorded peak temperature in evenings. Mild runny nose, no breathing difficulty observed.",
                "Frequent seasonal allergies in winter.",
                "Paracetamol syrup given 6 hours ago with temporary temperature drop to 99.8 F.",
                "Mild skin rash with Amoxicillin in infancy",
                "School-going child, up to date with universal immunization",
                "Routine / Moderate",
                json.dumps([]),
                json.dumps([
                    {
                        "severity": "low",
                        "title": "Urine Output Check",
                        "desc": "Fluid intake status and diaper/urination frequency should be confirmed by doctor."
                    }
                ]),
                "Verified",
                "Mild viral upper respiratory tract infection. Paracetamol dosage adjusted according to weight.",
                "Viral Pharyngitis with Pyrexia",
                "1. Syp. Paracetamol 250mg/5ml - 5ml SOS for temp > 100°F\n2. Syp. Cetirizine 2.5ml at bedtime for 3 days\n3. ORS hydration and steam inhalation",
                "Dr. Priya Sharma (M.D. Pediatrics)",
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                json.dumps([
                    {"sender": "ai", "text": "Hello. I am here to help collect Aarav's health history for the doctor. How can I help?"},
                    {"sender": "patient", "text": "My son has had fever for 2 days, around 102 degrees, and a dry cough."},
                    {"sender": "ai", "text": "Does he have any difficulty breathing, wheezing, or rash on his body?"},
                    {"sender": "patient", "text": "No breathing issue. Paracetamol helped temporarily."},
                    {"sender": "ai", "text": "Does he have any known allergy to medicines?"},
                    {"sender": "patient", "text": "Yes, he got a small rash once with Amoxicillin antibiotic when he was a baby."}
                ]),
                datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            )
        ]
        
        cursor.executemany("""
            INSERT INTO patient_cases VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        """, demo_cases)
        conn.commit()

    conn.close()


class PatientCareHandler(http.server.SimpleHTTPRequestHandler):
    """Handles static files and REST API requests for PatientCare AI."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=STATIC_DIR, **kwargs)

    def _send_json(self, data, status_code=200):
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode("utf-8"))

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        # Avoid 404 log noise for browser favicon requests
        if path == "/favicon.ico":
            self.send_response(204)
            self.end_headers()
            return

        # API: Get all cases
        if path == "/api/cases":
            conn = sqlite3.connect(DB_FILE)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM patient_cases ORDER BY created_at DESC")
            rows = cursor.fetchall()
            cases = []
            for row in rows:
                c = dict(row)
                c["contradictions"] = json.loads(c["contradictions"] or "[]")
                c["missing_gaps"] = json.loads(c["missing_gaps"] or "[]")
                c["conversation_transcript"] = json.loads(c["conversation_transcript"] or "[]")
                cases.append(c)
            conn.close()
            self._send_json({"success": True, "cases": cases})
            return

        # API: Get single case by ID
        if path.startswith("/api/cases/"):
            case_id = path.split("/api/cases/")[1].split("/")[0]
            conn = sqlite3.connect(DB_FILE)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM patient_cases WHERE id = ?", (case_id,))
            row = cursor.fetchone()
            conn.close()
            if row:
                c = dict(row)
                c["contradictions"] = json.loads(c["contradictions"] or "[]")
                c["missing_gaps"] = json.loads(c["missing_gaps"] or "[]")
                c["conversation_transcript"] = json.loads(c["conversation_transcript"] or "[]")
                self._send_json({"success": True, "case": c})
            else:
                self._send_json({"success": False, "error": "Case not found"}, status_code=404)
            return

        # Serve static HTML/CSS/JS frontend
        super().do_GET()

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length).decode("utf-8") if content_length > 0 else "{}"
        try:
            payload = json.loads(body)
        except Exception:
            payload = {}

        # API: Create new patient case
        if path == "/api/cases":
            case_id = payload.get("id") or f"CAS-2026-{int(datetime.now().timestamp()) % 100000:05d}"
            conn = sqlite3.connect(DB_FILE)
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO patient_cases (
                    id, patient_name, age, gender, contact, language,
                    chief_complaint, symptoms, hpi, past_history, medications,
                    allergies, lifestyle, triage_level, contradictions, missing_gaps,
                    doctor_status, doctor_notes, doctor_diagnosis, doctor_rx,
                    verified_by, verified_at, uploaded_document_name, uploaded_document_data,
                    conversation_transcript, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                case_id,
                payload.get("patient_name", "Anonymous Patient"),
                int(payload.get("age", 30)),
                payload.get("gender", "Other"),
                payload.get("contact", ""),
                payload.get("language", "English"),
                payload.get("chief_complaint", "General Health Assessment"),
                payload.get("symptoms", ""),
                payload.get("hpi", ""),
                payload.get("past_history", "None reported"),
                payload.get("medications", "None reported"),
                payload.get("allergies", "None reported"),
                payload.get("lifestyle", "Normal"),
                payload.get("triage_level", "Routine"),
                json.dumps(payload.get("contradictions", [])),
                json.dumps(payload.get("missing_gaps", [])),
                payload.get("doctor_status", "Pending Review"),
                payload.get("doctor_notes", ""),
                payload.get("doctor_diagnosis", ""),
                payload.get("doctor_rx", ""),
                payload.get("verified_by", ""),
                payload.get("verified_at", ""),
                payload.get("uploaded_document_name", ""),
                payload.get("uploaded_document_data", ""),
                json.dumps(payload.get("conversation_transcript", [])),
                datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            ))
            conn.commit()
            conn.close()
            self._send_json({"success": True, "id": case_id, "message": "Case saved successfully"})
            return

        # API: Doctor verification
        if path.startswith("/api/cases/") and path.endswith("/verify"):
            case_id = path.split("/api/cases/")[1].replace("/verify", "")
            conn = sqlite3.connect(DB_FILE)
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE patient_cases
                SET doctor_status = 'Verified',
                    doctor_notes = ?,
                    doctor_diagnosis = ?,
                    doctor_rx = ?,
                    verified_by = ?,
                    verified_at = ?
                WHERE id = ?
            """, (
                payload.get("doctor_notes", ""),
                payload.get("doctor_diagnosis", ""),
                payload.get("doctor_rx", ""),
                payload.get("verified_by", "Dr. Priya Sharma, M.D."),
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                case_id
            ))
            conn.commit()
            conn.close()
            self._send_json({"success": True, "message": "Case verified by doctor successfully"})
            return

        # Fallback 404
        self._send_json({"success": False, "error": "Endpoint not found"}, status_code=404)

    def do_PUT(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        if path.startswith("/api/cases/"):
            case_id = path.split("/api/cases/")[1].split("/")[0]
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length).decode("utf-8") if content_length > 0 else "{}"
            payload = json.loads(body)

            conn = sqlite3.connect(DB_FILE)
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE patient_cases
                SET chief_complaint = coalesce(?, chief_complaint),
                    hpi = coalesce(?, hpi),
                    past_history = coalesce(?, past_history),
                    medications = coalesce(?, medications),
                    allergies = coalesce(?, allergies),
                    doctor_notes = coalesce(?, doctor_notes),
                    doctor_diagnosis = coalesce(?, doctor_diagnosis),
                    doctor_rx = coalesce(?, doctor_rx),
                    doctor_status = coalesce(?, doctor_status)
                WHERE id = ?
            """, (
                payload.get("chief_complaint"),
                payload.get("hpi"),
                payload.get("past_history"),
                payload.get("medications"),
                payload.get("allergies"),
                payload.get("doctor_notes"),
                payload.get("doctor_diagnosis"),
                payload.get("doctor_rx"),
                payload.get("doctor_status"),
                case_id
            ))
            conn.commit()
            conn.close()
            self._send_json({"success": True, "message": "Case updated successfully"})
            return

        self._send_json({"success": False, "error": "Endpoint not found"}, status_code=404)


if __name__ == "__main__":
    init_db()
    print("=" * 70)
    print("  PATIENTCARE AI - SIH 2026 PROTOTYPE SERVER (PRODUCTION READY)")
    print("  Problem Statement #47: Patient Case Tracking & Smart Intake")
    print("=" * 70)
    print(f"  -> Bound to: http://{HOST}:{PORT}")
    print(f"  -> Serving Directory: {STATIC_DIR}")
    print("  -> Press Ctrl + C to stop the server")
    print("=" * 70)
    
    # Multi-threaded server so multiple requests/tabs run smoothly
    class ThreadedHTTPServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
        daemon_threads = True
        allow_reuse_address = True

    with ThreadedHTTPServer((HOST, PORT), PatientCareHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server cleanly. Goodbye!")
