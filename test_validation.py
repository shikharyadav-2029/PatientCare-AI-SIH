import urllib.request
import json
import os

BASE_URL = os.environ.get("BASE_URL", f"http://localhost:{os.environ.get('PORT', 5000)}")

def test_full_pipeline():
    # 1. Fetch existing cases
    req = urllib.request.urlopen(f"{BASE_URL}/api/cases")
    data = json.loads(req.read().decode("utf-8"))
    assert data["success"] is True
    initial_count = len(data["cases"])
    print(f"Step 1: Loaded {initial_count} patient cases from SQLite database.")

    # 2. Add new patient case from conversational intake
    test_id = "CAS-2026-TEST"
    new_patient_payload = {
        "id": test_id,
        "patient_name": "Rohan Gupta",
        "age": 42,
        "gender": "Male",
        "contact": "+91 98111 22334",
        "language": "Hindi / English",
        "chief_complaint": "Acute epigastric burning after meal",
        "symptoms": "Upper stomach burn, acidity",
        "hpi": "Pain started 2 hours ago after taking painkiller for headache.",
        "past_history": "No known previous chronic conditions",
        "medications": "Took Ibuprofen 400mg without food",
        "allergies": "None",
        "lifestyle": "Sedentary desk job",
        "triage_level": "Priority / Moderate",
        "contradictions": [
            {
                "severity": "high",
                "title": "NSAID Gastric Irritation Contradiction",
                "desc": "Patient took Ibuprofen on empty stomach leading to acute gastritis."
            }
        ],
        "missing_gaps": [],
        "conversation_transcript": [
            {"sender": "patient", "text": "I have sudden burning in upper abdomen."},
            {"sender": "ai", "text": "Did you take any pain medicine or have food?"}
        ]
    }

    req_post = urllib.request.Request(
        f"{BASE_URL}/api/cases",
        data=json.dumps(new_patient_payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    res_post = json.loads(urllib.request.urlopen(req_post).read().decode("utf-8"))
    assert res_post["success"] is True
    print(f"Step 2: Successfully created patient case {test_id} via intake API.")

    # 3. Doctor reviews, adds prescription and signs off
    verify_payload = {
        "doctor_diagnosis": "Acute Drug-Induced Gastritis",
        "doctor_rx": "1. Tab Pantoprazole 40mg OD Before Food\n2. Syp. Mucaine Gel 10ml TDS\n3. Discontinue Ibuprofen",
        "doctor_notes": "Advised lifestyle modifications and avoiding NSAIDs on empty stomach.",
        "verified_by": "Dr. Priya Sharma, M.D. (Internal Medicine)"
    }
    req_verify = urllib.request.Request(
        f"{BASE_URL}/api/cases/{test_id}/verify",
        data=json.dumps(verify_payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    res_verify = json.loads(urllib.request.urlopen(req_verify).read().decode("utf-8"))
    assert res_verify["success"] is True
    print(f"Step 3: Doctor verification completed with digital sign-off.")

    # 4. Fetch the verified case back and assert fields
    req_check = urllib.request.urlopen(f"{BASE_URL}/api/cases/{test_id}")
    case_verified = json.loads(req_check.read().decode("utf-8"))["case"]
    assert case_verified["doctor_status"] == "Verified"
    assert "Priya Sharma" in case_verified["verified_by"]
    assert len(case_verified["contradictions"]) == 1
    print(f"Step 4: Final clinical record verified: Status='{case_verified['doctor_status']}' | Sign-off='{case_verified['verified_by']}'")

    print("\nSUCCESS: All clinical intake, contradiction detection & doctor verification tests PASSED!")

if __name__ == "__main__":
    test_full_pipeline()
