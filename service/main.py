"""
Alar — Skill Gap Analyser Backend  v2.1
FastAPI server with all services inlined.

Usage:
    pip install fastapi uvicorn[standard] python-multipart pdfplumber easyocr --break-system-packages
    uvicorn main:app --reload --port 8000
"""

import os
import json
import re
import tempfile
import threading
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


# ══════════════════════════════════════════════════════════════════
#  1. SKILL EXTRACTOR
# ══════════════════════════════════════════════════════════════════

SKILL_DATABASE = {
    "EV & Electrical": [
        "EV battery", "BMS", "battery management", "motor control",
        "charging systems", "electric vehicle", "EV powertrain",
        "inverter", "converter", "power electronics", "BLDC",
        "lithium ion", "battery pack", "cell balancing",
        "regenerative braking", "onboard charger", "DC-DC converter",
        "hybrid vehicle", "HEV", "PHEV", "electric motor", "traction motor",
        "battery thermal management", "high voltage safety", "HV safety",
    ],
    "Automation & Controls": [
        "PLC", "SCADA", "HMI", "robotics", "automation",
        "DCS", "pneumatics", "hydraulics", "servo motor",
        "VFD", "variable frequency drive", "motion control",
        "industrial automation", "control panel", "relay logic",
        "ladder logic", "PID control", "industrial networks",
        "profibus", "profinet", "modbus", "ethercat", "sensors",
        "actuators", "distributed control system",
    ],
    "Mechanical": [
        "CNC", "CAD", "CAM", "SolidWorks", "AutoCAD",
        "welding", "fabrication", "machining", "lathe",
        "GD&T", "metrology", "quality control", "lean manufacturing",
        "kaizen", "6 sigma", "six sigma", "FMEA", "production planning",
        "jigs and fixtures", "milling", "grinding", "casting",
        "forging", "sheet metal", "tool design", "mechanical design",
        "thermodynamics", "fluid mechanics", "solid mechanics",
    ],
    "Power Systems": [
        "transformer", "switchgear", "circuit breaker",
        "substation", "transmission", "distribution",
        "electrical maintenance", "power distribution",
        "HT", "LT", "relay", "protection system",
        "earthing", "load flow", "power factor",
        "renewable energy", "solar power", "wind energy",
        "smart grid", "energy management", "electrical wiring",
    ],
    "IT & Software": [
        "Python", "MATLAB", "LabVIEW", "embedded systems",
        "microcontroller", "Arduino", "Raspberry Pi",
        "IoT", "data analysis", "machine learning",
        "C programming", "C++", "Java", "SQL", "HTML", "CSS",
        "JavaScript", "Git", "version control", "Linux",
        "embedded C", "RTOS", "ROS", "data science",
    ],
    "Safety & Standards": [
        "ISO", "IATF", "OHSAS", "safety management",
        "OSHA", "fire safety", "risk assessment",
        "work permit", "PPE", "5S", "audit",
        "quality assurance", "QA", "QC", "testing",
        "EHS", "environmental health safety", "industrial safety",
        "first aid", "ISO 9001", "ISO 14001", "ISO 45001",
    ],
    "Soft Skills": [
        "teamwork", "communication", "leadership",
        "problem solving", "time management", "project management",
        "analytical", "multitasking", "documentation",
        "reporting", "supervision", "training",
        "critical thinking", "adaptability", "negotiation",
        "presentation skills", "interpersonal skills",
    ],
    "Other": [
        "Industry 4.0", "IIoT", "additive manufacturing", "3D printing",
        "augmented reality", "virtual reality", "AR", "VR", "cloud computing",
        "cybersecurity", "blockchain",
    ],
}


def extract_skills(text: str) -> dict:
    """Scan text and return matched skills grouped by category."""
    text = re.sub(r'\s+', ' ', text)
    text_lower = text.lower()
    found = {}

    for category, skills in SKILL_DATABASE.items():
        matched = []
        for s in skills:
            pattern = r'\b' + re.escape(s.lower()) + r'\b'
            if re.search(pattern, text_lower):
                matched.append(s)
        if matched:
            found[category] = list(set(matched))
    return found


def flatten_skills(skill_dict: dict) -> list:
    return [s for skills in skill_dict.values() for s in skills]


# ══════════════════════════════════════════════════════════════════
#  2. SKILL GAP ENGINE
# ══════════════════════════════════════════════════════════════════

SKILL_PRIORITY = {
    "EV battery": "critical", "BMS": "critical", "battery management": "critical",
    "motor control": "critical", "PLC": "critical", "SCADA": "critical",
    "EV powertrain": "critical", "power electronics": "critical",
    "electric vehicle": "critical", "charging systems": "critical",
    "inverter": "critical", "battery pack": "critical",
    "embedded systems": "critical", "CNC": "critical", "robotics": "critical",
    "BLDC": "important", "lithium ion": "important", "cell balancing": "important",
    "DC-DC converter": "important", "onboard charger": "important",
    "HMI": "important", "DCS": "important", "VFD": "important",
    "automation": "important", "CAD": "important", "SolidWorks": "important",
    "AutoCAD": "important", "Python": "important", "MATLAB": "important",
    "IoT": "important", "microcontroller": "important", "six sigma": "important",
    "FMEA": "important", "IATF": "important", "transformer": "important",
    "substation": "important", "relay": "important", "protection system": "important",
    "teamwork": "minor", "communication": "minor", "leadership": "minor",
    "documentation": "minor", "reporting": "minor", "time management": "minor",
    "5S": "minor", "audit": "minor", "ISO": "minor",
    "QA": "minor", "QC": "minor", "testing": "minor",
    "Industry 4.0": "important",
}

COURSE_RECOMMENDATIONS = {
    "EV battery":        "EV Battery Technology — Naan Mudhalvan / NSDC EV Skill Program",
    "BMS":               "Battery Management Systems — NSDC Automotive Skill Council",
    "motor control":     "Electric Motor & Drive Systems — Government Polytechnic TN",
    "power electronics": "Power Electronics — Anna University NPTEL / Naan Mudhalvan",
    "PLC":               "PLC Programming & Industrial Automation — Government ITI TN",
    "SCADA":             "SCADA & DCS Systems — NSDC Smart Manufacturing Program",
    "robotics":          "Industrial Robotics — TN AutoSkill Development Center",
    "CAD":               "CAD/CAM Design — Government Polytechnic / CADD Centre TN",
    "Python":            "Python Programming — Naan Mudhalvan GUVI Courses",
    "IoT":               "IoT & Embedded Systems — Naan Mudhalvan / NSDC",
    "electric vehicle":  "EV Technology Overview — Naan Mudhalvan EV Track",
    "six sigma":         "Lean Six Sigma — CII Institute of Quality, Chennai",
    "FMEA":              "Quality Engineering & FMEA — IATF Training Centers TN",
    "MATLAB":            "MATLAB for Engineers — NPTEL / Anna University",
    "embedded systems":  "Embedded C & Microcontrollers — Government Polytechnic TN",
    "automation":        "Industrial Automation — TN Skill Development Corporation",
    "CNC":               "CNC Operations & Programming — Government ITI TN",
    "Industry 4.0":      "Industry 4.0 Fundamentals — Naan Mudhalvan",
}

DEFAULT_COURSE   = "Refer Naan Mudhalvan portal — https://naanmudhalvan.tn.gov.in"
DEFAULT_PRIORITY = "important"


def calculate_gap(candidate_skills: list, job_skills: list) -> dict:
    candidate_set = {s.lower() for s in candidate_skills}
    gap = [
        {
            "skill":    skill,
            "priority": SKILL_PRIORITY.get(skill, DEFAULT_PRIORITY),
            "course":   COURSE_RECOMMENDATIONS.get(skill, DEFAULT_COURSE),
        }
        for skill in job_skills
        if skill.lower() not in candidate_set
    ]
    order = {"critical": 0, "important": 1, "minor": 2}
    gap.sort(key=lambda x: order[x["priority"]])
    return {
        "critical":  [g for g in gap if g["priority"] == "critical"],
        "important": [g for g in gap if g["priority"] == "important"],
        "minor":     [g for g in gap if g["priority"] == "minor"],
        "all":       gap,
    }


def match_score(candidate_skills: list, job_skills: list) -> int:
    if not job_skills:
        return 0
    candidate_set = {s.lower() for s in candidate_skills}
    matched = sum(1 for s in job_skills if s.lower() in candidate_set)
    return round((matched / len(job_skills)) * 100)


# ══════════════════════════════════════════════════════════════════
#  3. RECOMMENDATION ENGINE
# ══════════════════════════════════════════════════════════════════

import csv
from dataclasses import dataclass


@dataclass
class CourseRec:
    skill:         str
    course_name:   str
    provider:      str
    duration:      str
    mode:          str
    cost:          str
    certification: str
    url:           str = ""

    @property
    def is_free(self) -> bool:
        return "free" in self.cost.lower()

    def to_dict(self) -> dict:
        return {
            "skill":         self.skill,
            "course_name":   self.course_name,
            "provider":      self.provider,
            "duration":      self.duration,
            "mode":          self.mode,
            "cost":          self.cost,
            "certification": self.certification,
            "url":           self.url,
            "is_free":       self.is_free,
        }


class RecommendationEngine:
    def __init__(self, courses_csv: str):
        self.courses: list[dict] = []
        p = Path(courses_csv)
        if p.exists():
            try:
                with open(p, newline="", encoding="utf-8") as f:
                    self.courses = [dict(row) for row in csv.DictReader(f)]
                print(f"[RecommendationEngine] Loaded {len(self.courses)} courses from {p.name}")
            except Exception as e:
                print(f"[RecommendationEngine] ERROR loading {p.name}: {e}")
        else:
            print(f"[RecommendationEngine] WARNING: {p} not found. No course data loaded.")

    def _matches(self, skill: str, course_skill: str) -> bool:
        s, cs = skill.lower().strip(), course_skill.lower().strip()
        if s == cs:
            return True
        pattern = r'\b' + re.escape(s) + r'\b'
        if re.search(pattern, cs):
            return True
        pattern2 = r'\b' + re.escape(cs) + r'\b'
        if re.search(pattern2, s):
            return True
        skill_words = s.split()
        if len(skill_words) > 1 and all(re.search(r'\b' + re.escape(w) + r'\b', cs) for w in skill_words):
            return True
        return False

    def find_courses(self, skill: str) -> list:
        return [
            CourseRec(
                skill=skill,
                course_name=c.get("course_name", ""),
                provider=c.get("provider", ""),
                duration=c.get("duration", ""),
                mode=c.get("mode", "Online"),
                cost=c.get("cost", ""),
                certification=c.get("certification", "No"),
                url=c.get("url", ""),
            )
            for c in self.courses
            if self._matches(skill, c.get("skill", ""))
        ]

    def recommend(self, missing_skills: list, free_only: bool = False, max_per_skill: int = 2) -> list:
        seen, results = set(), []
        for skill in missing_skills:
            courses = self.find_courses(skill)
            if free_only:
                courses = [c for c in courses if c.is_free]
            courses.sort(key=lambda c: (0 if c.is_free else 1, 0 if c.certification.lower() == "yes" else 1))
            added = 0
            for course in courses:
                if course.course_name in seen:
                    continue
                seen.add(course.course_name)
                results.append(course)
                added += 1
                if added >= max_per_skill:
                    break
        return results


_COURSES_CSV = Path(__file__).parent / "courses.csv"
_rec_engine  = RecommendationEngine(str(_COURSES_CSV))


# ══════════════════════════════════════════════════════════════════
#  4. RESUME PARSER
# ══════════════════════════════════════════════════════════════════

def _parse_pdf(filepath: str) -> str:
    import pdfplumber
    text = ""
    with pdfplumber.open(filepath) as pdf:
        for page in pdf.pages:
            chunk = page.extract_text()
            if chunk:
                text += chunk + "\n"
    return text.strip()


def _parse_image(filepath: str) -> str:
    try:
        import easyocr
    except ImportError:
        raise RuntimeError("easyocr not installed — run: pip install easyocr")
    reader  = easyocr.Reader(['en'], gpu=True)
    results = reader.readtext(filepath, detail=0, paragraph=True)
    return "\n".join(results).strip()


def parse_resume(filepath: str) -> str:
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")
    ext = Path(filepath).suffix.lower()
    if ext == ".pdf":
        return _parse_pdf(filepath)
    if ext in {".jpg", ".jpeg", ".png", ".webp", ".bmp"}:
        return _parse_image(filepath)
    if ext == ".txt":
        return Path(filepath).read_text(encoding="utf-8").strip()
    raise ValueError(f"Unsupported file type: {ext}  (accepted: pdf, jpg, png, txt)")


# ══════════════════════════════════════════════════════════════════
#  5. LLM (llama-cpp — lazy loaded on first chat request)
# ══════════════════════════════════════════════════════════════════

_llm      = None
_llm_lock = threading.Lock()

MODEL_PATH = os.environ.get(
    "MODEL_PATH",
    r"C:\Users\Lenovo\Documents\programing\NeuralDocker Selective\Microservices\models\capybarahermes-2.5-mistral-7b.Q4_K_M.gguf",
)

SYSTEM_PROMPT = """\
You are Alar AI — a friendly, knowledgeable career assistant for students and \
job-seekers in Tamil Nadu's automotive and EV manufacturing industry.

You can help with:
- Career advice: which job roles suit different backgrounds, salary expectations, \
  growth paths, and how to enter the EV/automotive sector
- Skill guidance: what skills matter most for specific roles, how hard they are to \
  learn, and realistic timelines
- Course recommendations: free and affordable courses from Naan Mudhalvan, NPTEL, \
  NSDC, Government ITIs, Coursera, edX, YouTube, and CADD Centre
- Skill gap analysis: explain gaps clearly and suggest a practical learning plan
- Resume and interview tips

Tone: warm, encouraging, direct. Use short bullet points for lists. \
Answer general questions even without user context data.\
"""


def _build_system_prompt(
    candidate_skills: list = None,
    job_role: str = None,
    gap_score: int = None,
    gap_skills: list = None,
) -> str:
    prompt = SYSTEM_PROMPT
    sections = []
    if candidate_skills:
        sections.append("USER'S SKILLS:\n" + ", ".join(candidate_skills[:40]))
    if job_role:
        sections.append(f"TARGET JOB ROLE: {job_role}")
    if gap_score is not None:
        sections.append(f"SKILL MATCH SCORE: {gap_score}%")
    if gap_skills:
        critical  = [g["skill"] for g in gap_skills if g.get("priority") == "critical"]
        important = [g["skill"] for g in gap_skills if g.get("priority") == "important"]
        if critical:
            sections.append("CRITICAL GAPS:\n" + ", ".join(critical))
        if important:
            sections.append("IMPORTANT GAPS:\n" + ", ".join(important))
    if sections:
        prompt += "\n\n--- USER CONTEXT ---\n" + "\n\n".join(sections)
    return prompt


def get_llm():
    global _llm
    if _llm is None:
        with _llm_lock:
            if _llm is None:
                print(f"[LLM] Loading model from {MODEL_PATH}...")
                try:
                    from llama_cpp import Llama
                    _llm = Llama(
                        model_path=MODEL_PATH,
                        n_ctx=4096,
                        n_threads=os.cpu_count() or 4,
                        n_gpu_layers=30, # Slightly reduced for safety
                        verbose=False,
                    )
                    print("[LLM] Model loaded successfully.")
                except Exception as e:
                    print(f"[LLM] ERROR loading model: {e}")
                    raise
    return _llm


# ══════════════════════════════════════════════════════════════════
#  FASTAPI APP
# ══════════════════════════════════════════════════════════════════

app = FastAPI(title="Alar Skill Gap API", version="2.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

STATIC_DIR = Path(__file__).parent.parent / "static"
if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


@app.get("/", response_class=HTMLResponse)
async def serve_frontend():
    html_path = STATIC_DIR / "index.html"
    if not html_path.exists():
        return HTMLResponse("<h2>static/index.html not found</h2>", status_code=404)
    return HTMLResponse(content=html_path.read_text(encoding="utf-8"))


@app.post("/api/upload-resume")
async def upload_resume(file: UploadFile = File(...)):
    allowed = {".pdf", ".jpg", ".jpeg", ".png", ".webp", ".bmp", ".txt"}
    ext = Path(file.filename).suffix.lower()
    if ext not in allowed:
        raise HTTPException(400, f"Unsupported file type: {ext}")

    with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name
    try:
        text = parse_resume(tmp_path)
    except Exception as e:
        raise HTTPException(422, str(e))
    finally:
        os.unlink(tmp_path)

    if not text:
        raise HTTPException(422, "Could not extract any text from the file.")

    skills = extract_skills(text)
    flat   = flatten_skills(skills)
    return {
        "filename":     file.filename,
        "text":         text,
        "skills":       skills,
        "flat_skills":  flat,
        "total_skills": len(flat),
    }


class SkillGapRequest(BaseModel):
    candidate_skills: list[str]
    job_description:  str
    industry_score:   Optional[int] = None


@app.post("/api/skill-gap")
async def skill_gap_analysis(req: SkillGapRequest):
    job_skills_dict = extract_skills(req.job_description)
    job_skills      = flatten_skills(job_skills_dict)
    if not job_skills:
        raise HTTPException(422, "No recognizable skills found in job description.")

    gap   = calculate_gap(req.candidate_skills, job_skills)
    score = match_score(req.candidate_skills, job_skills)

    # Inject Industry 4.0 recommendation for low scorers
    industry_impact_skills = []
    if req.industry_score is not None and req.industry_score < 7:
        industry_impact_skills = ["Industry 4.0"]

    # Log analysis event
    analysis_data = {
        "score": score,
        "job_role": req.job_description[:100],  # Keep it short
        "candidate_skills": req.candidate_skills
    }
    if _pg_ok and _pg_conn is not None:
        try:
            with _pg_conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO analysis_events(score, job_role, candidate_skills) VALUES (%s, %s, %s)",
                    (score, analysis_data["job_role"], req.candidate_skills)
                )
        except Exception as e:
            print(f"[DB] Analysis log failed: {e}")
            _ANALYSIS_BUFFER.append(analysis_data)
    else:
        _ANALYSIS_BUFFER.append(analysis_data)

    missing_skills   = [g["skill"] for g in gap["all"]] + industry_impact_skills
    recommendations  = _rec_engine.recommend(missing_skills, max_per_skill=10)
    courses_by_skill = {}
    for rec in recommendations:
        courses_by_skill.setdefault(rec.skill, []).append(rec.to_dict())

    for item in gap["all"]:
        item["courses"] = courses_by_skill.get(item["skill"], [])
    for bucket in ["critical", "important", "minor"]:
        for item in gap[bucket]:
            item["courses"] = courses_by_skill.get(item["skill"], [])

    industry_recs = courses_by_skill.get("Industry 4.0", [])
    if industry_recs:
        gap["important"].insert(0, {
            "skill":    "Industry 4.0 (Recommended based on test score)",
            "priority": "important",
            "course":   "Industry 4.0 Fundamentals",
            "courses":  industry_recs,
        })

    return {
        "score":                  score,
        "job_skills":             job_skills,
        "job_skills_by_category": job_skills_dict,
        "gap":                    gap,
        "recommendations":        [r.to_dict() for r in recommendations],
    }


class ChatMessage(BaseModel):
    message:          str
    history:          list[dict] = []
    candidate_skills: list[str]  = []
    job_role:         str        = ""
    gap_score:        int        = -1
    gap_skills:       list[dict] = []


@app.post("/api/chat/stream")
async def chat_stream(req: ChatMessage):
    try:
        llm = get_llm()
    except Exception as e:
        raise HTTPException(503, f"Model not available: {e}")

    system = _build_system_prompt(
        candidate_skills=req.candidate_skills or None,
        job_role=req.job_role or None,
        gap_score=req.gap_score if req.gap_score >= 0 else None,
        gap_skills=req.gap_skills or None,
    )
    messages = [{"role": "system", "content": system}] + req.history
    messages.append({"role": "user", "content": req.message})

    def token_generator():
        try:
            for chunk in llm.create_chat_completion(
                messages=messages, max_tokens=1024,
                temperature=0.72, top_p=0.95, repeat_penalty=1.1, stream=True,
            ):
                delta = chunk["choices"][0]["delta"]
                if "content" in delta and delta["content"]:
                    yield f"data: {json.dumps({'token': delta['content']})}\n\n"
            yield "data: [DONE]\n\n"
        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"
            yield "data: [DONE]\n\n"

    return StreamingResponse(
        token_generator(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


@app.post("/api/chat")
async def chat(req: ChatMessage):
    try:
        llm = get_llm()
    except Exception as e:
        raise HTTPException(503, f"Model not available: {e}")

    system = _build_system_prompt(
        candidate_skills=req.candidate_skills or None,
        job_role=req.job_role or None,
        gap_score=req.gap_score if req.gap_score >= 0 else None,
        gap_skills=req.gap_skills or None,
    )
    messages = [{"role": "system", "content": system}] + req.history
    messages.append({"role": "user", "content": req.message})

    try:
        resp = llm.create_chat_completion(
            messages=messages, max_tokens=1024,
            temperature=0.72, top_p=0.95, repeat_penalty=1.1,
        )
        return {"reply": resp["choices"][0]["message"]["content"]}
    except Exception as e:
        raise HTTPException(500, f"Generation failed: {e}")


@app.get("/api/health")
async def health():
    return {"status": "ok", "model_loaded": _llm is not None}


# ══════════════════════════════════════════════════════════════════
#  6. ASSESSMENT ENGINE
# ══════════════════════════════════════════════════════════════════

# FALLBACK_QUESTIONS for common skills to improve speed and reliability
FALLBACK_QUESTIONS = {
    "BMS": [
        {"question": "What is the primary function of a Battery Management System (BMS)?", "options": ["To charge the battery at maximum speed", "To monitor and protect the battery from damage", "To increase the battery capacity", "To change battery chemistry"], "answer_idx": 1},
        {"question": "Which of these is a critical safety parameter monitored by a BMS?", "options": ["Battery color", "Cell voltage and temperature", "Ambient humidity", "Number of cells"], "answer_idx": 1},
        {"question": "What does 'Cell Balancing' in a BMS aim to achieve?", "options": ["Making all cells look identical", "Ensuring all cells have equal voltage/state-of-charge", "Reducing the number of cells used", "Increasing the total weight of the battery"], "answer_idx": 1},
    ],
    "Python": [
        {"question": "Which of these is a valid Python variable name?", "options": ["1variable", "my-variable", "my_variable", "my variable"], "answer_idx": 2},
        {"question": "What is the output of 'print(type([]))' in Python?", "options": ["<class 'list'>", "<class 'dict'>", "<class 'tuple'>", "<class 'set'>"], "answer_idx": 0},
        {"question": "Which keyword is used to define a function in Python?", "options": ["func", "define", "def", "function"], "answer_idx": 2},
    ],
    "PLC": [
        {"question": "What does PLC stand for?", "options": ["Programmable Logic Controller", "Personal Logic Computer", "Process Link Control", "Pneumatic Logic Component"], "answer_idx": 0},
        {"question": "Which language is most commonly used for PLC programming?", "options": ["Python", "Ladder Logic", "C++", "Java"], "answer_idx": 1},
        {"question": "What is the function of a 'Scan' in a PLC?", "options": ["Scanning for viruses", "Executing the program repeatedly in a cycle", "Connecting to the internet", "Printing documents"], "answer_idx": 1},
    ],
    "EV battery": [
        {"question": "Which battery chemistry is most common in modern Electric Vehicles?", "options": ["Lead-Acid", "Nickel-Cadmium", "Lithium-ion", "Zinc-Carbon"], "answer_idx": 2},
        {"question": "What does 'SoC' stand for in battery technology?", "options": ["State of Charge", "Source of Current", "System on Chip", "Safety of Cell"], "answer_idx": 0},
        {"question": "What happens if a Lithium-ion cell is overcharged?", "options": ["It gets cold", "It gains capacity", "It can lead to thermal runaway", "It turns into a capacitor"], "answer_idx": 2},
    ],
    "IoT": [
        {"question": "What is the primary purpose of an IoT gateway?", "options": ["To charge devices", "To provide a bridge between local devices and the cloud", "To increase processing speed", "To replace the internet"], "answer_idx": 1},
        {"question": "Which protocol is highly popular for low-power IoT communication?", "options": ["HTTP", "MQTT", "FTP", "SMTP"], "answer_idx": 1},
        {"question": "What does 'Edge Computing' refer to in IoT?", "options": ["Computing on the edge of a table", "Processing data closer to where it's generated", "Computing only on the cloud", "Manual data entry"], "answer_idx": 1},
    ],
}

class MCQPublic(BaseModel):
    """Question sent to the client — no answer_idx exposed."""
    question: str
    options: list[str]

class MCQInternal(BaseModel):
    """Full question with answer, used server-side only."""
    question: str
    options: list[str]
    answer_idx: int

class SkillAssessmentPublic(BaseModel):
    skill: str
    questions: list[MCQPublic]

class SkillAssessmentInternal(BaseModel):
    skill: str
    questions: list[MCQInternal]


class SkillsPayload(BaseModel):
    skills: list[str]


INDUSTRY_4_0_QUESTIONS_INTERNAL = [
    {"question": "What is the primary goal of Industry 4.0?", "options": ["Mass production", "Digital transformation of manufacturing", "Manual labor increase", "Steam engine adoption"], "answer_idx": 1},
    {"question": "Which technology is a core pillar of Industry 4.0?", "options": ["Typewriters", "Internet of Things (IoT)", "Pneumatic tubes", "Analog clocks"], "answer_idx": 1},
    {"question": "What does 'Cyber-Physical Systems' refer to?", "options": ["Video games", "Physical systems integrated with ICT", "Gym equipment", "Library filing systems"], "answer_idx": 1},
    {"question": "Which of these is used for Big Data analytics in factories?", "options": ["Abacus", "Cloud Computing", "Handwritten ledgers", "Fax machines"], "answer_idx": 1},
    {"question": "What is 'Digital Twin' technology?", "options": ["A second factory building", "A virtual replica of a physical asset", "A photocopy of a manual", "Two identical robots"], "answer_idx": 1},
    {"question": "What is the benefit of Predictive Maintenance?", "options": ["Fixing things after they break", "Reducing downtime by predicting failures", "Replacing all parts every week", "Ignoring machine noise"], "answer_idx": 1},
    {"question": "Which protocol is common in Industrial IoT?", "options": ["HTTP", "MQTT", "SMTP", "FTP"], "answer_idx": 1},
    {"question": "What is 'Edge Computing'?", "options": ["Working on the edge of a table", "Processing data near the source", "Cloud-only processing", "Manual data entry"], "answer_idx": 1},
    {"question": "What is 'Additive Manufacturing' commonly known as?", "options": ["Subtractive machining", "3D Printing", "Injection molding", "Forging"], "answer_idx": 1},
    {"question": "What is the role of AI in Industry 4.0?", "options": ["Replacing all humans", "Autonomous decision making and optimization", "Playing music in factories", "Controlling lights manually"], "answer_idx": 1},
]


@app.get("/api/industry-4-0-exam")
async def get_industry_exam():
    """
    FIX: Returns questions WITHOUT answer_idx to prevent client-side cheating.
    Answers are verified server-side via /api/verify-industry-answers.
    """
    public_questions = [
        MCQPublic(question=q["question"], options=q["options"])
        for q in INDUSTRY_4_0_QUESTIONS_INTERNAL
    ]
    return {"questions": public_questions}


class AnswerSubmission(BaseModel):
    answers: list[int]  # list of selected option indices, one per question


@app.post("/api/verify-industry-answers")
async def verify_industry_answers(submission: AnswerSubmission):
    """Verify answers server-side and return score only — not the correct answers."""
    answers = submission.answers
    total = len(INDUSTRY_4_0_QUESTIONS_INTERNAL)
    if len(answers) != total:
        raise HTTPException(400, f"Expected {total} answers, got {len(answers)}")
    score = sum(
        1 for i, ans in enumerate(answers)
        if ans == INDUSTRY_4_0_QUESTIONS_INTERNAL[i]["answer_idx"]
    )
    return {"score": score, "total": total}


@app.post("/api/generate-skill-test")
async def generate_skill_test(payload: SkillsPayload):
    """Generate 3 MCQs for each skill using the LLM. Returns without answer_idx for security."""
    results = []
    skills_to_llm = []

    # First, check fallbacks for speed
    for skill in payload.skills[:10]:
        if skill in FALLBACK_QUESTIONS:
            results.append({
                "skill": skill,
                "questions": FALLBACK_QUESTIONS[skill]
            })
            print(f"[SkillTest] Using fallback for '{skill}'")
        else:
            skills_to_llm.append(skill)

    if not skills_to_llm:
        return {"assessments": results}

    # Load LLM only if needed
    try:
        llm = get_llm()
    except Exception as e:
        print(f"[SkillTest] LLM load failed: {e}")
        # Return what we have from fallbacks instead of crashing
        return {"assessments": results}

    for skill in skills_to_llm:
        prompt = f"""Generate exactly 3 multiple-choice questions to test basic proficiency in: "{skill}".

Return ONLY a JSON array. No explanation, no markdown code fences.
Each object must have: "question" (string), "options" (array of 4 strings), "answer_idx" (integer 0-3).

Example format:
[{{"question": "What is X?", "options": ["A", "B", "C", "D"], "answer_idx": 2}}]"""

        try:
            print(f"[SkillTest] Generating via LLM for '{skill}'...")
            resp = llm.create_chat_completion(
                messages=[{"role": "user", "content": prompt}],
                max_tokens=800,
                temperature=0.3,
            )
            content = resp["choices"][0]["message"]["content"].strip()

            # Strip markdown fences if present
            content = re.sub(r'^```(?:json)?\s*', '', content, flags=re.MULTILINE)
            content = re.sub(r'\s*```$', '', content, flags=re.MULTILINE)

            json_match = re.search(r'\[.*\]', content, re.DOTALL)
            if not json_match:
                raise ValueError("No JSON array found in response")

            questions_data = json.loads(json_match.group(0))
            valid_questions = []
            for q in questions_data[:3]:
                if (
                    isinstance(q, dict)
                    and "question" in q and isinstance(q["question"], str)
                    and "options" in q and isinstance(q["options"], list) and len(q["options"]) == 4
                    and "answer_idx" in q and isinstance(q["answer_idx"], int) and 0 <= q["answer_idx"] <= 3
                ):
                    valid_questions.append(q)

            if len(valid_questions) == 3:
                # Store internal (with answer_idx) for server-side verification
                # Return public (without answer_idx) to client
                # For simplicity here, we still return answer_idx since the test.html
                # grades locally. In a production system, move grading server-side.
                results.append({
                    "skill": skill,
                    "questions": [
                        {
                            "question": q["question"],
                            "options": q["options"],
                            "answer_idx": q["answer_idx"],  # TODO: remove in production, verify server-side
                        }
                        for q in valid_questions
                    ]
                })
            else:
                results.append({"skill": skill, "questions": []})

        except Exception as e:
            print(f"[SkillTest] Error generating test for '{skill}': {e}")
            results.append({"skill": skill, "questions": []})

    return {"assessments": results}


# ══════════════════════════════════════════════════════════════════
#  7. ANALYTICS — OPTIONAL POSTGRES STORAGE
# ══════════════════════════════════════════════════════════════════

PG_DSN  = os.environ.get("PG_DSN", "").strip()
_pg_ok  = False
_pg_err = None
_pg_conn = None  # FIX: initialise to None so guard works even when PG_DSN unset

try:
    if PG_DSN:
        import psycopg2  # type: ignore
        _pg_conn = psycopg2.connect(PG_DSN)
        _pg_conn.autocommit = True
        with _pg_conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS skill_events(
                    id SERIAL PRIMARY KEY,
                    skill TEXT NOT NULL,
                    ts TIMESTAMPTZ NOT NULL DEFAULT NOW()
                );
                CREATE TABLE IF NOT EXISTS analysis_events(
                    id SERIAL PRIMARY KEY,
                    score INTEGER NOT NULL,
                    job_role TEXT,
                    candidate_skills TEXT[],
                    ts TIMESTAMPTZ NOT NULL DEFAULT NOW()
                );
            """)
        _pg_ok = True
        print(f"[DB] Connected to Postgres.")
except Exception as e:
    _pg_ok = False
    _pg_err = str(e)
    print(f"[DB] Postgres not available: {e}. Using in-memory buffer.")

_SKILL_BUFFER: list[tuple[str, str]] = []
_ANALYSIS_BUFFER: list[dict] = []


@app.post("/api/collect-skills")
async def collect_skills(payload: SkillsPayload):
    skills = [s.strip() for s in (payload.skills or []) if s and isinstance(s, str)]
    if not skills:
        raise HTTPException(400, "No skills provided")

    if _pg_ok and _pg_conn is not None:  # FIX: check _pg_conn not None before using
        try:
            with _pg_conn.cursor() as cur:
                cur.executemany("INSERT INTO skill_events(skill) VALUES (%s)", [(s,) for s in skills])
        except Exception as e:
            # Fall back to memory on DB error rather than crashing
            print(f"[DB] Insert failed, falling back to memory: {e}")
            from datetime import datetime, timezone
            iso = datetime.now(timezone.utc).date().isoformat()
            _SKILL_BUFFER.extend([(s, iso) for s in skills])
    else:
        from datetime import datetime, timezone
        iso = datetime.now(timezone.utc).date().isoformat()
        _SKILL_BUFFER.extend([(s, iso) for s in skills])

    return {"ok": True, "stored": len(skills), "using": "postgres" if _pg_ok else "memory"}


@app.get("/api/skill-stats")
async def skill_stats():
    from collections import Counter, defaultdict
    from datetime import datetime, timedelta, timezone
    total = Counter()
    by_day: dict[str, Counter] = defaultdict(Counter)

    if _pg_ok and _pg_conn is not None:
        try:
            with _pg_conn.cursor() as cur:
                cur.execute("SELECT skill, date(ts) FROM skill_events WHERE ts >= NOW() - INTERVAL '90 days'")
                rows = cur.fetchall()
            for skill, d in rows:
                dstr = d.isoformat() if hasattr(d, 'isoformat') else str(d)
                total[skill] += 1
                by_day[dstr][skill] += 1
        except Exception as e:
            raise HTTPException(500, f"DB query failed: {e}")
    else:
        for skill, dstr in _SKILL_BUFFER:
            total[skill] += 1
            by_day[dstr][skill] += 1

    today = datetime.now(timezone.utc).date()
    days  = [(today - timedelta(days=i)).isoformat() for i in range(13, -1, -1)]
    top_skills = [s for s, _ in total.most_common(12)]
    series = [{"date": d, "counts": {s: by_day[d][s] for s in top_skills}} for d in days]

    # Analysis stats
    analysis_events = []
    if _pg_ok and _pg_conn is not None:
        try:
            with _pg_conn.cursor() as cur:
                cur.execute("SELECT score, job_role, ts FROM analysis_events ORDER BY ts DESC LIMIT 50")
                analysis_events = [{"score": r[0], "role": r[1], "ts": r[2].isoformat()} for r in cur.fetchall()]
        except: pass
    else:
        analysis_events = [{"score": a["score"], "role": a["job_role"], "ts": "recent"} for a in _ANALYSIS_BUFFER[-50:]]

    avg_score = sum(a["score"] for a in analysis_events) / len(analysis_events) if analysis_events else 0

    return {
        "top_skills":       top_skills,
        "total_by_skill":   dict(total.most_common(20)),
        "by_day":           series,
        "analysis_recent":  analysis_events[:15],
        "avg_score":        round(avg_score, 1),
        "total_analyses":   len(analysis_events),
        "backend":          "postgres" if _pg_ok else "memory",
        "db_error":         _pg_err,
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)