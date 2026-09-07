# -*- coding: utf-8 -*-
content = r'''/**
 * ==============================================================================
 * PatientCare AI - Frontend Controller (SIH 2026 Problem Statement #47)
 * AI-Assisted Intelligent Patient Case-Taking System
 * ------------------------------------------------------------------------------
 * Features:
 * 1. Full UI Multilingual Localization (7 Languages: EN, HI, TA, TE, BN, MR, GU)
 * 2. 11-Step Clinical Pointer Flow with Big Yes/No & Visual Touch Cards
 * 3. Doctor Review, Contradiction Engine & Digital Sign-off
 * 4. Real-time Doctor-to-Patient Live Verification & Digital Prescription
 * 5. Audio Voice Narration (TTS/STT) for Illiterate / Rural Patients
 * ==============================================================================
 */

// Application State
let currentRole = "patient";
let currentLanguage = "en";
let isAudioAssistanceOn = true;
let activeCase = null;
let allCases = [];
let recognition = null;
let isRecording = false;
let thankYouCountdownTimer = null;
let waitingCaseId = null;
let statusPollingInterval = null;

// Cross-tab / In-page Communication Channel
const patientCareChannel = ("BroadcastChannel" in window) ? new BroadcastChannel("patientcare_sync") : null;

// Current Registered Patient
let activePatient = {
  name: "Ramesh Verma",
  age: 48,
  gender: "Male",
  phone: "+91 98765 43210",
  language: "hi",
  mode: "assisted"
};

// 11 Comprehensive Clinical Intake Steps
let currentPointerStep = 1;
const TOTAL_POINTER_STEPS = 11;

let intakeAnswers = {
  symptom: "",
  symptom_icon: "",
  triage: "Routine",
  intensity: "",
  character: "",
  duration: "",
  clinical_followup: "",
  clinical_followup_val: null,
  clinical_followup2: "",
  clinical_followup2_val: null,
  is_sugar_patient: null,
  is_bp_patient: null,
  has_documents: false,
  doc_name: "",
  doc_data: "",
  is_daily_meds: null,
  meds_detail: "",
  is_allergic: null,
  allergy_detail: "",
  family_lifestyle: null
};

let detectedContradictions = [];
let patientTranscriptLog = [];

// ==============================================================================
// COMPREHENSIVE MULTILINGUAL UI DICTIONARY (7 REGIONAL LANGUAGES)
// ==============================================================================
const UI_TRANSLATIONS = {
  en: {
    tagline: "Problem Statement #47 • Smart India Hackathon 2026",
    voiceOn: "Voice Assistance: <strong>ON</strong>",
    voiceOff: "Voice Assistance: <strong>OFF</strong>",
    docLogin: "👨‍⚕️ Doctor Login / Portal",
    trackCase: "🔍 Track Case / Status",
    regTitle: "📋 Patient Registration & Language Selection",
    regSub: "Please fill your basic details to start clinical health intake",
    chooseLang: "🌐 Choose Your Preferred Language:",
    demoPresets: "⚡ Quick Demo Presets:",
    presetCardiac: "🫀 Cardiac Patient (Rajesh, 52)",
    presetGastric: "🔥 Gastric Contradiction (Sunita, 38)",
    presetPediatric: "👶 Pediatric Case (Aarav, 8)",
    nameLabel: "👤 Full Name / Patient Name *",
    namePlaceholder: "e.g. Ramesh Verma",
    ageLabel: "🎂 Age (Years) *",
    genderLabel: "⚧ Gender *",
    genderMale: "Male",
    genderFemale: "Female",
    genderOther: "Other",
    phoneLabel: "📱 Mobile Number",
    assistLabel: "♿ Patient Assistance Mode",
    assistVoice: "Illiterate / Voice & Visual Icon Mode (Assisted)",
    assistStandard: "Standard Digital Intake",
    startIntakeBtn: "🚀 Start Clinical Health Intake ➔",
    editReg: "✏️ Edit Registration",
    stepProgress: "Step {step} of 11",
    listenBtn: "🔊 Listen / Read Aloud",
    tapToSpeak: "🎙️ Tap to Speak",
    listeningWait: "Listening... Speak in your language",
    contradictionTitle: "⚠️ Real-Time Contradiction Detection",
    contradictionHint: "AI analyzes each pointer answer to flag contradictory history or unsafe medicine combinations...",
    caseSheetTitle: "📋 Auto Structured Case History",
    lblCC: "Chief Complaint & Nature",
    lblDuration: "Severity & Duration",
    lblSigns: "Clinical Follow-up Signs",
    lblPast: "Past History (Sugar & BP)",
    lblDocs: "Lab Reports / Documents",
    lblMeds: "Daily Medicines / Painkillers",
    lblAllergy: "Known Drug Allergies",
    lblLifestyle: "Lifestyle / Family History",
    valWaitingSymptom: "Waiting for symptom selection...",
    valNotAnswered: "Not answered yet",
    valNoneReported: "None reported",
    valNegative: "Negative / None",
    valNoDocs: "No documents attached (Optional)",
    valNone: "None",
    valStandard: "Standard / Non-contributory",
    submitCaseBtn: "🚀 Submit Case for Doctor Review",
    submitNotice: "Case is encrypted & transmitted directly to Doctor's triage queue.",
    thankYouTitle: "Thank You",
    thankYouSub: "Your clinical health case has been registered successfully.",
    tokenLabel: "🎫 TOKEN ID:",
    waitHeading: "Please Wait Till Your Call",
    waitMsg: "A doctor will attend to you shortly. You will be called by your token number.",
    redirectMsg: "Returning to New Patient Registration in",
    nextPatientBtn: "➕ Register Next Patient Now",
    spokenThankYou: "Thank you. Your registration is complete. Please wait until your call. A doctor will attend to you shortly.",
    spokenVerified: "Your case has been digitally verified by the doctor. Your prescription is ready.",
    verifiedBadge: "VERIFIED BY DOCTOR",
    verifiedTitle: "🎉 Case Digitally Verified & Signed-Off!",
    docDiagnosisLabel: "🩺 Doctor's Confirmed Diagnosis:",
    docRxLabel: "💊 Doctor's Prescription (Rx):",
    docAdviceLabel: "📝 Doctor's Clinical Advice & Notes:",
    printRxBtn: "🖨️ View & Print Official Prescription",
    waitingInQueue: "⏳ Waiting in Doctor's Queue...",
    trackModalTitle: "Track Patient Case & Prescription",
    searchBtn: "Search",
    symptomChest: "Chest Pain / Pressure",
    symptomChestSub: "Severe heaviness, crushing or tightness",
    symptomStomach: "Stomach Burning / Acid",
    symptomStomachSub: "Acidity, burning, nausea or upper pain",
    symptomFever: "High Fever & Cough",
    symptomFeverSub: "Chills, cold, phlegm or body temperature",
    symptomHeadache: "Severe Headache & Vertigo",
    symptomHeadacheSub: "Migraine, throbbing pain or dizziness",
    symptomJoint: "Joint & Bone Pain",
    symptomJointSub: "Knees, stiffness, back or joint ache",
    symptomOther: "General Illness / Other",
    symptomOtherSub: "Other physical discomfort or symptoms",
    mildIntensity: "Mild (1 to 3)",
    modIntensity: "Moderate (4 to 6)",
    sevIntensity: "Severe (7 to 10)",
    charHeavy: "Heavy / Crushing",
    charHeavySub: "Heavy weight or pressure",
    charBurning: "Burning / Acidic",
    charBurningSub: "Fire-like burning sensation",
    charSharp: "Sharp / Stabbing",
    charSharpSub: "Piercing needle-like pain",
    charDull: "Dull Continuous Ache",
    charDullSub: "Constant mild background pain",
    durToday: "Just Today (< 24 Hours)",
    durTodaySub: "Started today or few hours ago",
    durDays: "2 to 4 Days",
    durDaysSub: "Continuous for a few days",
    durWeeks: "1 to 2 Weeks",
    durWeeksSub: "Persisting for one or two weeks",
    durMonth: "More than 1 Month",
    durMonthSub: "Long standing chronic problem",
    yesText: "YES",
    noText: "NO",
    yesSub: "Yes, I have / Affirmative",
    noSub: "No, I do not / Negative",
    skipDocBtn: "⏭️ Skip - I don't have reports right now",
    uploadDocTitle: "Click or Tap to Upload Lab Report / Prescription / ECG (Optional)",
    uploadDocSub: "Supported formats: Images (JPG, PNG) or PDF up to 10MB"
  },
  hi: {
    tagline: "समस्या विवरण #47 • स्मार्ट इंडिया हैकथॉन 2026",
    voiceOn: "आवाज़ सहायता: <strong>चालू</strong>",
    voiceOff: "आवाज़ सहायता: <strong>बंद</strong>",
    docLogin: "👨‍⚕️ डॉक्टर लॉगिन / पोर्टल",
    trackCase: "🔍 टोकन / केस स्थिति देखें",
    regTitle: "📋 मरीज पंजीकरण एवं भाषा चयन",
    regSub: "स्वास्थ्य जांच शुरू करने के लिए कृपया अपनी सामान्य जानकारी भरें",
    chooseLang: "🌐 अपनी पसंदीदा भाषा चुनें:",
    demoPresets: "⚡ तुरंत डेमो प्रोफाइल (क्लिक करके भरें):",
    presetCardiac: "🫀 हृदय रोगी (राजेश, 52)",
    presetGastric: "🔥 पेट की जलन व पेनकिलर (सुनीता, 38)",
    presetPediatric: "👶 बाल बुखार (आरव, 8)",
    nameLabel: "👤 मरीज का पूरा नाम *",
    namePlaceholder: "उदा. रमेश वर्मा",
    ageLabel: "🎂 उम्र (वर्ष) *",
    genderLabel: "⚧ लिंग *",
    genderMale: "पुरुष (Male)",
    genderFemale: "महिला (Female)",
    genderOther: "अन्य (Other)",
    phoneLabel: "📱 मोबाइल नंबर",
    assistLabel: "♿ मरीज सहायता मोड",
    assistVoice: "सहायक वॉयस मोड (ग्रामीण / निरक्षर - बड़े चित्र + स्वतः आवाज़)",
    assistStandard: "सामान्य डिजिटल मोड",
    startIntakeBtn: "🚀 स्वास्थ्य जांच शुरू करें ➔",
    editReg: "✏️ पंजीकरण बदलें",
    stepProgress: "चरण {step} / 11",
    listenBtn: "🔊 सवाल सुनें",
    tapToSpeak: "🎙️ बोलकर बताएं",
    listeningWait: "सुन रहे हैं... अपनी भाषा में बोलें",
    contradictionTitle: "⚠️ लाइव मेडिकल विरोधाभास पहचान",
    contradictionHint: "एआई हर उत्तर की जांच करके विरोधाभासी दवा या खतरनाक स्थिति की पहचान करता है...",
    caseSheetTitle: "📋 स्वचालित केस विवरण (लाइव)",
    lblCC: "मुख्य तकलीफ एवं लक्षण",
    lblDuration: "दर्द की तीव्रता व समय अवधि",
    lblSigns: "संबंधित संकेत व फैलाव",
    lblPast: "पुरानी बीमारी (शुगर और बीपी)",
    lblDocs: "जांच रिपोर्ट व पर्चे",
    lblMeds: "दैनिक दवाएं / दर्द निवारक",
    lblAllergy: "दवाइयों से एलर्जी",
    lblLifestyle: "जीवनशैली व पारिवारिक इतिहास",
    valWaitingSymptom: "लक्षण चुने जाने की प्रतीक्षा में...",
    valNotAnswered: "अभी उत्तर नहीं दिया",
    valNoneReported: "कुछ नहीं",
    valNegative: "नहीं / सामान्य",
    valNoDocs: "कोई रिपोर्ट नहीं जोड़ी (वैकल्पिक)",
    valNone: "कोई नहीं",
    valStandard: "सामान्य",
    submitCaseBtn: "🚀 डॉक्टर जांच के लिए भेजें",
    submitNotice: "केस सुरक्षित रूप से डॉक्टर की जांच कतार में भेजा जाता है।",
    thankYouTitle: "धन्यवाद",
    thankYouSub: "आपकी स्वास्थ्य जानकारी सफलतापूर्वक दर्ज हो गई है।",
    tokenLabel: "🎫 टोकन आईडी:",
    waitHeading: "कृपया अपनी बारी की प्रतीक्षा करें",
    waitMsg: "डॉक्टर जल्द ही आपको बुलाएंगे। आपको टोकन नंबर से बुलाया जाएगा।",
    redirectMsg: "नए मरीज के पंजीकरण पर लौटने में शेष समय",
    nextPatientBtn: "➕ तुरंत अगला मरीज दर्ज करें",
    spokenThankYou: "धन्यवाद। आपका पंजीकरण पूरा हो गया है। कृपया प्रतीक्षा करें, डॉक्टर जल्द ही आपको बुलाएंगे।",
    spokenVerified: "डॉक्टर ने आपका पर्चा सत्यापित कर दिया है। दवाइयां उपलब्ध हैं।",
    verifiedBadge: "डॉक्टर द्वारा सत्यापित",
    verifiedTitle: "🎉 डॉक्टर द्वारा केस की जांच पूरी हो गई है!",
    docDiagnosisLabel: "🩺 डॉक्टर का अंतिम निदान (Diagnosis):",
    docRxLabel: "💊 डॉक्टर का पर्चा व दवाइयां (Rx):",
    docAdviceLabel: "📝 डॉक्टर की सलाह व निर्देश:",
    printRxBtn: "🖨️ सरकारी पर्चा देखें व प्रिंट करें",
    waitingInQueue: "⏳ डॉक्टर की जांच की प्रतीक्षा में...",
    trackModalTitle: "मरीज केस व डॉक्टर का पर्चा ट्रैक करें",
    searchBtn: "खोजें",
    symptomChest: "सीने में दर्द या भारीपन",
    symptomChestSub: "सीने पर भारी दबाव, जकड़न या पसीना",
    symptomStomach: "पेट में जलन या एसिडिटी",
    symptomStomachSub: "खट्टी डकार, जलन, जी मिचलाना या दर्द",
    symptomFever: "तेज बुखार और खांसी",
    symptomFeverSub: "कंपकंपी, बलगम या बदन गर्म होना",
    symptomHeadache: "तेज सिरदर्द व चक्कर",
    symptomHeadacheSub: "माइग्रेन, सिर घूमना या भारीपन",
    symptomJoint: "जोड़ों और हड्डियों में दर्द",
    symptomJointSub: "घुटनों में जकड़न, सूजन या कमर दर्द",
    symptomOther: "सामान्य बीमारी / अन्य",
    symptomOtherSub: "अन्य कोई शारीरिक परेशानी",
    mildIntensity: "हल्का दर्द (1 से 3)",
    modIntensity: "मध्यम दर्द (4 से 6)",
    sevIntensity: "असहनीय तेज (7 से 10)",
    charHeavy: "भारी दबाव जैसा",
    charHeavySub: "छाती पर भारी वजन रखा हो",
    charBurning: "आग या एसिड जैसी जलन",
    charBurningSub: "पेट या गले में तेज जलन",
    charSharp: "तीखा चुभन वाला दर्द",
    charSharpSub: "सुई चुभने जैसा अहसास",
    charDull: "लगातार मीठा दर्द",
    charDullSub: "धीमा लगातार बना रहने वाला दर्द",
    durToday: "आज ही शुरू हुआ (< 24 घंटे)",
    durTodaySub: "कुछ ही घंटों पहले शुरुआत",
    durDays: "2 से 4 दिनों से",
    durDaysSub: "पिछले कुछ दिनों से लगातार",
    durWeeks: "1 से 2 हफ़्तों से",
    durWeeksSub: "एक या दो सप्ताह से बना हुआ",
    durMonth: "1 महीने से अधिक समय से",
    durMonthSub: "काफी पुराने समय से चली आ रही परेशानी",
    yesText: "हाँ (YES)",
    noText: "नहीं (NO)",
    yesSub: "हाँ, मुझे है",
    noSub: "नहीं, मुझे नहीं है",
    skipDocBtn: "⏭️ मेरे पास अभी रिपोर्ट नहीं है (आगे बढ़ें)",
    uploadDocTitle: "पुरानी जांच रिपोर्ट / पर्चे की फोटो अपलोड करें (वैकल्पिक)",
    uploadDocSub: "फाइल प्रकार: फोटो (JPG, PNG) या पीडीएफ (अधिकतम 10MB)"
  },
  ta: {
    tagline: "பிரச்சனை அறிக்கை #47 • ஸ்மார்ட் இந்தியா ஹேக்கத்தான் 2026",
    voiceOn: "குரல் உதவி: <strong>ஆன்</strong>",
    voiceOff: "குரல் உதவி: <strong>ஆஃப்</strong>",
    docLogin: "👨‍⚕️ மருத்துவர் உள்நுழைவு",
    trackCase: "🔍 நிலை சரிபார்க்கவும்",
    regTitle: "📋 நோயாளி பதிவு & மொழி தேர்வு",
    regSub: "மருத்துவ பரிசோதனையைத் தொடங்க அடிப்படை விவரங்களை நிரப்பவும்",
    chooseLang: "🌐 உங்கள் மொழியைத் தேர்ந்தெடுக்கவும்:",
    demoPresets: "⚡ விரைவு மாதிரி சுயவிவரங்கள்:",
    presetCardiac: "🫀 இதய நோயாளி (ராஜேஷ், 52)",
    presetGastric: "🔥 வயிற்று எரிச்சல் (சுனிதா, 38)",
    presetPediatric: "👶 குழந்தை காய்ச்சல் (ஆரவ், 8)",
    nameLabel: "👤 நோயாளியின் முழு பெயர் *",
    namePlaceholder: "எ.கா. ரமேஷ் வர்மா",
    ageLabel: "🎂 வயது *",
    genderLabel: "⚧ பாலினம் *",
    genderMale: "ஆண் (Male)",
    genderFemale: "பெண் (Female)",
    genderOther: "மற்றவை (Other)",
    phoneLabel: "📱 கைபேசி எண்",
    assistLabel: "♿ நோயாளி உதவி முறை",
    assistVoice: "குரல் மற்றும் பட முறை (உதவி முறை)",
    assistStandard: "வழக்கமான டிஜிட்டல் முறை",
    startIntakeBtn: "🚀 மருத்துவ பரிசோதனையைத் தொடங்கவும் ➔",
    editReg: "✏️ பதிவை மாற்றவும்",
    stepProgress: "படி {step} / 11",
    listenBtn: "🔊 கேள்வியைக் கேட்கவும்",
    tapToSpeak: "🎙️ பேசி பதிலளிக்கவும்",
    listeningWait: "கேட்கிறது... உங்கள் மொழியில் பேசுங்கள்",
    contradictionTitle: "⚠️ நேரலை மருத்துவ முரண்பாடு கண்டறிதல்",
    contradictionHint: "AI முரண்பாடான தகவல்களைக் கண்டறியும்...",
    caseSheetTitle: "📋 மருத்துவ விவரப் பட்டியல்",
    lblCC: "முக்கிய பிரச்சனை",
    lblDuration: "தீவிரம் & காலம்",
    lblSigns: "தொடர்புடைய அறிகுறிகள்",
    lblPast: "முந்தைய வரலாறு (சர்க்கரை & BP)",
    lblDocs: "பரிசோதனை அறிக்கைகள்",
    lblMeds: "தினசரி மருந்துகள்",
    lblAllergy: "மருந்து ஒவ்வாமை",
    lblLifestyle: "வாழ்க்கை முறை & குடும்ப வரலாறு",
    valWaitingSymptom: "அறிகுறி தேர்வுக்காக காத்திருக்கிறது...",
    valNotAnswered: "இன்னும் பதிலளிக்கவில்லை",
    valNoneReported: "எதுவுமில்லை",
    valNegative: "இல்லை / வழக்கமானது",
    valNoDocs: "அறிக்கைகள் இணைக்கப்படவில்லை",
    valNone: "இல்லை",
    valStandard: "வழக்கமானது",
    submitCaseBtn: "🚀 மருத்துவரிடம் அனுப்பவும்",
    submitNotice: "விவரங்கள் பாதுகாப்பாக மருத்துவருக்கு அனுப்பப்படுகின்றன.",
    thankYouTitle: "நன்றி",
    thankYouSub: "உங்கள் தகவல்கள் வெற்றிகரமாக பதிவு செய்யப்பட்டன.",
    tokenLabel: "🎫 டோக்கன் எண்:",
    waitHeading: "உங்கள் முறை வரும் வரை காத்திருக்கவும்",
    waitMsg: "மருத்துவர் விரைவில் உங்களை அழைப்பார்.",
    redirectMsg: "புதிய பதிவுக்குத் திரும்பும் நேரம்",
    nextPatientBtn: "➕ அடுத்த நோயாளியைப் பதிவு செய்யவும்",
    spokenThankYou: "நன்றி. உங்கள் பதிவு முடிந்தது. மருத்துவர் விரைவில் உங்களை அழைப்பார்.",
    spokenVerified: "மருத்துவர் உங்கள் வழக்கை சரிபார்த்துள்ளார். மருந்துச் சீட்டு தயாராக உள்ளது.",
    verifiedBadge: "மருத்துவரால் சரிபார்க்கப்பட்டது",
    verifiedTitle: "🎉 மருத்துவர் பரிசோதனை முடிந்தது!",
    docDiagnosisLabel: "🩺 மருத்துவரின் இறுதி நோயறிதல்:",
    docRxLabel: "💊 மருந்துச் சீட்டு (Rx):",
    docAdviceLabel: "📝 மருத்துவரின் மருத்துவ அறிவுரை:",
    printRxBtn: "🖨️ மருந்துச் சீட்டை அச்சிடுக",
    waitingInQueue: "⏳ மருத்துவர் வருகைக்காக காத்திருக்கிறது...",
    trackModalTitle: "மருந்துச் சீட்டை சரிபார்க்கவும்",
    searchBtn: "தேடு",
    symptomChest: "நெஞ்சு வலி அல்லது அழுத்தம்",
    symptomChestSub: "கடுமையான நெஞ்சு பாரம், வியர்வை",
    symptomStomach: "வயிற்று எரிச்சல் அல்லது அசிடிட்டி",
    symptomStomachSub: "எரிச்சல், வாந்தி அல்லது மேல் வயிற்று வலி",
    symptomFever: "காய்ச்சல் & இருமல்",
    symptomFeverSub: "குளிர் நடுக்கம், சளி அல்லது உடல் சூடு",
    symptomHeadache: "தலைவலி & மயக்கம்",
    symptomHeadacheSub: "ஒற்றைத் தலைவலி, தலைச்சுற்றல்",
    symptomJoint: "மூட்டு & எலும்பு வலி",
    symptomJointSub: "முழங்கால் வலி, மூட்டு இறுக்கம்",
    symptomOther: "பிற பிரச்சனைகள்",
    symptomOtherSub: "மற்ற உடல்நல உபாதைகள்",
    mildIntensity: "லேசான வலி (1 - 3)",
    modIntensity: "மிதமான வலி (4 - 6)",
    sevIntensity: "கடுமையான வலி (7 - 10)",
    charHeavy: "கனமான அழுத்தம்",
    charHeavySub: "நெஞ்சில் பாரம் இருப்பது போன்ற உணர்வு",
    charBurning: "தீ போன்ற எரிச்சல்",
    charBurningSub: "வயிற்றில் கடுமையான எரிச்சல்",
    charSharp: "குத்துவது போன்ற வலி",
    charSharpSub: "ஊசி குத்துவது போன்ற உணர்வு",
    charDull: "தொடர்ச்சியான வலி",
    charDullSub: "நீண்ட நேர மிதமான வலி",
    durToday: "இன்று தொடங்கியது (< 24 மணிநேரம்)",
    durTodaySub: "சில மணி நேரங்களுக்கு முன்",
    durDays: "2 முதல் 4 நாட்கள்",
    durDaysSub: "சில நாட்களாக தொடர்ந்து",
    durWeeks: "1 முதல் 2 வாரங்கள்",
    durWeeksSub: "ஒன்று அல்லது இரண்டு வாரங்களாக",
    durMonth: "1 மாதத்திற்கும் மேல்",
    durMonthSub: "நீண்ட காலமாக இருக்கும் பிரச்சனை",
    yesText: "ஆம் (YES)",
    noText: "இல்லை (NO)",
    yesSub: "ஆம், உள்ளது",
    noSub: "இல்லை",
    skipDocBtn: "⏭️ அறிக்கைகள் இல்லை (தவிர்க்கவும்)",
    uploadDocTitle: "பழைய அறிக்கையை பதிவேற்றவும் (விருப்பத்தேர்வு)",
    uploadDocSub: "வடிவங்கள்: JPG, PNG, PDF (அதிகபட்சம் 10MB)"
  },
  te: {
    tagline: "సమస్య ప్రకటన #47 • స్మార్ట్ ఇండియా హ్యాకథాన్ 2026",
    voiceOn: "వాయిస్ సహాయం: <strong>ఆన్</strong>",
    voiceOff: "వాయిస్ సహాయం: <strong>ఆఫ్</strong>",
    docLogin: "👨‍⚕️ డాక్టర్ లాగిన్ / పోర్టల్",
    trackCase: "🔍 కేస్ స్థితిని తనిఖీ చేయండి",
    regTitle: "📋 రోగి నమోదు & భాష ఎంపిక",
    regSub: "వైద్య పరీక్ష ప్రారంభించడానికి మీ ప్రాథమిక వివరాలు నమోదు చేయండి",
    chooseLang: "🌐 మీ భాషను ఎంచుకోండి:",
    demoPresets: "⚡ శీఘ్ర ప్రదర్శన నమూనాలు:",
    presetCardiac: "🫀 గుండె రోగి (రాజేష్, 52)",
    presetGastric: "🔥 గ్యాస్ట్రిక్ సమస్య (సునీత, 38)",
    presetPediatric: "👶 పిల్లల జ్వరం (ఆరవ్, 8)",
    nameLabel: "👤 రోగి పూర్తి పేరు *",
    namePlaceholder: "ఉదా. రమేష్ వర్మ",
    ageLabel: "🎂 వయస్సు *",
    genderLabel: "⚧ లింగం *",
    genderMale: "పురుషుడు (Male)",
    genderFemale: "మహిళ (Female)",
    genderOther: "ఇతర (Other)",
    phoneLabel: "📱 మొబైల్ నంబర్",
    assistLabel: "♿ రోగి సహాయ విధానం",
    assistVoice: "వాయిస్ & చిత్రాల మోడ్ (సహాయక మోడ్)",
    assistStandard: "సాధారణ డిజిటల్ మోడ్",
    startIntakeBtn: "🚀 ఆరోగ్య పరీక్ష ప్రారంభించండి ➔",
    editReg: "✏️ నమోదు సవరించండి",
    stepProgress: "దశ {step} / 11",
    listenBtn: "🔊 ప్రశ్న వినండి",
    tapToSpeak: "🎙️ మాట్లాడి సమాధానం ఇవ్వండి",
    listeningWait: "వింటున్నాము... మీ భాషలో మాట్లాడండి",
    contradictionTitle: "⚠️ నిజ-సమయ వైద్య విరుద్ధతల గుర్తింపు",
    contradictionHint: "AI పరస్పర విరుద్ధమైన ఔషధాలను మరియు ప్రమాదాలను గుర్తిస్తుంది...",
    caseSheetTitle: "📋 ఆటోమేటెడ్ కేస్ షీట్",
    lblCC: "ప్రధాన సమస్య",
    lblDuration: "తీవ్రత & వ్యవధి",
    lblSigns: "సంబంధిత లక్షణాలు",
    lblPast: "గత చరిత్ర (షుగర్ & బీపీ)",
    lblDocs: "ల్యాబ్ రిపోర్టులు",
    lblMeds: "రోజువారీ మందులు",
    lblAllergy: "మందుల అలెర్జీ",
    lblLifestyle: "జీవనశైలి & కుటుంబ చరిత్ర",
    valWaitingSymptom: "లక్షణాల ఎంపిక కోసం వేచి చూస్తోంది...",
    valNotAnswered: "ఇంకా సమాధానం ఇవ్వలేదు",
    valNoneReported: "ఏమీ లేదు",
    valNegative: "లేదు / సాధారణం",
    valNoDocs: "రిపోర్టులు జతచేయలేదు",
    valNone: "ఏదీ లేదు",
    valStandard: "సాధారణం",
    submitCaseBtn: "🚀 డాక్టర్ సమీక్షకు పంపండి",
    submitNotice: "వివరాలు సురక్షితంగా డాక్టర్‌కు బదిలీ చేయబడతాయి.",
    thankYouTitle: "ధన్యవాదాలు",
    thankYouSub: "మీ ఆరోగ్య వివరాలు విజయవంతంగా నమోదు చేయబడ్డాయి.",
    tokenLabel: "🎫 టోకెన్ ఐడీ:",
    waitHeading: "దయచేసి మీ పిలుపు వచ్చేవరకు వేచి ఉండండి",
    waitMsg: "వైద్యులు త్వరలో మిమ్మల్ని పిలుస్తారు. టోకెన్ నంబర్ ప్రకారం పిలుస్తారు.",
    redirectMsg: "కొత్త రోగి నమోదుకు తిరిగి వెళ్ళడానికి సమయం",
    nextPatientBtn: "➕ తదుపరి రోగిని నమోదు చేయండి",
    spokenThankYou: "ధన్యవాదాలు. మీ నమోదు పూర్తయింది. దయచేసి వేచి ఉండండి, వైద్యులు త్వరలో మిమ్మల్ని పిలుస్తారు.",
    spokenVerified: "డాక్టర్ మీ కేస్‌ను ధృవీకరించారు. ప్రిస్క్రిప్షన్ సిద్ధంగా ఉంది.",
    verifiedBadge: "డాక్టర్ ధృవీకరించారు",
    verifiedTitle: "🎉 డాక్టర్ ధృవీకరణ పూర్తయింది!",
    docDiagnosisLabel: "🩺 వైద్యుల రోగ నిర్ధారణ:",
    docRxLabel: "💊 ప్రిస్క్రిప్షన్ (Rx):",
    docAdviceLabel: "📝 వైద్యుల సలహాలు & సూచనలు:",
    printRxBtn: "🖨️ ప్రిస్క్రిప్షన్ ప్రింట్ చేయండి",
    waitingInQueue: "⏳ వైద్యుల కోసం క్యూలో వేచి ఉంది...",
    trackModalTitle: "కేస్ & ప్రిస్క్రిప్షన్ తనిఖీ చేయండి",
    searchBtn: "శోధించండి",
    symptomChest: "ఛాతీ నొప్పి లేదా ఒత్తిడి",
    symptomChestSub: "తీవ్రమైన బరువు, పట్టేయడం లేదా చెమటలు",
    symptomStomach: "కడుపులో మంట లేదా ఎసిడిటీ",
    symptomStomachSub: "మంట, వికారం లేదా నొప్పి",
    symptomFever: "తీవ్ర జ్వరం & దగ్గు",
    symptomFeverSub: "వణుకు, జలుబు లేదా ఒళ్లు కాలడం",
    symptomHeadache: "తీవ్ర తలనొప్పి & మైకం",
    symptomHeadacheSub: "మైగ్రేన్ లేదా కళ్ళు తిరగడం",
    symptomJoint: "కీళ్ళు & ఎముకల నొప్పులు",
    symptomJointSub: "మోకాళ్ళ వాపు, బిగుతు లేదా నొప్పి",
    symptomOther: "సాధారణ అనారోగ్యం / ఇతర",
    symptomOtherSub: "ఇతర శారీరక ఇబ్బందులు",
    mildIntensity: "తేలికపాటి నొప్పి (1 - 3)",
    modIntensity: "మధ్యస్థ నొప్పి (4 - 6)",
    sevIntensity: "తీవ్రమైన నొప్పి (7 - 10)",
    charHeavy: "భారీ ఒత్తిడి",
    charHeavySub: "ఛాతీపై బరువు పెట్టినట్లు",
    charBurning: "మంటగా అనిపించడం",
    charBurningSub: "కడుపు లేదా గొంతులో మంట",
    charSharp: "సూది గుచ్చినట్లు",
    charSharpSub: "తీక్షణమైన నొప్పి",
    charDull: "నిరంతర మందకొడి నొప్పి",
    charDullSub: "నెమ్మదిగా నిరంతరం ఉండే నొప్పి",
    durToday: "ఈ రోజే మొదలైంది (< 24 గంటలు)",
    durTodaySub: "కొన్ని గంటల క్రితం",
    durDays: "2 నుండి 4 రోజులు",
    durDaysSub: "కొన్ని రోజులుగా నిరంతరం",
    durWeeks: "1 నుండి 2 వారాలు",
    durWeeksSub: "వారం లేదా రెండు వారాలుగా",
    durMonth: "1 నెల కంటే ఎక్కువ",
    durMonthSub: "చాలా కాలంగా ఉన్న సమస్య",
    yesText: "అవును (YES)",
    noText: "కాదు (NO)",
    yesSub: "అవును, ఉంది",
    noSub: "లేదు",
    skipDocBtn: "⏭️ రిపోర్టులు లేవు (దాటవేయండి)",
    uploadDocTitle: "పాత రిపోర్టును అప్‌లోడ్ చేయండి (ఐచ్ఛికం)",
    uploadDocSub: "ఫైల్స్: JPG, PNG, PDF (గరిష్టంగా 10MB)"
  },
  bn: {
    tagline: "সমস্যা বিবৃতি #৪৭ • স্মার্ট ইন্ডিয়া হ্যাকাথন ২০২৬",
    voiceOn: "ভয়েস সহায়তা: <strong>চালু</strong>",
    voiceOff: "ভয়েস সহায়তা: <strong>বন্ধ</strong>",
    docLogin: "👨‍⚕️ ডাক্তার লগইন / পোর্টাল",
    trackCase: "🔍 কেস স্থিতি দেখুন",
    regTitle: "📋 রোগী নিবন্ধন ও ভাষা নির্বাচন",
    regSub: "স্বাস্থ্য পরীক্ষা শুরু করতে প্রাথমিক তথ্য পূরণ করুন",
    chooseLang: "🌐 আপনার পছন্দের ভাষা বেছে নিন:",
    demoPresets: "⚡ দ্রুত ডেমো প্রোফাইল:",
    presetCardiac: "🫀 হৃদরোগী (রাজেশ, ৫২)",
    presetGastric: "🔥 পেটের সমস্যা (সুনীতা, ৩৮)",
    presetPediatric: "👶 শিশুর জ্বর (আরভ, ৮)",
    nameLabel: "👤 রোগীর পুরো নাম *",
    namePlaceholder: "উদা. রমেশ ভার্মা",
    ageLabel: "🎂 বয়স *",
    genderLabel: "⚧ লিঙ্গ *",
    genderMale: "পুরুষ (Male)",
    genderFemale: "মহিলা (Female)",
    genderOther: "অন্যান্য (Other)",
    phoneLabel: "📱 মোবাইল নম্বর",
    assistLabel: "♿ রোগী সহায়তা মোড",
    assistVoice: "সহায়ক ভয়েস ও ছবি মোড",
    assistStandard: "সাধারণ ডিজিটাল মোড",
    startIntakeBtn: "🚀 স্বাস্থ্য পরীক্ষা শুরু করুন ➔",
    editReg: "✏️ নিবন্ধন পরিবর্তন",
    stepProgress: "পদক্ষেপ {step} / ১১",
    listenBtn: "🔊 প্রশ্ন শুনুন",
    tapToSpeak: "🎙️ মুখে বলে জানান",
    listeningWait: "শুনছি... আপনার ভাষায় বলুন",
    contradictionTitle: "⚠️ লাইভ মেডিকেল অসঙ্গতি সনাক্তকরণ",
    contradictionHint: "AI বিপরীত ওষুধের ঝুঁকি বিশ্লেষণ করে...",
    caseSheetTitle: "📋 স্বয়ংক্রিয় কেস বিবরণী",
    lblCC: "প্রধান শারীরিক সমস্যা",
    lblDuration: "তীব্রতা ও সময়কাল",
    lblSigns: "আনুষঙ্গিক লক্ষণ",
    lblPast: "পূর্ব ইতিহাস (সুগার ও প্রেশার)",
    lblDocs: "পরীক্ষার রিপোর্ট",
    lblMeds: "নিয়মিত ওষুধ",
    lblAllergy: "ওষুধের অ্যালার্জি",
    lblLifestyle: "জীবনযাত্রা ও পারিবারিক ইতিহাস",
    valWaitingSymptom: "লক্ষণ নির্বাচনের অপেক্ষায়...",
    valNotAnswered: "এখনও উত্তর দেওয়া হয়নি",
    valNoneReported: "কিছু নেই",
    valNegative: "নেই / স্বাভাবিক",
    valNoDocs: "রিপোর্ট যুক্ত করা হয়নি",
    valNone: "নেই",
    valStandard: "স্বাভাবিক",
    submitCaseBtn: "🚀 ডাক্তারের কাছে পাঠান",
    submitNotice: "তথ্য সুরক্ষিতভাবে ডাক্তারের কাছে পাঠানো হবে।",
    thankYouTitle: "ধন্যবাদ",
    thankYouSub: "আপনার তথ্য সফলভাবে নথিভুক্ত হয়েছে।",
    tokenLabel: "🎫 টোকেন আইডি:",
    waitHeading: "দয়া করে আপনার ডাক আসা পর্যন্ত অপেক্ষা করুন",
    waitMsg: "ডাক্তারবাবু শীঘ্রই আপনাকে ডাকবেন।",
    redirectMsg: "নতুন রোগী রেজিস্ট্রেশনে ফেরার সময়",
    nextPatientBtn: "➕ পরবর্তী রোগী নথিভুক্ত করুন",
    spokenThankYou: "ধন্যবাদ। আপনার রেজিস্ট্রেশন সম্পন্ন হয়েছে। দয়া করে অপেক্ষা করুন, ডাক্তারবাবু শীঘ্রই ডাকবেন।",
    spokenVerified: "ডাক্তারবাবু আপনার প্রেসক্রিপশন অনুমোদন করেছেন। ওষুধ প্রস্তুত।",
    verifiedBadge: "ডাক্তার দ্বারা অনুমোদিত",
    verifiedTitle: "🎉 ডাক্তারবাবু যাচাই সম্পন্ন করেছেন!",
    docDiagnosisLabel: "🩺 ডাক্তারের চূড়ান্ত রোগনির্ণয়:",
    docRxLabel: "💊 প্রেসক্রিপশন ও ওষুধ (Rx):",
    docAdviceLabel: "📝 ডাক্তারের পরামর্শ ও নির্দেশ:",
    printRxBtn: "🖨️ প্রেসক্রিপশন প্রিন্ট করুন",
    waitingInQueue: "⏳ ডাক্তারের অপেক্ষায়...",
    trackModalTitle: "রোগীর কেস ও প্রেসক্রিপশন দেখুন",
    searchBtn: "খুঁজুন",
    symptomChest: "বুকে ব্যথা বা চাপ",
    symptomChestSub: "বুকে তীব্র ভারী ভাব, ঘাম হওয়া",
    symptomStomach: "পেটে জ্বালা বা গ্যাস",
    symptomStomachSub: "অম্লতা, বমি বমি ভাব বা পেটে ব্যথা",
    symptomFever: "তীব্র জ্বর ও কাশি",
    symptomFeverSub: "কাঁপুনির সঙ্গে জ্বর, সর্দি",
    symptomHeadache: "তীব্র মাথাব্যথা ও মাথা ঘোরা",
    symptomHeadacheSub: "মাইগ্রেন বা দৃষ্টি ঝাপসা হওয়া",
    symptomJoint: "জয়েন্টে বা হাড়ে ব্যথা",
    symptomJointSub: "হাঁটুতে টান বা ব্যথা",
    symptomOther: "সাধারণ অসুস্থতা / অন্যান্য",
    symptomOtherSub: "অন্যান্য শারীরিক সমস্যা",
    mildIntensity: "হালকা ব্যথা (১ - ৩)",
    modIntensity: "মাঝারি ব্যথা (৪ - ৬)",
    sevIntensity: "অসহ্য তীব্র ব্যথা (৭ - ১০)",
    charHeavy: "ভারী চাপ",
    charHeavySub: "বুকে ভার চেপে থাকার মতো",
    charBurning: "জ্বালা পোড়া",
    charBurningSub: "পেটে বা বুকে আগুনের মতো জ্বালা",
    charSharp: "তীক্ষ্ণ ছুঁচ ফোটানোর মতো",
    charSharpSub: "তীক্ষ্ণ ব্যথা",
    charDull: "একটানা হালকা ব্যথা",
    charDullSub: "ক্রমাগত হালকা ব্যথা",
    durToday: "আজই শুরু হয়েছে (< ২৪ ঘণ্টা)",
    durTodaySub: "কয়েক ঘণ্টা আগে",
    durDays: "২ থেকে ৪ দিন ধরে",
    durDaysSub: "কয়েক দিন ধরে একটানা",
    durWeeks: "১ থেকে ২ সপ্তাহ ধরে",
    durWeeksSub: "এক বা দুই সপ্তাহ ধরে",
    durMonth: "১ মাসের বেশি সময় ধরে",
    durMonthSub: "অনেক পুরনো সমস্যা",
    yesText: "হ্যাঁ (YES)",
    noText: "না (NO)",
    yesSub: "হ্যাঁ, আছে",
    noSub: "না, নেই",
    skipDocBtn: "⏭️ রিপোর্ট নেই (পরবর্তী পদক্ষেপে যান)",
    uploadDocTitle: "পুরনো রিপোর্ট আপলোড করুন (ঐচ্ছিক)",
    uploadDocSub: "ফরম্যাট: JPG, PNG, PDF (সর্বোচ্চ 10MB)"
  },
  mr: {
    tagline: "समस्या विधान #47 • स्मार्ट इंडिया हॅकाथॉन 2026",
    voiceOn: "आवाज सहाय्य: <strong>सुरू</strong>",
    voiceOff: "आवाज सहाय्य: <strong>बंद</strong>",
    docLogin: "👨‍⚕️ डॉक्टर लॉगिन / पोर्टल",
    trackCase: "🔍 केस स्थिती तपासा",
    regTitle: "📋 रुग्ण नोंदणी आणि भाषा निवड",
    regSub: "आरोग्य तपासणी सुरू करण्यासाठी मूलभूत माहिती भरा",
    chooseLang: "🌐 आपली पसंतीची भाषा निवडा:",
    demoPresets: "⚡ जलद डेमो प्रोफाइल:",
    presetCardiac: "🫀 हृदयविकार रुग्ण (राजेश, ५२)",
    presetGastric: "🔥 पोटातील जळजळ (सुनीता, ३८)",
    presetPediatric: "👶 बालरोग ताप (आरव, ८)",
    nameLabel: "👤 रुग्णाचे पूर्ण नाव *",
    namePlaceholder: "उदा. रमेश वर्मा",
    ageLabel: "🎂 वय (वर्षे) *",
    genderLabel: "⚧ लिंग *",
    genderMale: "पुरुष (Male)",
    genderFemale: "महिला (Female)",
    genderOther: "इतर (Other)",
    phoneLabel: "📱 मोबाईल नंबर",
    assistLabel: "♿ रुग्ण सहाय्य मोड",
    assistVoice: "सहायक व्हॉईस मोड (मोठी चित्रे + आवाज)",
    assistStandard: "सामान्य डिजिटल मोड",
    startIntakeBtn: "🚀 आरोग्य तपासणी सुरू करा ➔",
    editReg: "✏️ नोंदणी बदला",
    stepProgress: "टप्पा {step} / 11",
    listenBtn: "🔊 प्रश्न ऐका",
    tapToSpeak: "🎙️ बोलून सांगा",
    listeningWait: "ऐकत आहोत... तुमच्या भाषेत बोला",
    contradictionTitle: "⚠️ रिअल-टाईम वैद्यकीय विसंगती शोध",
    contradictionHint: "AI परस्परविरोधी औषधे व धोके ओळखते...",
    caseSheetTitle: "📋 स्वयंचलित केस शीट (थेट)",
    lblCC: "मुख्य त्रास व लक्षणे",
    lblDuration: "वेदना तीव्रता व कालावधी",
    lblSigns: "संबंधित इतर लक्षणे",
    lblPast: "जुना आजार (शुगर व बीपी)",
    lblDocs: "तपासणी रिपोर्ट",
    lblMeds: "दररोजची औषधे",
    lblAllergy: "औषधांची ॲलर्जी",
    lblLifestyle: "जीवनशैली व कौटुंबिक इतिहास",
    valWaitingSymptom: "लक्षण निवडण्याची प्रतीक्षा...",
    valNotAnswered: "अद्याप उत्तर नाही",
    valNoneReported: "काही नाही",
    valNegative: "नाही / सामान्य",
    valNoDocs: "रिपोर्ट जोडलेली नाही",
    valNone: "काही नाही",
    valStandard: "सामान्य",
    submitCaseBtn: "🚀 डॉक्टरांकडे तपासायला पाठवा",
    submitNotice: "केस सुरक्षितपणे डॉक्टरांच्या तपासणी रांगेत पाठवली जाते.",
    thankYouTitle: "धन्यवाद",
    thankYouSub: "आपली आरोग्य माहिती यशस्वीरित्या नोंदवली गेली आहे.",
    tokenLabel: "🎫 टोकन आयडी:",
    waitHeading: "कृपया आपली पाळी येईपर्यंत प्रतीक्षा करा",
    waitMsg: "डॉक्टर लवकरच आपल्याला तपासतील. टोकन नंबरने हाक मारली जाईल.",
    redirectMsg: "नवीन नोंदणीकडे परत जाण्याची वेळ",
    nextPatientBtn: "➕ पुढील रुग्णाची नोंदणी करा",
    spokenThankYou: "धन्यवाद. आपली नोंदणी पूर्ण झाली आहे. कृपया प्रतीक्षा करा, डॉक्टर लवकरच बोलवतील.",
    spokenVerified: "डॉक्टरांनी केस तपासली असून औषधांची चिठ्ठी तयार आहे.",
    verifiedBadge: "डॉक्टरांनी प्रमाणित केले",
    verifiedTitle: "🎉 डॉक्टरांनी तपासणी पूर्ण केली आहे!",
    docDiagnosisLabel: "🩺 डॉक्टरांचे अंतिम निदान:",
    docRxLabel: "💊 औषधांची चिठ्ठी (Rx):",
    docAdviceLabel: "📝 डॉक्टरांचा सल्ला व सूचना:",
    printRxBtn: "🖨️ चिठ्ठी प्रिंट करा",
    waitingInQueue: "⏳ डॉक्टरांच्या तपासणीची प्रतीक्षा...",
    trackModalTitle: "रुग्ण केस व औषध चिठ्ठी तपासा",
    searchBtn: "शोधा",
    symptomChest: "छातीत दुखणे किंवा जडपणा",
    symptomChestSub: "छातीवर तीव्र दाब, घाम येणे",
    symptomStomach: "पोटात जळजळ किंवा ॲसिडिटी",
    symptomStomachSub: "मळमळ, आंबट ढेकर किंवा पोटदुखी",
    symptomFever: "तीव्र ताप व खोकला",
    symptomFeverSub: "थंडी वाजून ताप, कफ",
    symptomHeadache: "तीव्र डोकेदुखी व चक्कर",
    symptomHeadacheSub: "मायग्रेन, डोळ्यांसमोर अंधारी",
    symptomJoint: "सांधेदुखी व हाडांचे दुखणे",
    symptomJointSub: "गुडघेदुखी, सांधे आखडणे",
    symptomOther: "सामान्य आजार / इतर",
    symptomOtherSub: "इतर कोणताही शारीरिक त्रास",
    mildIntensity: "हलक्या वेदना (1 ते 3)",
    modIntensity: "मध्यम वेदना (4 ते 6)",
    sevIntensity: "असह्य तीव्र वेदना (7 ते 10)",
    charHeavy: "जड दाब असल्यासारखे",
    charHeavySub: "छातीवर वजन ठेवल्यासारखे",
    charBurning: "आगीसारखी जळजळ",
    charBurningSub: "पोटात किंवा छातीत जळजळ",
    charSharp: "तीक्ष्ण सुई टोचल्यासारखे",
    charSharpSub: "अचानक तीक्ष्ण कळ",
    charDull: "सलग मंद वेदना",
    charDullSub: "सतत राहणारे दुखणे",
    durToday: "आजच सुरू झाले (< 24 तास)",
    durTodaySub: "काही तासांपूर्वी",
    durDays: "2 ते 4 दिवसांपासून",
    durDaysSub: "काही दिवसांपासून सलग",
    durWeeks: "1 ते 2 आठवड्यांपासून",
    durWeeksSub: "एक किंवा दोन आठवड्यांपासून",
    durMonth: "1 महिन्यापेक्षा जास्त काळ",
    durMonthSub: "फार जुना आजार",
    yesText: "होय (YES)",
    noText: "नाही (NO)",
    yesSub: "होय, आहे",
    noSub: "नाही, नाहीये",
    skipDocBtn: "⏭️ रिपोर्ट उपलब्ध नाही (पुढे जा)",
    uploadDocTitle: "जुनी रिपोर्ट अपलोड करा (ऐच्छिक असल्यास)",
    uploadDocSub: "फाइल प्रकार: JPG, PNG, PDF (कमाल 10MB)"
  },
  gu: {
    tagline: "સમસ્યા નિવેદન #47 • સ્માર્ટ ઇન્ડિયા હેકાથોન 2026",
    voiceOn: "અવાજ સહાય: <strong>ચાલુ</strong>",
    voiceOff: "અવાજ સહાય: <strong>બંધ</strong>",
    docLogin: "👨‍⚕️ ડૉક્ટર લૉગિન / પોર્ટલ",
    trackCase: "🔍 કેસ સ્થિતિ તપાસો",
    regTitle: "📋 દર્દી નોંધણી અને ભાષા પસંદગી",
    regSub: "તપાસ શરૂ કરવા માટે મૂળભૂત વિગતો ભરો",
    chooseLang: "🌐 તમારી ભાષા પસંદ કરો:",
    demoPresets: "⚡ ઝડપી ડેમો પ્રોફાઇલ:",
    presetCardiac: "🫀 હૃદય દર્દી (રાજેશ, 52)",
    presetGastric: "🔥 ગેસ્ટ્રિક તકલીફ (સુનિતા, 38)",
    presetPediatric: "👶 બાળ તાવ (આરવ, 8)",
    nameLabel: "👤 દર્દીનું પૂરું નામ *",
    namePlaceholder: "દા.ત. રમેશ વર્મા",
    ageLabel: "🎂 ઉંમર (વર્ષ) *",
    genderLabel: "⚧ જાતિ *",
    genderMale: "પુરુષ (Male)",
    genderFemale: "સ્ત્રી (Female)",
    genderOther: "અન્ય (Other)",
    phoneLabel: "📱 મોબાઈલ નંબર",
    assistLabel: "♿ દર્દી સહાય મોડ",
    assistVoice: "અવાજ અને ચિત્ર મોડ (સહાયક મોડ)",
    assistStandard: "સામાન્ય ડિજિટલ મોડ",
    startIntakeBtn: "🚀 તપાસ શરૂ કરો ➔",
    editReg: "✏️ વિગત બદલો",
    stepProgress: "પગલું {step} / 11",
    listenBtn: "🔊 સવાલ સાંભળો",
    tapToSpeak: "🎙️ બોલીને જણાવો",
    listeningWait: "સાંભળી રહ્યા છીએ... તમારી ભાષામાં બોલો",
    contradictionTitle: "⚠️ રીઅલ-ટાઇમ તબીબી વિરોધાભાસ ઓળખ",
    contradictionHint: "AI જોખમી દવાઓ અને લક્ષણો ઓળખે છે...",
    caseSheetTitle: "📋 સ્વચાલિત કેસ હિસ્ટ્રી",
    lblCC: "મુખ્ય તકલીફ",
    lblDuration: "દુખાવાની તીવ્રતા અને સમય",
    lblSigns: "સાથે અન્ય લક્ષણો",
    lblPast: "જૂની બીમારી (ડાયાબિટીસ અને બીપી)",
    lblDocs: "રિપોર્ટ અને જૂના કાગળો",
    lblMeds: "રોજિંદી દવાઓ",
    lblAllergy: "દવાની એલર્જી",
    lblLifestyle: "જીવનશૈલી અને પારિવારિક ઇતિહાસ",
    valWaitingSymptom: "લક્ષણ પસંદગીની રાહ...",
    valNotAnswered: "હજુ જવાબ આપ્યો નથી",
    valNoneReported: "કંઈ નથી",
    valNegative: "ના / સામાન્ય",
    valNoDocs: "કોઈ રિપોર્ટ નથી",
    valNone: "કંઈ નથી",
    valStandard: "સામાન્ય",
    submitCaseBtn: "🚀 ડૉક્ટર તપાસ માટે મોકલો",
    submitNotice: "વિગતો સુરક્ષિત રીતે ડૉક્ટર પાસે પહોંચશે.",
    thankYouTitle: "આભાર",
    thankYouSub: "તમારી વિગતો સફળતાપૂર્વક નોંધાઈ ગઈ છે.",
    tokenLabel: "🎫 ટોકન આઈડી:",
    waitHeading: "કૃપા કરીને તમારો વારો આવે ત્યાં સુધી રાહ જુઓ",
    waitMsg: "ડૉક્ટર ટૂંક સમયમાં તમને બોલાવશે.",
    redirectMsg: "નવા દર્દીની નોંધણી પર પાછા જવાનો સમય",
    nextPatientBtn: "➕ આગામી દર્દીની નોંધણી કરો",
    spokenThankYou: "આભાર. તમારી નોંધણી પૂર્ણ થઈ છે. ડૉક્ટર ટૂંક સમયમાં બોલાવશે.",
    spokenVerified: "ડૉક્ટરે તમારા કેસની તપાસ કરી છે. દવાઓ તૈયાર છે.",
    verifiedBadge: "ડૉક્ટર દ્વારા પ્રમાણિત",
    verifiedTitle: "🎉 ડૉક્ટર દ્વારા તપાસ પૂર્ણ થઈ ગઈ છે!",
    docDiagnosisLabel: "🩺 ડૉક્ટરનું નિદાન:",
    docRxLabel: "💊 પ્રિસ્ક્રિપ્શન (Rx):",
    docAdviceLabel: "📝 ડૉક્ટરની સલાહ:",
    printRxBtn: "🖨️ પ્રિસ્ક્રિપ્શન પ્રિન્ટ કરો",
    waitingInQueue: "⏳ ડૉક્ટરની રાહ જોવાઈ રહી છે...",
    trackModalTitle: "દર્દી કેસ અને દવાઓ તપાસો",
    searchBtn: "શોધો",
    symptomChest: "છાતીમાં દુખાવો કે દબાણ",
    symptomChestSub: "તીવ્ર દબાણ, ગભરામણ કે પરસેવો",
    symptomStomach: "પેટમાં બળતરા કે એસિડિટી",
    symptomStomachSub: "ઉલટી, ખાટા ઓડકાર કે દુખાવો",
    symptomFever: "તાવ અને ઉધરસ",
    symptomFeverSub: "ધ્રૂજારી સાથે તાવ કે કફ",
    symptomHeadache: "તીવ્ર માથાનો દુખાવો અને ચક્કર",
    symptomHeadacheSub: "આધાશીશી અથવા ચક્કર આવવા",
    symptomJoint: "સાંધા અને હાડકાનો દુખાવો",
    symptomJointSub: "ઘૂંટણમાં સોજો અથવા જકડાઈ જવું",
    symptomOther: "સામાન્ય બીમારી / અન્ય",
    symptomOtherSub: "અન્ય કોઈ શારીરિક તકલીફ",
    mildIntensity: "હળવો દુખાવો (1 થી 3)",
    modIntensity: "મધ્યમ દુખાવો (4 થી 6)",
    sevIntensity: "અસહ્ય તીવ્ર (7 થી 10)",
    charHeavy: "ભારે વજન જેવું",
    charHeavySub: "છાતી પર વજન રાખ્યું હોય તેવું",
    charBurning: "બળતરા જેવું",
    charBurningSub: "પેટ કે છાતીમાં તીવ્ર બળતરા",
    charSharp: "સોય જેવી તીક્ષ્ણ ચૂંક",
    charSharpSub: "તીવ્ર દુખાવો",
    charDull: "સતત ધીમો દુખાવો",
    charDullSub: "લાંબા સમયથી રહેતો દુખાવો",
    durToday: "આજે જ શરૂ થયું (< 24 કલાક)",
    durTodaySub: "થોડા કલાકો પહેલાં",
    durDays: "2 થી 4 દિવસથી",
    durDaysSub: "કેટલાક દિવસોથી સતત",
    durWeeks: "1 થી 2 અઠવાડિયાથી",
    durWeeksSub: "એક કે બે અઠવાડિયાથી",
    durMonth: "1 મહિનાથી વધુ સમયથી",
    durMonthSub: "ઘણી જૂની તકલીફ",
    yesText: "હા (YES)",
    noText: "ના (NO)",
    yesSub: "હા, મને છે",
    noSub: "ના, નથી",
    skipDocBtn: "⏭️ રિપોર્ટ નથી (આગળ વધો)",
    uploadDocTitle: "જૂનો રિપોર્ટ અપલોડ કરો (વૈકલ્પિક)",
    uploadDocSub: "ફાઇલ: JPG, PNG, PDF (મહત્તમ 10MB)"
  }
};

// Pointer Question Prompts across all 7 languages
const POINTER_PROMPTS = {
  en: {
    regWelcome: "Welcome to PatientCare AI. Please choose your language and register to begin.",
    step1_title: "1. What is your main health trouble today?",
    step1_sub: "Please tap the icon that matches what you feel:",
    step2_title: "2. How severe is the pain and what type of sensation is it?",
    step2_sub: "Select pain intensity and nature:",
    step3_title: "3. How long have you been having this trouble?",
    step3_sub: "Select onset duration:",
    step4_title: "Clinical Follow-up 1: Associated Symptoms & Radiation",
    step4_chest: "Does the chest pain spread to your left arm, shoulder, neck, or jaw? Any cold sweating?",
    step4_stomach: "Does burning or pain spread to your back? Any nausea, acid reflux, or vomiting?",
    step4_fever: "Is fever accompanied by severe shivering chills, phlegm cough, or chest congestion?",
    step4_head: "Is there blurred vision, dizziness, or weakness in your hands or legs?",
    step4_joint: "Is there visible joint swelling, redness, or stiff joints in the morning?",
    step4_other: "Is this symptom causing shortness of breath or dizziness?",
    step5_title: "Clinical Follow-up 2: Triggers, Red Flags & Past Episodes",
    step5_chest: "Does chest heaviness get worse when walking or climbing stairs? Has this happened before?",
    step5_stomach: "Does pain worsen on an empty stomach or after spicy meals? Any dark black stools?",
    step5_fever: "Has high fever lasted continuously for more than 3 days without relief from medicine?",
    step5_head: "Was this a sudden, explosive severe headache with neck stiffness or confusion?",
    step5_joint: "Is it difficult to walk or bear weight on the joints without support?",
    step5_other: "Has this exact problem occurred previously, or required emergency hospital care?",
    step6_title: "6. Past Medical History: Are you a Sugar (Diabetes) patient?",
    step6_sub: "Do you have high blood glucose diagnosed by a doctor?",
    step7_title: "7. Past Medical History: Do you have High Blood Pressure (BP) or Heart trouble?",
    step7_sub: "Have you ever been diagnosed with hypertension or heart disease?",
    step8_title: "8. Past Medical History & Lab Reports: Do you have old reports or doctor prescriptions?",
    step8_sub: "Upload a photo or PDF of your lab report, ECG, or previous prescription (Optional):",
    step9_title: "9. Are you taking regular daily medicines or pain relief pills?",
    step9_sub: "Any daily tablets or painkillers like Ibuprofen, Combiflam, Aspirin?",
    step10_title: "10. Do you have any known allergy to any medicine or injection?",
    step10_sub: "Any skin rash, swelling, or breathing issue from antibiotics or painkillers?",
    step11_title: "11. Any family history of heart disease, or do you consume tobacco?",
    step11_sub: "Lifestyle and family risk assessment:"
  },
  hi: {
    regWelcome: "पेशेंटकेयर एआई में आपका स्वागत है। कृपया अपनी भाषा चुनें और पंजीकरण करें।",
    step1_title: "1. आज आपको क्या मुख्य शारीरिक तकलीफ हो रही है?",
    step1_sub: "कृपया नीचे दिए गए चित्र को छूकर चुनें:",
    step2_title: "2. दर्द कितना तेज है और किस तरह का महसूस हो रहा है?",
    step2_sub: "दर्द की तीव्रता और प्रकार चुनें:",
    step3_title: "3. यह तकलीफ आपको कितने समय से हो रही है?",
    step3_sub: "समय अवधि चुनें:",
    step4_title: "क्लिनिकल फॉलो-अप 1: साथ में अन्य लक्षण व फैलाव",
    step4_chest: "क्या सीने का दर्द बाएं हाथ, कंधे, गर्दन या जबड़े में जा रहा है? क्या ठंडा पसीना आ रहा है?",
    step4_stomach: "क्या पेट की जलन या दर्द पीठ की तरफ जाता है? क्या उल्टी, जी मिचलाना या खट्टी डकार है?",
    step4_fever: "क्या तेज कंपकंपी के साथ बुखार, खांसी में बलगम या सांस फूलने की समस्या है?",
    step4_head: "क्या आंखों के सामने धुंधलापन, चक्कर आना या अंगों में कमजोरी महसूस हो रही है?",
    step4_joint: "क्या जोड़ों में सूजन, लालिमा या सुबह उठने पर जोड़ों में तेज जकड़न होती है?",
    step4_other: "क्या इस परेशानी के साथ सांस फूलने या चक्कर आने की समस्या है?",
    step5_title: "क्लिनिकल फॉलो-अप 2: दर्द बढ़ने के कारण व पूर्व इतिहास",
    step5_chest: "क्या चलने या सीढ़ियां चढ़ने पर सीने का भारीपन बढ़ता है? क्या पहले कभी ऐसा हुआ था?",
    step5_stomach: "क्या खाली पेट या तीखा खाने से जलन बढ़ती है? क्या काले रंग का शौच हुआ?",
    step5_fever: "क्या 3 दिन से ज्यादा से लगातार तेज बुखार आ रहा है जो दवा से भी नहीं उतर रहा?",
    step5_head: "क्या अचानक असहनीय तेज सिरदर्द हुआ है साथ में गर्दन में अकड़न है?",
    step5_joint: "क्या बिना सहारे के चलना या जोड़ों पर वजन डालना बहुत मुश्किल हो गया है?",
    step5_other: "क्या यह तकलीफ पहले भी कभी हुई थी या अस्पताल में भर्ती होना पड़ा था?",
    step6_title: "6. पुराना इतिहास: क्या आपको शुगर (डायबिटीज) की बीमारी है?",
    step6_sub: "क्या डॉक्टर ने खून में शुगर की बीमारी बताई है?",
    step7_title: "7. पुराना इतिहास: क्या आपको ब्लड प्रेशर (बीपी) या दिल की बीमारी है?",
    step7_sub: "क्या पहले कभी बीपी की जांच में अधिक रक्तचाप या दिल का रोग आया है?",
    step8_title: "8. पुरानी मेडिकल रिपोर्ट व पर्चे: क्या आपके पास कोई पुरानी जांच रिपोर्ट या पर्चा है?",
    step8_sub: "पुरानी रिपोर्ट, ईसीजी या डॉक्टर के पर्चे की फोटो अपलोड करें (वैकल्पिक):",
    step9_title: "9. क्या आप कोई रोज की दवा या दर्द निवारक गोली ले रहे हैं?",
    step9_sub: "जैसे इबुप्रोफेन, कॉम्बीफ्लेम, एस्पिरिन या बीपी/शुगर की गोली:",
    step10_title: "10. क्या आपको किसी दवा या सुई से कोई एलर्जी है?",
    step10_sub: "दवा खाने से शरीर पर लाल चकत्ते, खुजली या सांस की दिक्कत हुई हो?",
    step11_title: "11. क्या परिवार में किसी को दिल का दौरा पड़ा है, या आप बीड़ी/तंबाकू लेते हैं?",
    step11_sub: "पारिवारिक इतिहास और जीवनशैली की जांच:"
  },
  ta: {
    regWelcome: "PatientCare AI-க்கு வரவேற்கிறோம். தயவுசெய்து பதிவு செய்யவும்.",
    step1_title: "1. இன்று உங்களுக்கு என்ன உடல்நல பிரச்சனை?",
    step1_sub: "பொருத்தமான குறியீட்டைத் தேர்ந்தெடுக்கவும்:",
    step2_title: "2. வலியின் தீவிரம் எப்படி உள்ளது?",
    step2_sub: "தீவிரத்தைத் தேர்ந்தெடுக்கவும்:",
    step3_title: "3. இந்த பிரச்சனை எத்தனை நாட்களாக உள்ளது?",
    step3_sub: "கால அளவைத் தேர்ந்தெடுக்கவும்:",
    step4_title: "மருத்துவ பரிசோதனை 1: தொடர்புடைய அறிகுறிகள்",
    step4_chest: "நெஞ்சு வலி இடது கை அல்லது தாடைக்கு பரவுகிறதா? வியர்க்கிறதா?",
    step4_stomach: "எரியும் வலி முதுகுக்கு பரவுகிறதா? வாந்தி உள்ளதா?",
    step4_fever: "குளிர்க்காய்ச்சல் அல்லது மூச்சுத்திணறல் உள்ளதா?",
    step4_head: "பார்வை மங்கலாக உள்ளதா அல்லது மயக்கம் வருகிறதா?",
    step4_joint: "மூட்டுகளில் வீக்கம் அல்லது காலையில் இறுக்கம் உள்ளதா?",
    step4_other: "மூச்சுத்திணறல் அல்லது மயக்கம் உள்ளதா?",
    step5_title: "மருத்துவ பரிசோதனை 2: தீவிர எச்சரிக்கை",
    step5_chest: "நடக்கும் போது அல்லது படிக்கட்டுகளில் ஏறும் போது நெஞ்சு வலி அதிகரிக்கிறதா?",
    step5_stomach: "வெறும் வயிற்றில் வலி அதிகரிக்கிறதா? கருப்பு மலம் வெளியேறியதா?",
    step5_fever: "3 நாட்களுக்கு மேலாக தொடர்ந்து காய்ச்சல் உள்ளதா?",
    step5_head: "திடீரென மிகக் கடுமையான தலைவலி ஏற்பட்டதா?",
    step5_joint: "நடக்க முடியாத அளவுக்கு வலி உள்ளதா?",
    step5_other: "முன்பு எப்போதாவது அவசர சிகிச்சை தேவைப்பட்டதா?",
    step6_title: "6. முந்தைய வரலாறு: உங்களுக்கு சர்க்கரை நோய் உள்ளதா?",
    step6_sub: "நீரிழிவு நோய் உள்ளதா?",
    step7_title: "7. முந்தைய வரலாறு: உங்களுக்கு ரத்த அழுத்தம் (BP) உள்ளதா?",
    step7_sub: "இதய நோய் உள்ளதா?",
    step8_title: "8. பழைய மருத்துவ பரிசோதனை அறிக்கைகள் உள்ளதா?",
    step8_sub: "அறிக்கையை பதிவேற்றவும் (விருப்பத்தேர்வு):",
    step9_title: "9. தினமும் ஏதேனும் வலி மாத்திரைகள் எடுக்கிறீர்களா?",
    step9_sub: "தினசரி மருந்துகள்:",
    step10_title: "10. ஏதேனும் மருந்து ஒவ்வாமை (Allergy) உள்ளதா?",
    step10_sub: "மருந்து ஒவ்வாமை:",
    step11_title: "11. குடும்பத்தில் யாருக்கேனும் இதய நோய் உள்ளதா?",
    step11_sub: "வாழ்க்கை முறை:"
  },
  te: {
    regWelcome: "PatientCare AI కి స్వాగతం. దయచేసి వివరాలు నమోదు చేయండి.",
    step1_title: "1. ఈ రోజు మీకు ప్రధాన సమస్య ఏమిటి?",
    step1_sub: "సరిపోయే చిత్రాన్ని తాకండి:",
    step2_title: "2. నొప్పి తీవ్రత ఎలా ఉంది?",
    step2_sub: "తీవ్రతను ఎంచుకోండి:",
    step3_title: "3. ఈ సమస్య ఎన్ని రోజుల నుంచి ఉంది?",
    step3_sub: "సమయాన్ని ఎంచుకోండి:",
    step4_title: "క్లినికల్ ఫాలో-అప్ 1: సంబంధిత లక్షణాలు",
    step4_chest: "ఛాతీ నొప్పి ఎడమ చేతికి లేదా దవడకు వ్యాపిస్తుందా? చెమటలు పడుతున్నాయా?",
    step4_stomach: "కడుపు మంట లేదా నొప్పి వెనుకకు వ్యాపిస్తుందా? వాంతులు ఉన్నాయా?",
    step4_fever: "వణుకుతో కూడిన జ్వరం లేదా శ్వాస ఆడకపోవటం ఉందా?",
    step4_head: "కళ్ళు తిరగడం లేదా చూపు మసకబారడం ఉందా?",
    step4_joint: "కీళ్ల వాపు లేదా ఉదయం పూట బిగుతుగా ఉండటం ఉందా?",
    step4_other: "శ్వాస ఆడకపోవటం లేదా మైకం ఉందా?",
    step5_title: "క్లినికల్ ఫాలో-అప్ 2: తీవ్రత మరియు గత చరిత్ర",
    step5_chest: "నడిచేటప్పుడు లేదా మెట్లు ఎక్కేటప్పుడు ఛాతీ నొప్పి పెరుగుతుందా?",
    step5_stomach: "ఖాళీ కడుపుతో ఉన్నప్పుడు మంట పెరుగుతుందా? నల్లటి విరేచనాలు అయ్యాయా?",
    step5_fever: "3 రోజులకు పైగా నిరంతరం జ్వరం తగ్గకుండా ఉందా?",
    step5_head: "హఠాత్తుగా తీవ్రమైన తలనొప్పి మరియు మెడ పట్టేయడం జరిగిందా?",
    step5_joint: "ఆధారం లేకుండా నడవడం చాలా కష్టంగా ఉందా?",
    step5_other: "గతంలో ఎప్పుడైనా ఆసుపత్రిలో చేరాల్సి వచ్చిందా?",
    step6_title: "6. గత చరిత్ర: మీకు షుగర్ (డయాబెటిస్) వ్యాధి ఉందా?",
    step6_sub: "షుగర్ లెవల్స్ ఎక్కువా?",
    step7_title: "7. గత చరిత్ర: మీకు రక్తపోటు (BP) లేదా గుండె సమస్య ఉందా?",
    step7_sub: "బీపీ ఉందా?",
    step8_title: "8. పాత ల్యాబ్ రిపోర్టులు లేదా మందుల చీటీలు ఉన్నాయా?",
    step8_sub: "రిపోర్టును అప్‌లోడ్ చేయండి (ఐచ్ఛికం):",
    step9_title: "9. మీరు రోజూ ఏవైనా మందులు లేదా పెయిన్ కిల్లర్స్ వాడుతున్నారా?",
    step9_sub: "రోజువారీ మందులు:",
    step10_title: "10. ఏదైనా మందుతో మీకు అలెర్జీ ఉందా?",
    step10_sub: "మందుల అలెర్జీ:",
    step11_title: "11. కుటుంబంలో ఎవరికైనా గుండెజబ్బు ఉందా?",
    step11_sub: "కుటుంబ చరిత్ర:"
  },
  bn: {
    regWelcome: "PatientCare AI-তে স্বাগতম। দয়া করে তথ্য দিয়ে শুরু করুন।",
    step1_title: "1. আজ আপনার কী শারীরিক সমস্যা হচ্ছে?",
    step1_sub: "নিচের ছবিতে স্পর্শ করে বেছে নিন:",
    step2_title: "2. ব্যথার তীব্রতা কেমন?",
    step2_sub: "তীব্রতা বেছে নিন:",
    step3_title: "3. কত দিন ধরে এই সমস্যা হচ্ছে?",
    step3_sub: "সময়কাল বেছে নিন:",
    step4_title: "ক্লিনিক্যাল ফলো-আপ ১: আনুষঙ্গিক লক্ষণ",
    step4_chest: "বুকে ব্যথা কি বাঁ হাত, কাঁধ বা চোয়ালে ছড়াচ্ছে? ঘাম হচ্ছে কি?",
    step4_stomach: "পেটে জ্বালা বা ব্যথা কি পিঠের দিকে ছড়াচ্ছে? বমি হচ্ছে কি?",
    step4_fever: "কাঁপুনি দিয়ে জ্বর বা বুকে কফ ও শ্বাসকষ্ট আছে কি?",
    step4_head: "চোখে ঝাপসা দেখা বা মাথা ঘোরার সমস্যা আছে?",
    step4_joint: "জয়েন্টে ফোলাভাব বা সকালে অসাড়তা আছে কি?",
    step4_other: "শ্বাসকষ্ট বা মাথা ঘোরার সমস্যা হচ্ছে কি?",
    step5_title: "ক্লিনিক্যাল ফলো-আপ ২: তীব্রতা ও পূর্ব ইতিহাস",
    step5_chest: "হাঁটার সময় কি বুকের চাপ বা ব্যথা বেড়ে যায়? আগে কি এমন হয়েছিল?",
    step5_stomach: "খালি পেটে বা ঝাল খেলে কি জ্বালা বাড়ে? কালো পায়খানা হয়েছে?",
    step5_fever: "৩ দিনের বেশি সময় ধরে কি ওষুধেও জ্বর কমছে না?",
    step5_head: "হঠাৎ প্রচণ্ড তীব্র মাথাব্যথা এবং ঘাড়ে শক্ত ভাব হয়েছে কি?",
    step5_joint: "ভর দিয়ে হাঁটা কি সম্পূর্ণ অসম্ভব হয়ে গেছে?",
    step5_other: "আগে কি কখনো এই সমস্যার জন্য হাসপাতালে ভর্তি হতে হয়েছিল?",
    step6_title: "6. পূর্বের ইতিহাস: আপনার কি সুগার (ডায়াবেটিস) আছে?",
    step6_sub: "রক্তে শর্করার মাত্রা বেশি?",
    step7_title: "7. পূর্বের ইতিহাস: আপনার কি ব্লাড প্রেসার (BP) বা হার্টের সমস্যা আছে?",
    step7_sub: "প্রেসার আছে কি?",
    step8_title: "8. আপনার কি কোনো পূর্বের মেডিকেল রিপোর্ট বা প্রেসক্রিপশন আছে?",
    step8_sub: "রিপোর্ট আপলোড করুন (ঐচ্ছিক):",
    step9_title: "9. আপনি কি প্রতিদিন কোনো ব্যথানাশক বা অন্যান্য ওষুধ খান?",
    step9_sub: "নিয়মিত ওষুধ:",
    step10_title: "10. কোনো ওষুধে আপনার অ্যালার্জি আছে কি?",
    step10_sub: "ওষুধের অ্যালার্জি:",
    step11_title: "11. পরিবারে কারো হৃদরোগের ইতিহাস আছে কি?",
    step11_sub: "পারিবারিক ইতিহাস:"
  },
  mr: {
    regWelcome: "PatientCare AI मध्ये आपले स्वागत आहे. कृपया नोंदणी करा.",
    step1_title: "1. आज तुम्हाला नेमका काय त्रास होत आहे?",
    step1_sub: "खालील चिन्हावर क्लिक करा:",
    step2_title: "2. वेदना किती तीव्र आहे आणि कशी जाणवते?",
    step2_sub: "तीव्रता व प्रकार निवडा:",
    step3_title: "3. हा त्रास किती दिवसांपासून होत आहे?",
    step3_sub: "कालावधी निवडा:",
    step4_title: "क्लिनिकल फॉलो-अप १: सोबत इतर लक्षणे",
    step4_chest: "छातीत दुखणे डाव्या हाताकडे, खांद्याकडे किंवा जबड्याकडे जाते का? घाम येतोय का?",
    step4_stomach: "पोटात जळजळ किंवा वेदना पाठीकडे जाते का? उलटी किंवा मळमळ होते का?",
    step4_fever: "थंडी वाजून ताप येतो का किंवा खोकल्यात कफ व धाप लागते का?",
    step4_head: "डोळ्यांसमोर अंधारी येणे किंवा चक्कर येते का?",
    step4_joint: "सांध्यांना सूज आली आहे का किंवा सकाळी सांधे आखडतात का?",
    step4_other: "धाप लागणे किंवा चक्कर येण्याचा त्रास होतोय का?",
    step5_title: "क्लिनिकल फॉलो-अप २: वेदना वाढण्याची कारणे",
    step5_chest: "चालताना किंवा जिना चढताना छातीवरील दाब वाढतो का? आधी असा त्रास झाला होता का?",
    step5_stomach: "उपाशीपोटी जळजळ वाढते का? काळ्या रंगाचे शौचास झाले आहे का?",
    step5_fever: "औषध घेऊनही ३ दिवसांपेक्षा जास्त काळ सतत ताप भरतोय का?",
    step5_head: "अचानक अतिशय तीव्र डोकेदुखी व मानेमध्ये ताठरता आली आहे का?",
    step5_joint: "आधाराशिवाय चालणे किंवा सांध्यावर वजन देणे कठीण झाले आहे का?",
    step5_other: "आधी कधी या त्रासासाठी रुग्णालयात दाखल व्हावे लागले होते का?",
    step6_title: "6. जुना आजार: तुम्हाला मधुमेहाचा (शुगरचा) आजार आहे का?",
    step6_sub: "शुगर जास्त आहे का?",
    step7_title: "7. जुना आजार: तुम्हाला ब्लड प्रेशर (BP) किंवा हृदयाचा त्रास आहे का?",
    step7_sub: "बीपीचा त्रास आहे का?",
    step8_title: "8. जुनी तपासणी रिपोर्ट किंवा औषधांची चिठ्ठी आहे का?",
    step8_sub: "रिपोर्ट अपलोड करा (ऐच्छिक असल्यास):",
    step9_title: "9. तुम्ही रोजची काही औषधे किंवा पेनकिलर गोळ्या घेता का?",
    step9_sub: "दररोजची औषधे:",
    step10_title: "10. कोणत्याही औषधाची तुम्हाला ॲलर्जी आहे का?",
    step10_sub: "गोळ्यांची ॲलर्जी:",
    step11_title: "11. कुटुंबात कुणाला हृदयविकाराचा इतिहास आहे का?",
    step11_sub: "कौटुंबिक माहिती:"
  },
  gu: {
    regWelcome: "PatientCare AI માં આપનું સ્વાગત છે. કૃપા કરીને નોંધણી કરો.",
    step1_title: "1. આજે તમને શું મુખ્ય તકલીફ છે?",
    step1_sub: "યોગ્ય નિશાની પર ક્લિક કરો:",
    step2_title: "2. દુખાવો કેટલો તીવ્ર છે?",
    step2_sub: "તીવ્રતા પસંદ કરો:",
    step3_title: "3. આ તકલીફ કેટલા સમયથી છે?",
    step3_sub: "સમય પસંદ કરો:",
    step4_title: "ક્લિનિકલ ફોલો-અપ 1: સાથે અન્ય લક્ષણો",
    step4_chest: "છાતીનો દુખાવો ડાબા હાથ, ગરદન કે જડબા તરફ જાય છે? પરસેવો વળે છે?",
    step4_stomach: "પેટની બળતરા પીઠ તરફ જાય છે? ઉબકા કે ઉલટી છે?",
    step4_fever: "ધ્રૂજારી સાથે તાવ, કફ કે શ્વાસ લેવામાં તકલીફ છે?",
    step4_head: "આંખે અંધારા કે ચક્કર આવે છે?",
    step4_joint: "સાંધામાં સોજો કે સવારે જકડાઈ જવું થાય છે?",
    step4_other: "શ્વાસ લેવામાં તકલીફ કે ચક્કર આવે છે?",
    step5_title: "ક્લિનિકલ ફોલો-અપ 2: વધવાના કારણો",
    step5_chest: "ચાલતી વખતે છાતીમાં દબાણ વધે છે? પહેલાં ક્યારેય આવું થયું છે?",
    step5_stomach: "ખાલી પેટે કે તીખું ખાવાથી બળતરા વધે છે? કાળો મળ આવ્યો?",
    step5_fever: "દવા લેવા છતાં 3 દિવસથી વધુ તાવ રહે છે?",
    step5_head: "અચાનક અસહ્ય તીવ્ર માથાનો દુખાવો થયો છે?",
    step5_joint: "ટેકા વગર ચાલવું ખૂબ મુશ્કેલ બન્યું છે?",
    step5_other: "પહેલાં ક્યારેય હોસ્પિટલમાં દાખલ થવું પડ્યું હતું?",
    step6_title: "6. જૂનો ઇતિહાસ: તમને ડાયાબિટીસ (શુગર) છે?",
    step6_sub: "ડૉક્ટરે શુગરની બીમારી કહી છે?",
    step7_title: "7. જૂનો ઇતિહાસ: તમને બ્લડ પ્રેશર (BP) કે હૃદયની તકલીફ છે?",
    step7_sub: "બીપીની બીમારી છે?",
    step8_title: "8. જૂનો લેબ રિપોર્ટ કે પ્રિસ્ક્રિપ્શન છે?",
    step8_sub: "રિપોર્ટ અપલોડ કરો (વૈકલ્પિક):",
    step9_title: "9. તમે દરરોજ કોઈ દવા કે પેઇન કિલર ગોળી લો છો?",
    step9_sub: "દરરોજની દવાઓ:",
    step10_title: "10. કોઈ દવાની તમને એલર્જી છે?",
    step10_sub: "દવાની એલર્જી:",
    step11_title: "11. પરિવારમાં કોઈને હૃદયરોગ થયો છે?",
    step11_sub: "પારિવારિક ઇતિહાસ:"
  }
};

// ==============================================================================
// INITIALIZATION
// ==============================================================================
window.addEventListener("DOMContentLoaded", () => {
  loadStoredCases();
  initVoiceRecognition();
  updateDoctorStats();
  applyLanguageToEntireUI(currentLanguage);
  setupVerificationSyncListeners();
});

// Broadcast / Sync Listeners for Live Updates
function setupVerificationSyncListeners() {
  if (patientCareChannel) {
    patientCareChannel.onmessage = (event) => {
      if (event.data && event.data.type === "CASE_VERIFIED") {
        handleCaseVerified(event.data.caseObj);
      }
    };
  }

  window.addEventListener("storage", (e) => {
    if (e.key === "patientcare_last_verified" && e.newValue) {
      try {
        const verifiedCase = JSON.parse(e.newValue);
        handleCaseVerified(verifiedCase);
      } catch (err) {}
    }
  });

  window.addEventListener("caseVerified", (e) => {
    if (e.detail) {
      handleCaseVerified(e.detail);
    }
  });
}

// Gentle pleasant Web Audio chime when doctor verifies
function playVerificationChime() {
  try {
    const ctx = new (window.AudioContext || window.webkitAudioContext)();
    const now = ctx.currentTime;

    const osc1 = ctx.createOscillator();
    const gain1 = ctx.createGain();
    osc1.type = "sine";
    osc1.frequency.setValueAtTime(523.25, now); // C5
    gain1.gain.setValueAtTime(0.2, now);
    gain1.gain.exponentialRampToValueAtTime(0.01, now + 0.35);
    osc1.connect(gain1);
    gain1.connect(ctx.destination);
    osc1.start(now);
    osc1.stop(now + 0.35);

    const osc2 = ctx.createOscillator();
    const gain2 = ctx.createGain();
    osc2.type = "sine";
    osc2.frequency.setValueAtTime(659.25, now + 0.15); // E5
    gain2.gain.setValueAtTime(0.25, now + 0.15);
    gain2.gain.exponentialRampToValueAtTime(0.001, now + 0.7);
    osc2.connect(gain2);
    gain2.connect(ctx.destination);
    osc2.start(now + 0.15);
    osc2.stop(now + 0.7);
  } catch (e) {
    // Audio context not allowed without interaction
  }
}

async function loadStoredCases() {
  try {
    const res = await fetch("/api/cases");
    if (res.ok) {
      const data = await res.json();
      allCases = data.cases || [];
    } else {
      throw new Error("API not reachable");
    }
  } catch (err) {
    const local = localStorage.getItem("patientcare_cases");
    if (local) {
      allCases = JSON.parse(local);
    }
  }
  updateDoctorStats();
  renderCasesTable(allCases);
}

// ==============================================================================
// DYNAMIC FULL-PROTOTYPE UI LOCALIZATION ENGINE
// ==============================================================================
function applyLanguageToEntireUI(langCode) {
  currentLanguage = langCode;
  const t = UI_TRANSLATIONS[langCode] || UI_TRANSLATIONS.en;

  // 1. Header Elements
  const tagline = document.getElementById("headerBrandTagline");
  if (tagline) tagline.textContent = t.tagline;

  const audioText = document.getElementById("audioText");
  if (audioText) {
    audioText.innerHTML = isAudioAssistanceOn ? t.voiceOn : t.voiceOff;
  }

  const docLoginBtn = document.getElementById("docLoginTriggerBtn");
  if (docLoginBtn) {
    const pendingCount = allCases.filter(c => c.doctor_status !== "Verified").length;
    docLoginBtn.innerHTML = `${t.docLogin} <span id="headerPendingBadge" class="mini-badge">${pendingCount}</span>`;
  }

  const trackBtnText = document.getElementById("trackStatusBtnText");
  if (trackBtnText) trackBtnText.textContent = t.trackCase;

  // 2. Registration Card
  const regTitle = document.getElementById("regCardTitle");
  if (regTitle) regTitle.textContent = t.regTitle;

  const regSub = document.getElementById("regCardSub");
  if (regSub) regSub.textContent = t.regSub;

  const regLangLabel = document.getElementById("regLangLabel");
  if (regLangLabel) regLangLabel.innerHTML = `<span>🌐</span> ${t.chooseLang}`;

  const lblDemoPresets = document.getElementById("lblDemoPresets");
  if (lblDemoPresets) lblDemoPresets.textContent = t.demoPresets;

  const presetCardiacBtn = document.getElementById("presetCardiacBtn");
  if (presetCardiacBtn) presetCardiacBtn.textContent = t.presetCardiac;

  const presetGastricBtn = document.getElementById("presetGastricBtn");
  if (presetGastricBtn) presetGastricBtn.textContent = t.presetGastric;

  const presetPediatricBtn = document.getElementById("presetPediatricBtn");
  if (presetPediatricBtn) presetPediatricBtn.textContent = t.presetPediatric;

  const lblRegName = document.getElementById("lblRegName");
  if (lblRegName) lblRegName.innerHTML = `<span>👤</span> ${t.nameLabel}`;

  const regNameInput = document.getElementById("regName");
  if (regNameInput) regNameInput.placeholder = t.namePlaceholder;

  const lblRegAge = document.getElementById("lblRegAge");
  if (lblRegAge) lblRegAge.innerHTML = `<span>🎂</span> ${t.ageLabel}`;

  const lblRegGender = document.getElementById("lblRegGender");
  if (lblRegGender) lblRegGender.innerHTML = `<span>⚧</span> ${t.genderLabel}`;

  const regGenderSelect = document.getElementById("regGender");
  if (regGenderSelect) {
    regGenderSelect.options[0].text = t.genderMale;
    regGenderSelect.options[1].text = t.genderFemale;
    regGenderSelect.options[2].text = t.genderOther;
  }

  const lblRegPhone = document.getElementById("lblRegPhone");
  if (lblRegPhone) lblRegPhone.innerHTML = `<span>📱</span> ${t.phoneLabel}`;

  const lblRegAssistance = document.getElementById("lblRegAssistance");
  if (lblRegAssistance) lblRegAssistance.innerHTML = `<span>♿</span> ${t.assistLabel}`;

  const regPatientType = document.getElementById("regPatientType");
  if (regPatientType) {
    regPatientType.options[0].text = t.assistStandard;
    regPatientType.options[1].text = t.assistVoice;
  }

  const btnStartIntake = document.getElementById("btnStartIntake");
  if (btnStartIntake) btnStartIntake.textContent = t.startIntakeBtn;

  // 3. Patient Active Bar
  const btnEditReg = document.getElementById("btnEditReg");
  if (btnEditReg) btnEditReg.textContent = t.editReg;

  const intakeProgressBadge = document.getElementById("intakeProgressBadge");
  if (intakeProgressBadge) {
    intakeProgressBadge.textContent = t.stepProgress.replace("{step}", currentPointerStep);
  }

  // 4. Voice bar
  const micStatusText = document.getElementById("micStatusText");
  if (micStatusText) micStatusText.textContent = t.tapToSpeak;

  const voiceFeedback = document.getElementById("voiceTranscriptFeedback");
  if (voiceFeedback && !isRecording) voiceFeedback.textContent = t.listeningWait;

  const readQuestionBtn = document.getElementById("readQuestionBtn");
  if (readQuestionBtn) readQuestionBtn.textContent = t.listenBtn;

  // 5. Intelligence Panel (Right Sidebar)
  const lblContradictionTitle = document.getElementById("lblContradictionTitle");
  if (lblContradictionTitle) {
    lblContradictionTitle.innerHTML = `<span style="display:flex; align-items:center; gap:0.4rem; color:#dc2626;">${t.contradictionTitle}</span>`;
  }

  const contradictionHintText = document.getElementById("contradictionHintText");
  if (contradictionHintText && detectedContradictions.length === 0) {
    contradictionHintText.textContent = t.contradictionHint;
  }

  const lblCaseHistoryTitle = document.getElementById("lblCaseHistoryTitle");
  if (lblCaseHistoryTitle) {
    lblCaseHistoryTitle.innerHTML = `<span style="display:flex; align-items:center; gap:0.4rem; color:var(--teal);">${t.caseSheetTitle}</span>`;
  }

  const lblLiveCC = document.getElementById("lblLiveCC");
  if (lblLiveCC) lblLiveCC.textContent = t.lblCC;

  const lblLiveDuration = document.getElementById("lblLiveDuration");
  if (lblLiveDuration) lblLiveDuration.textContent = t.lblDuration;

  const lblLiveSigns = document.getElementById("lblLiveSigns");
  if (lblLiveSigns) lblLiveSigns.textContent = t.lblSigns;

  const lblLivePast = document.getElementById("lblLivePast");
  if (lblLivePast) lblLivePast.textContent = t.lblPast;

  const lblLiveDocs = document.getElementById("lblLiveDocs");
  if (lblLiveDocs) lblLiveDocs.textContent = t.lblDocs;

  const lblLiveMeds = document.getElementById("lblLiveMeds");
  if (lblLiveMeds) lblLiveMeds.textContent = t.lblMeds;

  const lblLiveAllergy = document.getElementById("lblLiveAllergy");
  if (lblLiveAllergy) lblLiveAllergy.textContent = t.lblAllergy;

  const lblLiveLifestyle = document.getElementById("lblLiveLifestyle");
  if (lblLiveLifestyle) lblLiveLifestyle.textContent = t.lblLifestyle;

  const finalSubmitBtn = document.getElementById("finalSubmitBtn");
  if (finalSubmitBtn) finalSubmitBtn.textContent = t.submitCaseBtn;

  const lblSubmitNotice = document.getElementById("lblSubmitNotice");
  if (lblSubmitNotice) lblSubmitNotice.textContent = t.submitNotice;

  // Update Track modal header
  const trackModalHeader = document.getElementById("trackModalHeader");
  if (trackModalHeader) trackModalHeader.textContent = t.trackModalTitle;

  // Re-render the active pointer step so options and buttons translate immediately!
  const intakeView = document.getElementById("pointerIntakeView");
  if (intakeView && intakeView.classList.contains("active")) {
    renderPointerQuestion(currentPointerStep);
  }
}

function selectLanguage(langCode, btnElement) {
  currentLanguage = langCode;
  document.querySelectorAll(".lang-chip").forEach(c => c.classList.remove("active"));
  if (btnElement) btnElement.classList.add("active");

  applyLanguageToEntireUI(langCode);

  const p = POINTER_PROMPTS[langCode] || POINTER_PROMPTS.en;
  speakCurrentText(p.regWelcome);
}

function fillQuickProfile(type) {
  if (type === "cardiac") {
    document.getElementById("regName").value = "Rajesh Kumar";
    document.getElementById("regAge").value = "52";
    document.getElementById("regGender").value = "Male";
    document.getElementById("regPhone").value = "+91 98765 43210";
    selectLanguage('hi', document.querySelector('[data-lang="hi"]'));
  } else if (type === "gastric") {
    document.getElementById("regName").value = "Sunita Devi";
    document.getElementById("regAge").value = "38";
    document.getElementById("regGender").value = "Female";
    document.getElementById("regPhone").value = "+91 94123 78901";
    selectLanguage('hi', document.querySelector('[data-lang="hi"]'));
  } else if (type === "pediatric") {
    document.getElementById("regName").value = "Aarav Patel";
    document.getElementById("regAge").value = "8";
    document.getElementById("regGender").value = "Male";
    document.getElementById("regPhone").value = "+91 97234 11223";
    selectLanguage('gu', document.querySelector('[data-lang="gu"]'));
  }
}

function toggleAssistanceMode(val) {
  activePatient.mode = val;
}

function handleRegistrationSubmit(e) {
  e.preventDefault();

  activePatient.name = document.getElementById("regName").value.trim() || "Ramesh Verma";
  activePatient.age = parseInt(document.getElementById("regAge").value) || 48;
  activePatient.gender = document.getElementById("regGender").value || "Male";
  activePatient.phone = document.getElementById("regPhone").value.trim() || "+91 98765 43210";
  activePatient.language = currentLanguage;
  activePatient.mode = document.getElementById("regPatientType").value || "assisted";

  document.getElementById("activePatientName").textContent = activePatient.name;
  document.getElementById("activePatientMeta").textContent = `${activePatient.age} Yrs • ${activePatient.gender} • ${activePatient.language.toUpperCase()}`;

  document.getElementById("registrationView").classList.remove("active");
  document.getElementById("doctorView").classList.remove("active");
  document.getElementById("pointerIntakeView").classList.add("active");

  currentPointerStep = 1;
  renderPointerQuestion(1);
}

function returnToRegistration() {
  document.getElementById("pointerIntakeView").classList.remove("active");
  document.getElementById("doctorView").classList.remove("active");
  document.getElementById("registrationView").classList.add("active");
  applyLanguageToEntireUI(currentLanguage);
}

// ==============================================================================
// 11-STEP ACCESSIBLE POINTER ENGINE (FULLY LOCALIZED)
// ==============================================================================
function renderPointerQuestion(step) {
  currentPointerStep = step;
  updateStepperIndicator(step);

  const container = document.getElementById("pointerQuestionBox");
  const p = POINTER_PROMPTS[currentLanguage] || POINTER_PROMPTS.en;
  const t = UI_TRANSLATIONS[currentLanguage] || UI_TRANSLATIONS.en;
  const header = document.getElementById("pointerStepHeader");

  const progressBadge = document.getElementById("intakeProgressBadge");
  if (progressBadge) progressBadge.textContent = t.stepProgress.replace("{step}", step);

  // STEP 1: Primary Symptom
  if (step === 1) {
    header.textContent = p.step1_title;
    container.innerHTML = `
      <div class="pointer-question-prompt">
        <div class="pointer-title-main">${p.step1_title}</div>
        <div class="pointer-title-sub">${p.step1_sub}</div>
      </div>

      <div class="symptom-cards-grid">
        <button type="button" class="symptom-tile" onclick="selectSymptom('${escapeQuotes(t.symptomChest)}', '🫀', 'Emergency')">
          <div class="symptom-icon">🫀</div>
          <div>
            <div class="symptom-name">${t.symptomChest}</div>
            <div class="symptom-desc">${t.symptomChestSub}</div>
          </div>
        </button>

        <button type="button" class="symptom-tile" onclick="selectSymptom('${escapeQuotes(t.symptomStomach)}', '🤰', 'Priority')">
          <div class="symptom-icon">🤰</div>
          <div>
            <div class="symptom-name">${t.symptomStomach}</div>
            <div class="symptom-desc">${t.symptomStomachSub}</div>
          </div>
        </button>

        <button type="button" class="symptom-tile" onclick="selectSymptom('${escapeQuotes(t.symptomFever)}', '🌡️', 'Routine')">
          <div class="symptom-icon">🌡️</div>
          <div>
            <div class="symptom-name">${t.symptomFever}</div>
            <div class="symptom-desc">${t.symptomFeverSub}</div>
          </div>
        </button>

        <button type="button" class="symptom-tile" onclick="selectSymptom('${escapeQuotes(t.symptomHeadache)}', '🤕', 'Priority')">
          <div class="symptom-icon">🤕</div>
          <div>
            <div class="symptom-name">${t.symptomHeadache}</div>
            <div class="symptom-desc">${t.symptomHeadacheSub}</div>
          </div>
        </button>

        <button type="button" class="symptom-tile" onclick="selectSymptom('${escapeQuotes(t.symptomJoint)}', '🦵', 'Routine')">
          <div class="symptom-icon">🦵</div>
          <div>
            <div class="symptom-name">${t.symptomJoint}</div>
            <div class="symptom-desc">${t.symptomJointSub}</div>
          </div>
        </button>

        <button type="button" class="symptom-tile" onclick="selectSymptom('${escapeQuotes(t.symptomOther)}', '➕', 'Routine')">
          <div class="symptom-icon">➕</div>
          <div>
            <div class="symptom-name">${t.symptomOther}</div>
            <div class="symptom-desc">${t.symptomOtherSub}</div>
          </div>
        </button>
      </div>
    `;
    speakCurrentText(p.step1_title);

  // STEP 2: Intensity & Nature of Pain
  } else if (step === 2) {
    header.textContent = p.step2_title;
    container.innerHTML = `
      <div class="pointer-question-prompt">
        <div class="pointer-title-main">${p.step2_title}</div>
        <div class="pointer-title-sub">${p.step2_sub}</div>
      </div>

      <div style="margin-bottom:1rem;">
        <label style="font-size:0.85rem; font-weight:700; color:var(--primary); margin-bottom:0.4rem; display:block;">
          ${t.lblDuration}:
        </label>
        <div style="display:grid; grid-template-columns: repeat(3, 1fr); gap:0.75rem;">
          <button type="button" class="btn-pointer-choice" style="background:#f0fdf4; border:2px solid #86efac; padding:1rem;" onclick="selectIntensity('${escapeQuotes(t.mildIntensity)}')">
            <span style="font-size:1.8rem;">🙂</span>
            <span style="font-weight:700; color:#15803d;">${t.mildIntensity}</span>
          </button>
          <button type="button" class="btn-pointer-choice" style="background:#fffbeb; border:2px solid #fde68a; padding:1rem;" onclick="selectIntensity('${escapeQuotes(t.modIntensity)}')">
            <span style="font-size:1.8rem;">😐</span>
            <span style="font-weight:700; color:#b45309;">${t.modIntensity}</span>
          </button>
          <button type="button" class="btn-pointer-choice" style="background:#fef2f2; border:2px solid #fca5a5; padding:1rem;" onclick="selectIntensity('${escapeQuotes(t.sevIntensity)}')">
            <span style="font-size:1.8rem;">😫</span>
            <span style="font-weight:700; color:#b91c1c;">${t.sevIntensity}</span>
          </button>
        </div>
      </div>

      <label style="font-size:0.85rem; font-weight:700; color:var(--primary); margin-bottom:0.4rem; display:block;">
        ${t.lblCC}:
      </label>
      <div class="symptom-cards-grid">
        <button type="button" class="symptom-tile" onclick="selectCharacter('${escapeQuotes(t.charHeavy)}')">
          <div class="symptom-icon">🏋️</div>
          <div>
            <div class="symptom-name">${t.charHeavy}</div>
            <div class="symptom-desc">${t.charHeavySub}</div>
          </div>
        </button>
        <button type="button" class="symptom-tile" onclick="selectCharacter('${escapeQuotes(t.charBurning)}')">
          <div class="symptom-icon">🔥</div>
          <div>
            <div class="symptom-name">${t.charBurning}</div>
            <div class="symptom-desc">${t.charBurningSub}</div>
          </div>
        </button>
        <button type="button" class="symptom-tile" onclick="selectCharacter('${escapeQuotes(t.charSharp)}')">
          <div class="symptom-icon">⚡</div>
          <div>
            <div class="symptom-name">${t.charSharp}</div>
            <div class="symptom-desc">${t.charSharpSub}</div>
          </div>
        </button>
        <button type="button" class="symptom-tile" onclick="selectCharacter('${escapeQuotes(t.charDull)}')">
          <div class="symptom-icon">🩹</div>
          <div>
            <div class="symptom-name">${t.charDull}</div>
            <div class="symptom-desc">${t.charDullSub}</div>
          </div>
        </button>
      </div>
    `;
    speakCurrentText(p.step2_title);

  // STEP 3: Duration & Onset
  } else if (step === 3) {
    header.textContent = p.step3_title;
    container.innerHTML = `
      <div class="pointer-question-prompt">
        <div class="pointer-title-main">${p.step3_title}</div>
        <div class="pointer-title-sub">${p.step3_sub}</div>
      </div>

      <div class="symptom-cards-grid">
        <button type="button" class="symptom-tile" onclick="selectDuration('${escapeQuotes(t.durToday)}')">
          <div class="symptom-icon">⏱️</div>
          <div>
            <div class="symptom-name">${t.durToday}</div>
            <div class="symptom-desc">${t.durTodaySub}</div>
          </div>
        </button>

        <button type="button" class="symptom-tile" onclick="selectDuration('${escapeQuotes(t.durDays)}')">
          <div class="symptom-icon">📅</div>
          <div>
            <div class="symptom-name">${t.durDays}</div>
            <div class="symptom-desc">${t.durDaysSub}</div>
          </div>
        </button>

        <button type="button" class="symptom-tile" onclick="selectDuration('${escapeQuotes(t.durWeeks)}')">
          <div class="symptom-icon">🗓️</div>
          <div>
            <div class="symptom-name">${t.durWeeks}</div>
            <div class="symptom-desc">${t.durWeeksSub}</div>
          </div>
        </button>

        <button type="button" class="symptom-tile" onclick="selectDuration('${escapeQuotes(t.durMonth)}')">
          <div class="symptom-icon">⏳</div>
          <div>
            <div class="symptom-name">${t.durMonth}</div>
            <div class="symptom-desc">${t.durMonthSub}</div>
          </div>
        </button>
      </div>
    `;
    speakCurrentText(p.step3_title);

  // STEP 4: Clinical Follow-up 1 (Associated Symptoms & Radiation)
  } else if (step === 4) {
    let questionText = p.step4_other;
    const symLower = intakeAnswers.symptom.toLowerCase();
    if (symLower.includes("chest") || symLower.includes("सीने") || symLower.includes("நெஞ்சு") || symLower.includes("ఛాతీ") || symLower.includes("বুকে") || symLower.includes("છાતી")) {
      questionText = p.step4_chest;
    } else if (symLower.includes("stomach") || symLower.includes("पेट") || symLower.includes("வயிறு") || symLower.includes("కడుపు") || symLower.includes("পেট") || symLower.includes("પેટ")) {
      questionText = p.step4_stomach;
    } else if (symLower.includes("fever") || symLower.includes("बुखार") || symLower.includes("காய்ச்சல்") || symLower.includes("జ్వరం") || symLower.includes("জ্বর") || symLower.includes("તાવ")) {
      questionText = p.step4_fever;
    } else if (symLower.includes("head") || symLower.includes("सिर") || symLower.includes("தலை") || symLower.includes("తల") || symLower.includes("মাথা") || symLower.includes("માથ")) {
      questionText = p.step4_head;
    } else if (symLower.includes("joint") || symLower.includes("जोड़") || symLower.includes("மூட்டு") || symLower.includes("కీళ్ల") || symLower.includes("জয়েন্ট") || symLower.includes("સાંધા")) {
      questionText = p.step4_joint;
    }

    header.textContent = p.step4_title;
    renderYesNoQuestion(questionText, t.lblSigns, "followup1");

  // STEP 5: Clinical Follow-up 2 (Triggers, Red Flags & Past Episodes)
  } else if (step === 5) {
    let questionText = p.step5_other;
    const symLower = intakeAnswers.symptom.toLowerCase();
    if (symLower.includes("chest") || symLower.includes("सीने") || symLower.includes("நெஞ்சு") || symLower.includes("ఛాతీ") || symLower.includes("বুকে") || symLower.includes("છાતી")) {
      questionText = p.step5_chest;
    } else if (symLower.includes("stomach") || symLower.includes("पेट") || symLower.includes("வயிறு") || symLower.includes("కడుపు") || symLower.includes("পেট") || symLower.includes("પેટ")) {
      questionText = p.step5_stomach;
    } else if (symLower.includes("fever") || symLower.includes("बुखार") || symLower.includes("காய்ச்சல்") || symLower.includes("జ్వరం") || symLower.includes("জ্বর") || symLower.includes("તાવ")) {
      questionText = p.step5_fever;
    } else if (symLower.includes("head") || symLower.includes("सिर") || symLower.includes("தலை") || symLower.includes("తల") || symLower.includes("মাথা") || symLower.includes("માથ")) {
      questionText = p.step5_head;
    } else if (symLower.includes("joint") || symLower.includes("जोड़") || symLower.includes("மூட்டு") || symLower.includes("కీళ్ల") || symLower.includes("জয়েন্ট") || symLower.includes("સાંધા")) {
      questionText = p.step5_joint;
    }

    header.textContent = p.step5_title;
    renderYesNoQuestion(questionText, t.lblSigns, "followup2");

  // STEP 6: Past Medical History - Sugar (Diabetes)
  } else if (step === 6) {
    header.textContent = p.step6_title;
    renderYesNoQuestion(p.step6_title, p.step6_sub, "sugar");

  // STEP 7: Past Medical History - High Blood Pressure (BP) / Heart Condition
  } else if (step === 7) {
    header.textContent = p.step7_title;
    renderYesNoQuestion(p.step7_title, p.step7_sub, "bp");

  // STEP 8: OPTIONAL PAST MEDICAL HISTORY & LAB REPORT UPLOAD
  } else if (step === 8) {
    header.textContent = p.step8_title;
    container.innerHTML = `
      <div class="pointer-question-prompt">
        <div class="pointer-title-main">${p.step8_title}</div>
        <div class="pointer-title-sub">${p.step8_sub}</div>
      </div>

      <div class="upload-box-wrap" onclick="document.getElementById('docFileInput').click()">
        <input type="file" id="docFileInput" style="display:none;" accept="image/*,.pdf" onchange="handleDocumentUpload(event)">
        <div class="upload-box-icon">📤</div>
        <h4 style="font-size:1rem; font-weight:700; color:var(--teal); margin-bottom:0.35rem;">
          ${t.uploadDocTitle}
        </h4>
        <p style="font-size:0.8rem; color:var(--text-muted); margin:0;">
          ${t.uploadDocSub}
        </p>
      </div>

      <div id="uploadedPreviewArea" style="margin-top:0.75rem; text-align:center;">
        ${intakeAnswers.has_documents ? `
          <div style="display:inline-flex; align-items:center; gap:0.5rem; background:#f0fdf4; border:1px solid #86efac; color:#15803d; padding:0.4rem 0.8rem; border-radius:4px; font-weight:600; font-size:0.85rem;">
            <span>📎</span> <span>${escapeHtml(intakeAnswers.doc_name)}</span>
            <span style="color:#16a34a; font-weight:700;">✓ Ready</span>
          </div>
        ` : ''}
      </div>

      <div style="display:flex; justify-content:space-between; align-items:center; margin-top:1.25rem;">
        <button type="button" class="btn btn-outline" onclick="renderPointerQuestion(7)">
          ⬅ Previous
        </button>
        <button type="button" class="btn btn-teal" style="font-weight:700;" onclick="skipOrProceedDocument()">
          ${intakeAnswers.has_documents ? 'Next Step ➔' : t.skipDocBtn}
        </button>
      </div>
    `;
    speakCurrentText(p.step8_title);

  // STEP 9: Daily Medications / Painkillers
  } else if (step === 9) {
    header.textContent = p.step9_title;
    renderYesNoQuestion(p.step9_title, p.step9_sub, "meds");

  // STEP 10: Drug Allergies
  } else if (step === 10) {
    header.textContent = p.step10_title;
    renderYesNoQuestion(p.step10_title, p.step10_sub, "allergies");

  // STEP 11: Family Cardiac History & Lifestyle (Smoking/Tobacco)
  } else if (step === 11) {
    header.textContent = p.step11_title;
    renderYesNoQuestion(p.step11_title, p.step11_sub, "lifestyle");
  }
}

function escapeQuotes(str) {
  return (str || "").replace(/'/g, "\\\\'");
}

function updateStepperIndicator(activeStep) {
  for (let i = 1; i <= TOTAL_POINTER_STEPS; i++) {
    const dot = document.getElementById(`dot${i}`);
    if (dot) {
      if (i < activeStep) {
        dot.className = "step-dot completed";
      } else if (i === activeStep) {
        dot.className = "step-dot active";
      } else {
        dot.className = "step-dot";
      }
    }
  }
}

function selectSymptom(symptomName, icon, initialTriage) {
  intakeAnswers.symptom = symptomName;
  intakeAnswers.symptom_icon = icon;
  intakeAnswers.triage = initialTriage;

  document.getElementById("liveCC").textContent = `${icon} ${symptomName}`;
  updateTriageBadge(initialTriage);

  patientTranscriptLog.push({ sender: "ai", text: "What is your main health trouble today?" });
  patientTranscriptLog.push({ sender: "patient", text: `${icon} ${symptomName}` });

  checkForContradictions();
  renderPointerQuestion(2);
}

function selectIntensity(intensity) {
  intakeAnswers.intensity = intensity;
  updateCombinedSeverityDuration();
}

function selectCharacter(character) {
  intakeAnswers.character = character;
  document.getElementById("liveCC").textContent = `${intakeAnswers.symptom_icon} ${intakeAnswers.symptom} (${character})`;
  patientTranscriptLog.push({ sender: "ai", text: "How severe is the pain and what type of sensation is it?" });
  patientTranscriptLog.push({ sender: "patient", text: `Intensity: ${intakeAnswers.intensity || 'Moderate'} | Type: ${character}` });

  checkForContradictions();
  renderPointerQuestion(3);
}

function selectDuration(durationText) {
  intakeAnswers.duration = durationText;
  updateCombinedSeverityDuration();
  patientTranscriptLog.push({ sender: "ai", text: "How long have you been having this trouble?" });
  patientTranscriptLog.push({ sender: "patient", text: durationText });

  checkForContradictions();
  renderPointerQuestion(4);
}

function updateCombinedSeverityDuration() {
  const i = intakeAnswers.intensity || "Moderate";
  const d = intakeAnswers.duration || "Just Started";
  document.getElementById("liveDuration").textContent = `${i} • ${d}`;
}

function renderYesNoQuestion(title, sub, fieldType) {
  const container = document.getElementById("pointerQuestionBox");
  const t = UI_TRANSLATIONS[currentLanguage] || UI_TRANSLATIONS.en;

  container.innerHTML = `
    <div class="pointer-question-prompt">
      <div class="pointer-title-main">${title}</div>
      <div class="pointer-title-sub">${sub}</div>
    </div>

    <div class="yes-no-wrap">
      <button type="button" class="btn-pointer-choice btn-pointer-yes" onclick="answerPointerYesNo('${fieldType}', true)">
        <span class="choice-icon">👍</span>
        <span class="choice-label">${t.yesText}</span>
        <span class="choice-sub">${t.yesSub}</span>
      </button>

      <button type="button" class="btn-pointer-choice btn-pointer-no" onclick="answerPointerYesNo('${fieldType}', false)">
        <span class="choice-icon">👎</span>
        <span class="choice-label">${t.noText}</span>
        <span class="choice-sub">${t.noSub}</span>
      </button>
    </div>

    <div style="text-align:center; margin-top:0.75rem;">
      <button type="button" class="speaker-btn" onclick="speakCurrentText('${title.replace(/'/g, "\\\\'")}')">
        🔊 ${t.listenBtn}
      </button>
    </div>
  `;

  speakCurrentText(title);
}

function answerPointerYesNo(fieldType, answerBool) {
  const t = UI_TRANSLATIONS[currentLanguage] || UI_TRANSLATIONS.en;
  const ansLabel = answerBool ? t.yesText : t.noText;

  if (fieldType === "followup1") {
    intakeAnswers.clinical_followup_val = answerBool;
    intakeAnswers.clinical_followup = answerBool ? "Positive for associated radiation/symptoms" : "Negative for radiation";
    document.getElementById("liveClinicalFollowup").textContent = answerBool ? "⚠️ Positive Associated Signs" : t.valNoneReported;
    patientTranscriptLog.push({ sender: "patient", text: `Associated Signs: ${ansLabel}` });
    renderPointerQuestion(5);

  } else if (fieldType === "followup2") {
    intakeAnswers.clinical_followup2_val = answerBool;
    intakeAnswers.clinical_followup2 = answerBool ? "Positive for triggers/past episodes" : "No trigger or recurrence";
    if (answerBool) {
      document.getElementById("liveClinicalFollowup").textContent += " (Trigger/Exertion Positive)";
    }
    patientTranscriptLog.push({ sender: "patient", text: `Triggers/Red Flags: ${ansLabel}` });
    renderPointerQuestion(6);

  } else if (fieldType === "sugar") {
    intakeAnswers.is_sugar_patient = answerBool;
    updateSugarBPLive();
    patientTranscriptLog.push({ sender: "patient", text: `Diabetic History: ${ansLabel}` });
    renderPointerQuestion(7);

  } else if (fieldType === "bp") {
    intakeAnswers.is_bp_patient = answerBool;
    updateSugarBPLive();
    patientTranscriptLog.push({ sender: "patient", text: `Hypertensive History: ${ansLabel}` });
    renderPointerQuestion(8);

  } else if (fieldType === "meds") {
    intakeAnswers.is_daily_meds = answerBool;
    document.getElementById("liveMeds").textContent = answerBool ? "⚠️ Daily Painkillers / Maintenance Tablets" : t.valNoneReported;
    patientTranscriptLog.push({ sender: "patient", text: `Daily Medicines / Painkillers: ${ansLabel}` });
    checkForContradictions();
    renderPointerQuestion(10);

  } else if (fieldType === "allergies") {
    intakeAnswers.is_allergic = answerBool;
    document.getElementById("liveAllergy").textContent = answerBool ? "⚠️ Allergy to Antibiotics/Painkillers" : "None";
    document.getElementById("liveAllergy").style.color = answerBool ? "#dc2626" : "#16a34a";
    patientTranscriptLog.push({ sender: "patient", text: `Drug Allergy: ${ansLabel}` });
    checkForContradictions();
    renderPointerQuestion(11);

  } else if (fieldType === "lifestyle") {
    intakeAnswers.family_lifestyle = answerBool;
    document.getElementById("liveLifestyle").textContent = answerBool ? "⚠️ Cardiac Family History / Tobacco" : t.valStandard;
    patientTranscriptLog.push({ sender: "patient", text: `Lifestyle / Cardiac Family History: ${ansLabel}` });
    checkForContradictions();

    // Enable final submission
    const submitBtn = document.getElementById("finalSubmitBtn");
    if (submitBtn) {
      submitBtn.disabled = false;
      submitBtn.classList.add("pulse-btn");
    }

    // Direct to Thank You / Submission
    finalizeAndSubmitIntake();
  }
}

function updateSugarBPLive() {
  const parts = [];
  if (intakeAnswers.is_sugar_patient) parts.push("Sugar (Diabetic)");
  if (intakeAnswers.is_bp_patient) parts.push("High BP (Hypertensive)");
  const text = parts.length > 0 ? parts.join(" • ") : "Negative / None";
  document.getElementById("liveSugarBP").textContent = text;
  checkForContradictions();
}

function handleDocumentUpload(event) {
  const file = event.target.files[0];
  if (!file) return;

  intakeAnswers.has_documents = true;
  intakeAnswers.doc_name = file.name;

  const reader = new FileReader();
  reader.onload = function(e) {
    intakeAnswers.doc_data = e.target.result;
    document.getElementById("liveDocuments").textContent = `📄 ${file.name} (Verified)`;
    document.getElementById("liveDocuments").style.color = "#0d9488";
    renderPointerQuestion(8);
  };
  reader.readAsDataURL(file);
}

function skipOrProceedDocument() {
  if (!intakeAnswers.has_documents) {
    document.getElementById("liveDocuments").textContent = "No documents attached (Skipped)";
  }
  renderPointerQuestion(9);
}

// ==============================================================================
// REAL-TIME CONTRADICTION DETECTION ENGINE
// ==============================================================================
function checkForContradictions() {
  detectedContradictions = [];
  const sym = intakeAnswers.symptom.toLowerCase();

  // Rule 1: Stomach burning + daily painkillers
  if ((sym.includes("stomach") || sym.includes("पेट") || sym.includes("வயிறு") || sym.includes("કడుపు") || sym.includes("পেট") || sym.includes("પેટ")) && intakeAnswers.is_daily_meds === true) {
    detectedContradictions.push({
      severity: "high",
      title: "NSAID Gastric Irritation Contradiction",
      desc: "Patient reports acute stomach burning/acid while taking daily painkiller pills (e.g. Ibuprofen/Combiflam). High risk of drug-induced peptic erosion!"
    });
  }

  // Rule 2: Chest pain + diabetic + exertion trigger
  if ((sym.includes("chest") || sym.includes("सीने") || sym.includes("நெஞ்சு") || sym.includes("ఛాతీ") || sym.includes("বুকে") || sym.includes("છાતી")) && intakeAnswers.is_sugar_patient === true) {
    detectedContradictions.push({
      severity: "high",
      title: "Atypical Diabetic Angina Risk",
      desc: "Diabetic neuropathy can blunt classic cardiac pain. Immediate ECG & Cardiac Troponin-I test recommended."
    });
    updateTriageBadge("Emergency");
  }

  // Rule 3: High fever > 3 days without relief
  if (intakeAnswers.clinical_followup2_val === true && (sym.includes("fever") || sym.includes("बुखार") || sym.includes("காய்ச்சல்") || sym.includes("జ్వరం") || sym.includes("জ্বর") || sym.includes("તાવ"))) {
    detectedContradictions.push({
      severity: "moderate",
      title: "Persistent Pyrexia Alert",
      desc: "Fever persisting despite medication. Rule out Dengue, Malaria, or Typhoid bacteremia."
    });
    updateTriageBadge("Priority");
  }

  updateContradictionUI();
}

function updateContradictionUI() {
  const container = document.getElementById("pointerFlagsContainer");
  const countBadge = document.getElementById("pointerFlagCount");

  if (!container || !countBadge) return;

  countBadge.textContent = `${detectedContradictions.length} Flags`;

  if (detectedContradictions.length === 0) {
    const t = UI_TRANSLATIONS[currentLanguage] || UI_TRANSLATIONS.en;
    countBadge.style.background = "#dcfce7";
    countBadge.style.color = "#15803d";
    container.innerHTML = `
      <div id="contradictionHintText" style="font-size:0.8rem; color:var(--text-muted); font-style:italic; padding:0.4rem 0;">
        ${t.contradictionHint}
      </div>
    `;
  } else {
    countBadge.style.background = "#fee2e2";
    countBadge.style.color = "#dc2626";
    container.innerHTML = "";
    detectedContradictions.forEach(flag => {
      const item = document.createElement("div");
      item.className = `flag-item ${flag.severity === 'high' ? 'danger' : 'warning'}`;
      item.innerHTML = `<strong>⚠️ ${escapeHtml(flag.title)}:</strong> ${escapeHtml(flag.desc)}`;
      container.appendChild(item);
    });
  }
}

function updateTriageBadge(level) {
  const badge = document.getElementById("pointerTriageBadge");
  if (!badge) return;
  badge.textContent = level;
  badge.className = `badge-triage triage-${level.toLowerCase()}`;
}

// ==============================================================================
// PATIENT SUBMISSION & REAL-TIME WAITING SCREEN
// ==============================================================================
async function finalizeAndSubmitIntake() {
  const caseId = `CAS-2026-${Math.floor(10000 + Math.random() * 90000)}`;
  const triageLevel = intakeAnswers.triage || "Routine";

  const newCase = {
    id: caseId,
    patient_name: activePatient.name,
    age: activePatient.age,
    gender: activePatient.gender,
    contact: activePatient.phone,
    language: (activePatient.language || currentLanguage || "hi").toUpperCase(),
    chief_complaint: `${intakeAnswers.symptom} (${intakeAnswers.character || 'Acute'})`,
    symptoms: `${intakeAnswers.symptom}. Intensity: ${intakeAnswers.intensity || 'Moderate'}.`,
    hpi: `Patient presented with ${intakeAnswers.symptom}. Duration: ${intakeAnswers.duration || 'Not specified'}. Associated signs: ${intakeAnswers.clinical_followup || 'None'}. Triggers/Past: ${intakeAnswers.clinical_followup2 || 'None'}. Diabetic: ${intakeAnswers.is_sugar_patient ? 'Yes' : 'No'}. Hypertensive: ${intakeAnswers.is_bp_patient ? 'Yes' : 'No'}.`,
    past_history: `Diabetes: ${intakeAnswers.is_sugar_patient ? 'Positive' : 'Negative'} | Hypertension: ${intakeAnswers.is_bp_patient ? 'Positive' : 'Negative'} | Attached Records: ${intakeAnswers.has_documents ? intakeAnswers.doc_name : 'None'}`,
    medications: intakeAnswers.is_daily_meds ? "Takes daily pain relief / maintenance tablets" : "None reported",
    allergies: intakeAnswers.is_allergic ? "Flagged known drug allergies" : "No known drug allergies (NKDA)",
    lifestyle: intakeAnswers.family_lifestyle ? "Positive family cardiac history / tobacco consumption" : "Standard non-contributory",
    triage_level: triageLevel,
    contradictions: detectedContradictions,
    missing_gaps: [],
    uploaded_document_name: intakeAnswers.doc_name,
    uploaded_document_data: intakeAnswers.doc_data,
    doctor_status: "Pending Review",
    doctor_notes: "",
    doctor_diagnosis: "",
    doctor_rx: "",
    verified_by: "",
    verified_at: "",
    conversation_transcript: patientTranscriptLog,
    created_at: new Date().toISOString().replace("T", " ").slice(0, 19)
  };

  waitingCaseId = caseId;
  await saveCaseToDatabase(newCase);
  showThankYouScreen(caseId);
}

async function saveCaseToDatabase(newCase) {
  try {
    await fetch("/api/cases", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(newCase)
    });
  } catch (err) {
    console.log("Local fallback save:", err.message);
  }

  const idx = allCases.findIndex(c => c.id === newCase.id);
  if (idx >= 0) allCases[idx] = newCase;
  else allCases.unshift(newCase);

  localStorage.setItem("patientcare_cases", JSON.stringify(allCases));
  updateDoctorStats();
  renderCasesTable(allCases);
}

function showThankYouScreen(caseId) {
  const container = document.getElementById("pointerQuestionBox");
  const header = document.getElementById("pointerStepHeader");

  const lang = activePatient.language || currentLanguage || "en";
  const t = UI_TRANSLATIONS[lang] || UI_TRANSLATIONS.en;

  header.textContent = `✅ ${t.thankYouTitle}`;

  // Hide voice bar during thank you screen
  const voiceBar = document.querySelector(".voice-illiterate-bar");
  if (voiceBar) voiceBar.style.display = "none";

  speakCurrentText(t.spokenThankYou);

  container.innerHTML = `
    <div class="thankyou-card">
      <div class="thankyou-icon-wrap">🙏</div>
      <div class="token-badge-large">
        <span>${t.tokenLabel}</span>
        <span id="activeWaitingToken">${escapeHtml(caseId)}</span>
      </div>
      <h2 style="font-size:1.35rem; font-weight:800; color:var(--primary); margin:0 0 0.5rem 0;">
        ${escapeHtml(t.thankYouTitle)}, ${escapeHtml(activePatient.name)}!
      </h2>
      <p style="font-size:0.925rem; color:var(--text-main); font-weight:600; margin:0 0 1rem 0;">
        ${escapeHtml(t.thankYouSub)}
      </p>

      <div id="patientWaitingStatusSlot">
        <div class="patient-wait-box" style="border-left: 4px solid var(--teal);">
          <div style="font-size:1rem; font-weight:700; color:var(--teal); margin-bottom:0.25rem;">
            📢 ${escapeHtml(t.waitHeading)}
          </div>
          <div style="font-size:0.9rem; color:var(--text-main); line-height:1.4;">
            ${escapeHtml(t.waitMsg)}
          </div>
          <div style="margin-top:0.6rem; font-size:0.8rem; color:#b45309; font-weight:700;">
            ${t.waitingInQueue}
          </div>
        </div>
      </div>

      <div id="countdownContainer" class="countdown-box">
        <div style="font-size:0.8rem; font-weight:700; color:var(--text-muted); text-transform:uppercase; letter-spacing:0.5px;">
          ${escapeHtml(t.redirectMsg)}
        </div>
        <div class="countdown-number" id="thankYouCountdownNum">15</div>
        <div class="countdown-bar-wrap">
          <div class="countdown-bar-fill" id="countdownProgressBar" style="width: 100%;"></div>
        </div>
      </div>

      <div style="margin-top:1.25rem; display:flex; justify-content:center; gap:0.75rem;">
        <button type="button" class="btn btn-outline" style="padding:0.65rem 1.25rem; font-weight:700;" onclick="resetForNewPatient()">
          ${escapeHtml(t.nextPatientBtn)}
        </button>
      </div>
    </div>
  `;

  startThankYouCountdown(15);
  startWaitingStatusPolling(caseId);
}

function startThankYouCountdown(totalSeconds) {
  if (thankYouCountdownTimer) clearInterval(thankYouCountdownTimer);

  let seconds = totalSeconds;
  thankYouCountdownTimer = setInterval(() => {
    seconds--;
    const numEl = document.getElementById("thankYouCountdownNum");
    const barEl = document.getElementById("countdownProgressBar");
    if (numEl) numEl.textContent = seconds;
    if (barEl) barEl.style.width = `${(seconds / totalSeconds) * 100}%`;

    if (seconds <= 0) {
      clearInterval(thankYouCountdownTimer);
      thankYouCountdownTimer = null;
      resetForNewPatient();
    }
  }, 1000);
}

// Background polling for real-time doctor verification
function startWaitingStatusPolling(caseId) {
  if (statusPollingInterval) clearInterval(statusPollingInterval);

  statusPollingInterval = setInterval(async () => {
    try {
      const res = await fetch(`/api/cases/${caseId}`);
      if (res.ok) {
        const data = await res.json();
        if (data.success && data.case && data.case.doctor_status === "Verified") {
          handleCaseVerified(data.case);
          clearInterval(statusPollingInterval);
        }
      }
    } catch (e) {}
  }, 2000);
}

// ==============================================================================
// INSTANT DOCTOR VERIFICATION TO PATIENT LIVE UPDATE HANDLER
// ==============================================================================
function handleCaseVerified(caseObj) {
  if (!caseObj) return;

  // Check if this matches currently waiting patient or active screen
  const tokenEl = document.getElementById("activeWaitingToken");
  const isCurrentlyWaitingThisCase = (tokenEl && tokenEl.textContent.trim() === caseObj.id) || (waitingCaseId === caseObj.id);

  // Play audio chime
  playVerificationChime();

  // Show Toast Notification
  showLiveToast(`🔔 Case ${caseObj.id} verified by ${caseObj.verified_by || 'Dr. Priya Sharma, M.D.'}!`);

  // Announce via voice
  const lang = (activePatient && activePatient.language) || currentLanguage || "en";
  const t = UI_TRANSLATIONS[lang] || UI_TRANSLATIONS.en;
  speakCurrentText(t.spokenVerified);

  // Update in-memory lists
  const idx = allCases.findIndex(c => c.id === caseObj.id);
  if (idx >= 0) allCases[idx] = caseObj;
  else allCases.unshift(caseObj);
  updateDoctorStats();
  renderCasesTable(allCases);

  // If patient is currently viewing the waiting screen, transform it into the verified prescription card!
  if (isCurrentlyWaitingThisCase) {
    if (thankYouCountdownTimer) {
      clearInterval(thankYouCountdownTimer);
      thankYouCountdownTimer = null;
    }
    if (statusPollingInterval) {
      clearInterval(statusPollingInterval);
      statusPollingInterval = null;
    }

    const countdownBox = document.getElementById("countdownContainer");
    if (countdownBox) countdownBox.style.display = "none";

    const slot = document.getElementById("patientWaitingStatusSlot");
    if (slot) {
      slot.innerHTML = `
        <div class="verified-live-card">
          <div class="verified-card-header">
            <div>
              <div style="font-size:1.15rem; font-weight:800; color:#15803d; display:flex; align-items:center; gap:0.4rem;">
                <span>✅</span> <span>${t.verifiedTitle}</span>
              </div>
              <div style="font-size:0.775rem; color:#166534; margin-top:0.2rem;">
                Verified by <strong>${escapeHtml(caseObj.verified_by || 'Dr. Priya Sharma, M.D.')}</strong> • ${escapeHtml(caseObj.verified_at || 'Just now')}
              </div>
            </div>
            <span class="verified-pill">✓ ${t.verifiedBadge}</span>
          </div>

          <div class="verified-section">
            <div class="verified-section-title">${t.docDiagnosisLabel}</div>
            <div class="verified-box-content" style="font-weight:700; color:#1e3a8a;">
              ${escapeHtml(caseObj.doctor_diagnosis || 'Clinical Assessment Confirmed')}
            </div>
          </div>

          <div class="verified-section">
            <div class="verified-section-title">${t.docRxLabel}</div>
            <div class="verified-box-content rx-box">
${escapeHtml(caseObj.doctor_rx || '1. Tab Pantoprazole 40mg OD AC\\n2. Symptomatic pain relief')}
            </div>
          </div>

          ${caseObj.doctor_notes ? `
          <div class="verified-section">
            <div class="verified-section-title">${t.docAdviceLabel}</div>
            <div class="verified-box-content" style="color:#334155; font-size:0.85rem;">
              ${escapeHtml(caseObj.doctor_notes)}
            </div>
          </div>` : ''}

          <div style="margin-top:1rem; display:flex; gap:0.75rem;">
            <button type="button" class="btn btn-teal" style="flex:1; padding:0.65rem; font-weight:700; font-size:0.9rem;" onclick="printCaseSheetById('${caseObj.id}')">
              ${t.printRxBtn}
            </button>
          </div>
        </div>
      `;
    }
  }
}

function showLiveToast(message) {
  const existing = document.getElementById("liveVerificationToast");
  if (existing) existing.remove();

  const toast = document.createElement("div");
  toast.id = "liveVerificationToast";
  toast.className = "live-notification-toast";
  toast.innerHTML = `<span>🔔</span> <span>${escapeHtml(message)}</span>`;
  document.body.appendChild(toast);

  setTimeout(() => {
    if (toast) toast.remove();
  }, 5000);
}

function resetForNewPatient() {
  if (thankYouCountdownTimer) {
    clearInterval(thankYouCountdownTimer);
    thankYouCountdownTimer = null;
  }
  if (statusPollingInterval) {
    clearInterval(statusPollingInterval);
    statusPollingInterval = null;
  }
  if (window.speechSynthesis) {
    window.speechSynthesis.cancel();
  }

  const voiceBar = document.querySelector(".voice-illiterate-bar");
  if (voiceBar) voiceBar.style.display = "flex";

  currentPointerStep = 1;
  waitingCaseId = null;
  patientTranscriptLog = [];
  detectedContradictions = [];
  intakeAnswers = {
    symptom: "",
    symptom_icon: "",
    triage: "Routine",
    intensity: "",
    character: "",
    duration: "",
    clinical_followup: "",
    clinical_followup_val: null,
    clinical_followup2: "",
    clinical_followup2_val: null,
    is_sugar_patient: null,
    is_bp_patient: null,
    has_documents: false,
    doc_name: "",
    doc_data: "",
    is_daily_meds: null,
    meds_detail: "",
    is_allergic: null,
    allergy_detail: "",
    family_lifestyle: null
  };

  const nameEl = document.getElementById("regName");
  const ageEl = document.getElementById("regAge");
  const phoneEl = document.getElementById("regPhone");
  if (nameEl) nameEl.value = "";
  if (ageEl) ageEl.value = "";
  if (phoneEl) phoneEl.value = "";

  const ccEl = document.getElementById("liveCC");
  const durEl = document.getElementById("liveDuration");
  const followEl = document.getElementById("liveClinicalFollowup");
  const sugarBPEl = document.getElementById("liveSugarBP");
  const docsEl = document.getElementById("liveDocuments");
  const medsEl = document.getElementById("liveMeds");
  const allergyEl = document.getElementById("liveAllergy");
  const lifeEl = document.getElementById("liveLifestyle");
  const submitBtn = document.getElementById("finalSubmitBtn");

  const t = UI_TRANSLATIONS[currentLanguage] || UI_TRANSLATIONS.en;
  if (ccEl) ccEl.textContent = t.valWaitingSymptom;
  if (durEl) durEl.textContent = t.valNotAnswered;
  if (followEl) followEl.textContent = t.valNoneReported;
  if (sugarBPEl) sugarBPEl.textContent = t.valNegative;
  if (docsEl) docsEl.textContent = t.valNoDocs;
  if (medsEl) medsEl.textContent = t.valNoneReported;
  if (allergyEl) allergyEl.textContent = t.valNone;
  if (lifeEl) lifeEl.textContent = t.valStandard;
  if (submitBtn) submitBtn.disabled = true;

  updateContradictionUI();

  document.getElementById("pointerIntakeView").classList.remove("active");
  document.getElementById("doctorView").classList.remove("active");
  document.getElementById("registrationView").classList.add("active");

  applyLanguageToEntireUI(currentLanguage);
}

// ==============================================================================
// DOCTOR PORTAL & ACTIONS
// ==============================================================================
function openDoctorLoginModal() {
  document.getElementById("doctorLoginModal").classList.add("active");
}

function closeDoctorLoginModal() {
  document.getElementById("doctorLoginModal").classList.remove("active");
}

function handleDoctorLogin(e) {
  e.preventDefault();
  closeDoctorLoginModal();
  switchRole("doctor");
}

function quickDemoDoctorLogin() {
  closeDoctorLoginModal();
  switchRole("doctor");
}

function logoutDoctor() {
  switchRole("patient");
}

function switchRole(role) {
  currentRole = role;
  if (role === "doctor") {
    document.getElementById("registrationView").classList.remove("active");
    document.getElementById("pointerIntakeView").classList.remove("active");
    document.getElementById("doctorView").classList.add("active");
    loadStoredCases();
  } else {
    document.getElementById("doctorView").classList.remove("active");
    document.getElementById("pointerIntakeView").classList.remove("active");
    document.getElementById("registrationView").classList.add("active");
    applyLanguageToEntireUI(currentLanguage);
  }
}

function updateDoctorStats() {
  const total = allCases.length;
  const pending = allCases.filter(c => c.doctor_status !== "Verified").length;
  const verified = allCases.filter(c => c.doctor_status === "Verified").length;
  const critical = allCases.filter(c => c.triage_level === "Emergency" || (c.contradictions && c.contradictions.length > 0)).length;

  const totalEl = document.getElementById("statTotalCases");
  const pendingEl = document.getElementById("statPendingTriage");
  const verifiedEl = document.getElementById("statVerified");
  const criticalEl = document.getElementById("statCriticalFlags");
  const headerBadge = document.getElementById("headerPendingBadge");

  if (totalEl) totalEl.textContent = total;
  if (pendingEl) pendingEl.textContent = pending;
  if (verifiedEl) verifiedEl.textContent = verified;
  if (criticalEl) criticalEl.textContent = critical;
  if (headerBadge) headerBadge.textContent = pending;
}

let activeDoctorFilter = "all";

function filterDoctorCases(filterType) {
  activeDoctorFilter = filterType;
  document.querySelectorAll(".doctor-filters .filter-btn").forEach(btn => btn.classList.remove("active"));
  const clicked = document.querySelector(`.doctor-filters .filter-btn[data-filter="${filterType}"]`);
  if (clicked) clicked.classList.add("active");

  const filtered = allCases.filter(c => {
    if (activeDoctorFilter === "all") return true;
    if (activeDoctorFilter === "pending") return c.doctor_status !== "Verified";
    if (activeDoctorFilter === "verified") return c.doctor_status === "Verified";
    if (activeDoctorFilter === "flagged") return c.contradictions && c.contradictions.length > 0;
    return true;
  });

  renderCasesTable(filtered);
}

function renderCasesTable(cases) {
  const tbody = document.getElementById("casesTableBody");
  if (!tbody) return;

  tbody.innerHTML = "";
  if (!cases || cases.length === 0) {
    tbody.innerHTML = `<tr><td colspan="7" style="text-align:center; padding:2rem; color:var(--text-muted);">No cases found in this triage view.</td></tr>`;
    return;
  }

  cases.forEach(c => {
    const tr = document.createElement("tr");

    const triageClass = `triage-${(c.triage_level || 'Routine').toLowerCase()}`;
    const flags = c.contradictions || [];
    const flagHtml = flags.length > 0
      ? `<span class="badge-count" style="background:#fee2e2; color:#dc2626;">⚠️ ${flags.length} Flags</span>`
      : `<span style="color:#16a34a; font-size:0.8rem; font-weight:600;">✓ Safe</span>`;

    const statusHtml = c.doctor_status === "Verified"
      ? `<span class="status-badge-verified">✓ Verified</span>`
      : `<span class="status-badge-pending">⏳ Pending Review</span>`;

    const docChip = c.uploaded_document_name
      ? `<span title="${escapeHtml(c.uploaded_document_name)}" style="display:inline-block; font-size:0.75rem; background:#ccfbf1; color:#0f766e; padding:0.15rem 0.4rem; border-radius:3px; margin-top:0.2rem;">📎 Report</span>`
      : '';

    tr.innerHTML = `
      <td><strong>${escapeHtml(c.id)}</strong><br><span style="font-size:0.7rem; color:var(--text-muted);">${c.created_at || 'Just now'}</span></td>
      <td>
        <strong>${escapeHtml(c.patient_name)}</strong><br>
        <span style="font-size:0.75rem; color:var(--text-muted);">${c.age} Y • ${escapeHtml(c.gender)} • ${escapeHtml(c.language || 'HI')}</span>
        ${docChip}
      </td>
      <td style="max-width:240px;">${escapeHtml(c.chief_complaint)}</td>
      <td><span class="badge-triage ${triageClass}">${escapeHtml(c.triage_level)}</span></td>
      <td>${flagHtml}</td>
      <td>${statusHtml}</td>
      <td>
        <button class="btn btn-primary" style="padding:0.35rem 0.75rem; font-size:0.775rem;" onclick="openCaseReview('${c.id}')">
          👁️ Review & Verify
        </button>
      </td>
    `;
    tbody.appendChild(tr);
  });
}

function openCaseReview(caseId) {
  const caseObj = allCases.find(c => c.id === caseId);
  if (!caseObj) return;

  activeCase = caseObj;

  document.getElementById("modalPatientTitle").textContent = `${caseObj.patient_name} (${caseObj.id})`;
  document.getElementById("modalPatientMeta").textContent = `${caseObj.age} Yrs • ${caseObj.gender} • Contact: ${caseObj.contact || 'N/A'} • Preferred: ${caseObj.language || 'Hindi'}`;

  const verifiedBanner = document.getElementById("verifiedBanner");
  if (caseObj.doctor_status === "Verified") {
    verifiedBanner.style.display = "flex";
    document.getElementById("verifiedByLabel").textContent = caseObj.verified_by || "Dr. Priya Sharma, M.D.";
    document.getElementById("verifiedAtLabel").textContent = `Verified: ${caseObj.verified_at || caseObj.created_at}`;
    document.getElementById("verifyBtn").textContent = "✓ Re-Verify Record";
  } else {
    verifiedBanner.style.display = "none";
    document.getElementById("verifyBtn").textContent = "✅ Verify & Sign-Off Record";
  }

  // Left Column: Patient Responses
  const transcriptBox = document.getElementById("modalTranscriptBox");
  transcriptBox.innerHTML = "";
  if (caseObj.conversation_transcript && caseObj.conversation_transcript.length > 0) {
    caseObj.conversation_transcript.forEach(msg => {
      const b = document.createElement("div");
      b.className = `chat-bubble-mini ${msg.sender}`;
      b.innerHTML = `<strong>${msg.sender === 'ai' ? '🩺 Question' : '👤 Patient'}:</strong> ${escapeHtml(msg.text)}`;
      transcriptBox.appendChild(b);
    });
  } else {
    transcriptBox.innerHTML = `<div style="font-size:0.8rem; color:var(--text-muted);">No transcript recorded for this patient.</div>`;
  }

  // Contradictions in Modal
  const flagsBox = document.getElementById("modalContradictionsBox");
  flagsBox.innerHTML = "";
  const allFlags = caseObj.contradictions || [];
  if (allFlags.length === 0) {
    flagsBox.innerHTML = `<div style="font-size:0.8rem; color:#16a34a;">No conflicting statements flagged.</div>`;
  } else {
    allFlags.forEach(f => {
      const div = document.createElement("div");
      div.className = `flag-item ${f.severity === 'high' ? 'danger' : 'warning'}`;
      div.innerHTML = `<strong>${escapeHtml(f.title)}:</strong> ${escapeHtml(f.desc)}`;
      flagsBox.appendChild(div);
    });
  }

  // Uploaded Document Viewer in Modal
  const docViewer = document.getElementById("modalDocumentViewer");
  if (docViewer) {
    if (caseObj.uploaded_document_name) {
      const isImg = caseObj.uploaded_document_data && caseObj.uploaded_document_data.startsWith("data:image");
      docViewer.innerHTML = `
        <div style="display:flex; align-items:center; gap:0.75rem; background:white; padding:0.5rem; border-radius:4px; border:1px solid #99f6e4;">
          ${isImg ? `<img src="${caseObj.uploaded_document_data}" style="max-width:50px; max-height:50px; border-radius:4px;">` : `<span style="font-size:1.5rem;">📄</span>`}
          <div>
            <strong style="color:var(--teal);">${escapeHtml(caseObj.uploaded_document_name)}</strong><br>
            <span style="font-size:0.75rem; color:#16a34a; font-weight:600;">✓ Document Verified by AI OCR</span>
          </div>
          ${caseObj.uploaded_document_data ? `<a href="${caseObj.uploaded_document_data}" target="_blank" class="btn btn-outline" style="margin-left:auto; padding:0.25rem 0.6rem; font-size:0.75rem;">View Document ↗</a>` : ''}
        </div>
      `;
    } else {
      docViewer.innerHTML = `<span style="font-style:italic; color:var(--text-muted);">No prior medical records or lab reports attached by patient.</span>`;
    }
  }

  // Right Column: Editable Fields
  document.getElementById("editCaseId").value = caseObj.id;
  document.getElementById("editCC").value = caseObj.chief_complaint || "";
  document.getElementById("editHPI").value = caseObj.hpi || "";
  document.getElementById("editPastHistory").value = caseObj.past_history || "None reported";
  document.getElementById("editMeds").value = caseObj.medications || "None reported";
  document.getElementById("editAllergies").value = caseObj.allergies || "NKDA";
  document.getElementById("editDiagnosis").value = caseObj.doctor_diagnosis || "Clinical Diagnosis Confirmed";
  document.getElementById("editRx").value = caseObj.doctor_rx || "1. Tab Pantoprazole 40mg OD AC\\n2. Symptomatic relief";
  document.getElementById("editDoctorNotes").value = caseObj.doctor_notes || "Patient evaluated and cleared.";

  document.getElementById("reviewModal").classList.add("active");
}

function closeReviewModal() {
  document.getElementById("reviewModal").classList.remove("active");
  activeCase = null;
}

async function saveCaseEditsOnly() {
  if (!activeCase) return;

  activeCase.chief_complaint = document.getElementById("editCC").value;
  activeCase.hpi = document.getElementById("editHPI").value;
  activeCase.past_history = document.getElementById("editPastHistory").value;
  activeCase.medications = document.getElementById("editMeds").value;
  activeCase.allergies = document.getElementById("editAllergies").value;
  activeCase.doctor_diagnosis = document.getElementById("editDiagnosis").value;
  activeCase.doctor_rx = document.getElementById("editRx").value;
  activeCase.doctor_notes = document.getElementById("editDoctorNotes").value;

  await saveCaseToDatabase(activeCase);
  alert("Case details updated successfully.");
}

// ==============================================================================
// DOCTOR VERIFICATION & REAL-TIME DISPATCH
// ==============================================================================
async function verifyAndSignOffCase() {
  if (!activeCase) return;

  activeCase.chief_complaint = document.getElementById("editCC").value;
  activeCase.hpi = document.getElementById("editHPI").value;
  activeCase.past_history = document.getElementById("editPastHistory").value;
  activeCase.medications = document.getElementById("editMeds").value;
  activeCase.allergies = document.getElementById("editAllergies").value;
  activeCase.doctor_diagnosis = document.getElementById("editDiagnosis").value || "Clinical Diagnosis Confirmed";
  activeCase.doctor_rx = document.getElementById("editRx").value || "1. Tab Pantoprazole 40mg OD AC\\n2. Symptomatic pain relief";
  activeCase.doctor_notes = document.getElementById("editDoctorNotes").value || "Patient verified and cleared for treatment.";
  activeCase.doctor_status = "Verified";
  activeCase.verified_by = "Dr. Priya Sharma, M.D. (Internal Medicine)";
  activeCase.verified_at = new Date().toISOString().replace("T", " ").slice(0, 19);

  try {
    await fetch(`/api/cases/${activeCase.id}/verify`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        doctor_diagnosis: activeCase.doctor_diagnosis,
        doctor_rx: activeCase.doctor_rx,
        doctor_notes: activeCase.doctor_notes,
        verified_by: activeCase.verified_by,
        verified_at: activeCase.verified_at
      })
    });
  } catch (err) {
    console.log("Local fallback verify:", err.message);
  }

  // Update in memory and local storage
  const idx = allCases.findIndex(c => c.id === activeCase.id);
  if (idx >= 0) allCases[idx] = activeCase;
  localStorage.setItem("patientcare_cases", JSON.stringify(allCases));
  localStorage.setItem("patientcare_last_verified", JSON.stringify(activeCase));

  // Broadcast to other tabs & dispatch locally
  if (patientCareChannel) {
    patientCareChannel.postMessage({ type: "CASE_VERIFIED", caseObj: activeCase });
  }
  window.dispatchEvent(new CustomEvent("caseVerified", { detail: activeCase }));

  // Also directly call handler in current window
  handleCaseVerified(activeCase);

  updateDoctorStats();
  renderCasesTable(allCases);
  closeReviewModal();

  alert(`✅ Case ${activeCase.id} has been digitally verified and signed off by Dr. Priya Sharma, M.D.!\\n\\nThe patient's record and screen have been updated in real-time.`);
}

// Alias for backwards compatibility
const verifyCaseByDoctor = verifyAndSignOffCase;

// ==============================================================================
// PATIENT STATUS TRACKER MODAL
// ==============================================================================
function openPatientStatusModal() {
  const modal = document.getElementById("patientStatusModal");
  if (modal) {
    modal.classList.add("active");
    const input = document.getElementById("trackCaseInput");
    if (input && waitingCaseId) input.value = waitingCaseId;
  }
}

function closePatientStatusModal() {
  const modal = document.getElementById("patientStatusModal");
  if (modal) modal.classList.remove("active");
}

function checkCaseStatusByInput() {
  const input = document.getElementById("trackCaseInput");
  const caseId = input ? input.value.trim() : "";
  if (!caseId) {
    alert("Please enter a valid Patient Token ID (e.g. CAS-2026-...)");
    return;
  }

  const found = allCases.find(c => c.id.toUpperCase() === caseId.toUpperCase());
  const resContainer = document.getElementById("trackStatusResultContainer");
  const lang = (found && found.language) ? found.language.toLowerCase() : currentLanguage;
  const t = UI_TRANSLATIONS[lang] || UI_TRANSLATIONS.en;

  if (!found) {
    resContainer.innerHTML = `
      <div style="text-align:center; padding:1.5rem; color:#dc2626;">
        <span style="font-size:2rem;">❌</span>
        <h4 style="margin:0.5rem 0 0.25rem 0;">Case Not Found</h4>
        <p style="font-size:0.85rem; color:var(--text-muted); margin:0;">No record exists with Token ID "${escapeHtml(caseId)}". Please verify your token.</p>
      </div>
    `;
    return;
  }

  if (found.doctor_status === "Verified") {
    resContainer.innerHTML = `
      <div class="verified-live-card" style="margin:0.5rem 0;">
        <div class="verified-card-header">
          <div>
            <div style="font-size:1.1rem; font-weight:800; color:#15803d; display:flex; align-items:center; gap:0.4rem;">
              <span>✅</span> <span>${t.verifiedTitle}</span>
            </div>
            <div style="font-size:0.775rem; color:#166534; margin-top:0.2rem;">
              Patient: <strong>${escapeHtml(found.patient_name)}</strong> • ${found.age} Yrs • ${escapeHtml(found.gender)}
            </div>
            <div style="font-size:0.75rem; color:#047857;">
              Verified by ${escapeHtml(found.verified_by || 'Dr. Priya Sharma, M.D.')} • ${escapeHtml(found.verified_at || 'Recently')}
            </div>
          </div>
          <span class="verified-pill">✓ VERIFIED</span>
        </div>

        <div class="verified-section">
          <div class="verified-section-title">${t.docDiagnosisLabel}</div>
          <div class="verified-box-content" style="font-weight:700; color:#1e3a8a;">
            ${escapeHtml(found.doctor_diagnosis || 'Clinical Diagnosis Confirmed')}
          </div>
        </div>

        <div class="verified-section">
          <div class="verified-section-title">${t.docRxLabel}</div>
          <div class="verified-box-content rx-box">
${escapeHtml(found.doctor_rx || '1. Tab Pantoprazole 40mg OD AC')}
          </div>
        </div>

        ${found.doctor_notes ? `
        <div class="verified-section">
          <div class="verified-section-title">${t.docAdviceLabel}</div>
          <div class="verified-box-content" style="color:#334155; font-size:0.85rem;">
            ${escapeHtml(found.doctor_notes)}
          </div>
        </div>` : ''}

        <div style="margin-top:1rem;">
          <button type="button" class="btn btn-teal btn-block" style="padding:0.65rem; font-weight:700;" onclick="printCaseSheetById('${found.id}')">
            ${t.printRxBtn}
          </button>
        </div>
      </div>
    `;
  } else {
    resContainer.innerHTML = `
      <div style="background:#fffbeb; border:1px solid #fde68a; border-radius:8px; padding:1.25rem; text-align:center;">
        <span style="font-size:2rem;">⏳</span>
        <h4 style="margin:0.5rem 0 0.25rem 0; color:#b45309;">${t.waitingInQueue}</h4>
        <p style="font-size:0.85rem; color:var(--text-muted); margin:0 0 0.5rem 0;">
          Patient: <strong>${escapeHtml(found.patient_name)}</strong> (${escapeHtml(found.id)})
        </p>
        <p style="font-size:0.85rem; color:var(--text-main); margin:0;">
          Your clinical health intake is safely in the doctor's review queue. Please wait until the doctor signs off your prescription.
        </p>
      </div>
    `;
  }
}

// ==============================================================================
// PRINT HOSPITAL CASE SHEET & PRESCRIPTION
// ==============================================================================
function printCaseSheetById(caseId) {
  const caseObj = allCases.find(c => c.id === caseId);
  if (!caseObj) return;
  activeCase = caseObj;
  printCaseSheet();
}

function printCaseSheet() {
  if (!activeCase) return;

  let container = document.getElementById("printHospitalSheet");
  if (!container) {
    container = document.createElement("div");
    container.id = "printHospitalSheet";
    container.style.display = "none";
    document.body.appendChild(container);
  }

  container.innerHTML = `
    <div style="font-family:Arial, sans-serif; max-width:800px; margin:0 auto; padding:20px; border:2px solid #0d9488;">
      <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:2px solid #0d9488; padding-bottom:10px; margin-bottom:15px;">
        <div>
          <h2 style="margin:0; color:#1e3a8a;">AIIMS / DISTRICT CIVIL HOSPITAL</h2>
          <p style="margin:2px 0 0 0; font-size:12px; color:#555;">Smart India Hackathon 2026 Prototype • Patient Care Case Sheet</p>
        </div>
        <div style="text-align:right;">
          <h3 style="margin:0; color:#0d9488;">Case ID: ${activeCase.id}</h3>
          <p style="margin:0; font-size:12px;">Date: ${activeCase.verified_at || activeCase.created_at}</p>
        </div>
      </div>

      <table style="width:100%; border-collapse:collapse; margin-bottom:15px; font-size:13px;">
        <tr style="background:#f1f5f9;">
          <td style="padding:6px; font-weight:bold;">Patient Name:</td>
          <td style="padding:6px;">${activeCase.patient_name}</td>
          <td style="padding:6px; font-weight:bold;">Age / Gender:</td>
          <td style="padding:6px;">${activeCase.age} Yrs / ${activeCase.gender}</td>
        </tr>
        <tr>
          <td style="padding:6px; font-weight:bold;">Contact:</td>
          <td style="padding:6px;">${activeCase.contact || 'N/A'}</td>
          <td style="padding:6px; font-weight:bold;">Triage Priority:</td>
          <td style="padding:6px; font-weight:bold; color:#0d9488;">${activeCase.triage_level}</td>
        </tr>
      </table>

      <div style="margin-bottom:12px;">
        <h4 style="margin:0 0 4px 0; color:#1e3a8a; border-bottom:1px solid #ddd; padding-bottom:3px; font-size:13px;">CHIEF COMPLAINT & PRESENT ILLNESS (HPI):</h4>
        <p style="margin:0; font-size:12px; line-height:1.4;">${activeCase.hpi || activeCase.chief_complaint}</p>
      </div>

      <div style="margin-bottom:12px;">
        <h4 style="margin:0 0 4px 0; color:#1e3a8a; border-bottom:1px solid #ddd; padding-bottom:3px; font-size:13px;">PAST MEDICAL HISTORY & MEDICATIONS:</h4>
        <p style="margin:0; font-size:12px; line-height:1.4;">${activeCase.past_history} • Daily Meds: ${activeCase.medications} • Allergies: ${activeCase.allergies}</p>
      </div>

      <div style="margin-bottom:12px; background:#f0fdf4; border:1px solid #86efac; padding:8px; border-radius:4px;">
        <h4 style="margin:0 0 4px 0; color:#15803d; font-size:13px;">DOCTOR CONFIRMED DIAGNOSIS:</h4>
        <p style="margin:0; font-size:13px; font-weight:bold; color:#0f172a;">${activeCase.doctor_diagnosis || 'Under Evaluation'}</p>
      </div>

      <div style="margin-bottom:15px; border:1px dashed #0d9488; padding:10px; border-radius:4px;">
        <h4 style="margin:0 0 6px 0; color:#0d9488; font-size:13px;">PRESCRIPTION / Rx:</h4>
        <pre style="margin:0; font-family:monospace; font-size:12px; white-space:pre-wrap; color:#0f172a;">${activeCase.doctor_rx || 'Symptomatic medical management.'}</pre>
      </div>

      <div style="display:flex; justify-content:space-between; align-items:flex-end; border-top:1px solid #ddd; padding-top:15px; margin-top:20px;">
        <div>
          <span style="display:inline-block; border:2px solid #16a34a; color:#16a34a; font-weight:bold; font-size:11px; padding:3px 8px; border-radius:3px;">
            ✓ DIGITALLY VERIFIED (SIH 2026 NDHM)
          </span>
        </div>
        <div style="text-align:right;">
          <p style="margin:0; font-weight:bold; font-size:13px;">${activeCase.verified_by || 'Dr. Priya Sharma, M.D.'}</p>
          <p style="margin:2px 0 0 0; font-size:11px; color:#666;">Medical Officer • Reg: MCI-78421</p>
        </div>
      </div>
    </div>
  `;

  const originalContent = document.body.innerHTML;
  document.body.innerHTML = container.innerHTML;
  window.print();
  document.body.innerHTML = originalContent;
  window.location.reload();
}

// ==============================================================================
// AUDIO READ-ALOUD & VOICE ACCESSIBILITY (FOR ILLITERATE PATIENTS)
// ==============================================================================
function toggleAudioNarration() {
  isAudioAssistanceOn = !isAudioAssistanceOn;
  const btn = document.getElementById("globalAudioToggleBtn");
  const text = document.getElementById("audioText");
  const icon = document.getElementById("audioIcon");
  const t = UI_TRANSLATIONS[currentLanguage] || UI_TRANSLATIONS.en;

  if (isAudioAssistanceOn) {
    btn.style.background = "#f0fdf4";
    btn.style.borderColor = "#bbf7d0";
    btn.style.color = "#166534";
    icon.textContent = "🔊";
    text.innerHTML = t.voiceOn;
    speakCurrentText("Voice assistance is enabled.");
  } else {
    btn.style.background = "#f1f5f9";
    btn.style.borderColor = "#cbd5e1";
    btn.style.color = "#64748b";
    icon.textContent = "🔇";
    text.innerHTML = t.voiceOff;
    if (window.speechSynthesis) window.speechSynthesis.cancel();
  }
}

function speakCurrentText(textToSpeak) {
  if (!isAudioAssistanceOn) return;
  if (!("speechSynthesis" in window)) return;

  window.speechSynthesis.cancel();

  const utterance = new SpeechSynthesisUtterance(textToSpeak);
  const voiceLangMap = {
    en: "en-IN",
    hi: "hi-IN",
    ta: "ta-IN",
    te: "te-IN",
    bn: "bn-IN",
    mr: "mr-IN",
    gu: "gu-IN"
  };
  const activeLang = (activePatient && activePatient.language) ? activePatient.language : currentLanguage;
  utterance.lang = voiceLangMap[activeLang] || "en-IN";
  utterance.rate = 0.95;

  window.speechSynthesis.speak(utterance);
}

function speakActiveQuestion() {
  const p = POINTER_PROMPTS[currentLanguage] || POINTER_PROMPTS.en;
  if (currentPointerStep === 1) speakCurrentText(p.step1_title);
  else if (currentPointerStep === 2) speakCurrentText(p.step2_title);
  else if (currentPointerStep === 3) speakCurrentText(p.step3_title);
  else if (currentPointerStep === 4) speakCurrentText(p.step4_title);
  else if (currentPointerStep === 5) speakCurrentText(p.step5_title);
  else if (currentPointerStep === 6) speakCurrentText(p.step6_title);
  else if (currentPointerStep === 7) speakCurrentText(p.step7_title);
  else if (currentPointerStep === 8) speakCurrentText(p.step8_title);
  else if (currentPointerStep === 9) speakCurrentText(p.step9_title);
  else if (currentPointerStep === 10) speakCurrentText(p.step10_title);
  else if (currentPointerStep === 11) speakCurrentText(p.step11_title);
}

// Voice Recognition for Illiterate / Regional Patients
function initVoiceRecognition() {
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  if (!SpeechRecognition) return;

  recognition = new SpeechRecognition();
  recognition.continuous = false;
  recognition.interimResults = true;

  recognition.onstart = function() {
    isRecording = true;
    const btn = document.getElementById("pointerMicBtn");
    const text = document.getElementById("micStatusText");
    const fb = document.getElementById("voiceTranscriptFeedback");
    if (btn) btn.classList.add("recording");
    if (text) text.textContent = "Listening... बोलिए";
    if (fb) fb.textContent = "Recording in progress...";
  };

  recognition.onresult = function(event) {
    let transcript = "";
    for (let i = event.resultIndex; i < event.results.length; i++) {
      transcript += event.results[i][0].transcript;
    }
    const fb = document.getElementById("voiceTranscriptFeedback");
    if (fb) fb.textContent = `"${transcript}"`;

    handleVoicePointerAnswer(transcript.toLowerCase());
  };

  recognition.onerror = function(e) {
    resetMicUI();
  };

  recognition.onend = function() {
    resetMicUI();
  };
}

function resetMicUI() {
  isRecording = false;
  const btn = document.getElementById("pointerMicBtn");
  const text = document.getElementById("micStatusText");
  const fb = document.getElementById("voiceTranscriptFeedback");
  const t = UI_TRANSLATIONS[currentLanguage] || UI_TRANSLATIONS.en;
  if (btn) btn.classList.remove("recording");
  if (text) text.textContent = t.tapToSpeak;
  if (fb && fb.textContent.includes("Recording")) {
    fb.textContent = t.listeningWait;
  }
}

function togglePointerVoice() {
  if (!recognition) {
    alert("Speech recognition is supported on modern Chrome or Edge browsers.");
    return;
  }

  if (isRecording) {
    recognition.stop();
  } else {
    const langMap = {
      en: "en-IN",
      hi: "hi-IN",
      ta: "ta-IN",
      te: "te-IN",
      bn: "bn-IN",
      mr: "mr-IN",
      gu: "gu-IN"
    };
    recognition.lang = langMap[currentLanguage] || "hi-IN";
    try {
      recognition.start();
    } catch (err) {
      console.log("Mic start error:", err);
    }
  }
}

function handleVoicePointerAnswer(text) {
  const isAffirmative = text.includes("yes") || text.includes("haan") || text.includes("हाँ") || text.includes("ஆம்") || text.includes("అవును") || text.includes("হ্যাঁ") || text.includes("होय") || text.includes("હા") || text.includes("hota hai") || text.includes("hai");
  const isNegative = text.includes("no") || text.includes("nahin") || text.includes("नहीं") || text.includes("இல்லை") || text.includes("లేదు") || text.includes("না") || text.includes("नाही") || text.includes("ના") || text.includes("nahi");

  if (currentPointerStep >= 4 && currentPointerStep <= 11 && currentPointerStep !== 8) {
    const fieldMap = {
      4: "followup1",
      5: "followup2",
      6: "sugar",
      7: "bp",
      9: "meds",
      10: "allergies",
      11: "lifestyle"
    };
    if (isAffirmative) {
      answerPointerYesNo(fieldMap[currentPointerStep], true);
    } else if (isNegative) {
      answerPointerYesNo(fieldMap[currentPointerStep], false);
    }
  }
}

function escapeHtml(str) {
  if (!str) return "";
  return String(str)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}
'''
with open('app.js', 'w', encoding='utf-8') as out: out.write(content)
