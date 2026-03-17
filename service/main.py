"""
SkillTech AI — Single File Backend
FastAPI server with all services inlined (no subfolders needed)

Usage:
    pip install fastapi uvicorn[standard] python-multipart pdfplumber llama-cpp-python easyocr
    uvicorn main:app --reload --port 8000
    Open: http://localhost:8000
"""

import os
import json
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
    ],
    "Automation & Controls": [
        "PLC", "SCADA", "HMI", "robotics", "automation",
        "DCS", "pneumatics", "hydraulics", "servo motor",
        "VFD", "variable frequency drive", "motion control",
        "industrial automation", "control panel", "relay logic",
        "ladder logic", "PID control",
    ],
    "Mechanical": [
        "CNC", "CAD", "CAM", "SolidWorks", "AutoCAD",
        "welding", "fabrication", "machining", "lathe",
        "GD&T", "metrology", "quality control", "lean manufacturing",
        "kaizen", "6 sigma", "six sigma", "FMEA", "production planning",
    ],
    "Power Systems": [
        "transformer", "switchgear", "circuit breaker",
        "substation", "transmission", "distribution",
        "electrical maintenance", "power distribution",
        "HT", "LT", "relay", "protection system",
        "earthing", "load flow", "power factor",
    ],
    "IT & Software": [
        "Python", "MATLAB", "LabVIEW", "embedded systems",
        "microcontroller", "Arduino", "Raspberry Pi",
        "IoT", "data analysis", "machine learning",
        "C programming", "C++", "Java", "SQL",
    ],
    "Safety & Standards": [
        "ISO", "IATF", "OHSAS", "safety management",
        "OSHA", "fire safety", "risk assessment",
        "work permit", "PPE", "5S", "audit",
        "quality assurance", "QA", "QC", "testing",
    ],
    "Soft Skills": [
        "teamwork", "communication", "leadership",
        "problem solving", "time management", "project management",
        "analytical", "multitasking", "documentation",
        "reporting", "supervision", "training",
    ],
}


def extract_skills(text: str) -> dict:
    """Scan text and return matched skills grouped by category."""
    text_lower = text.lower()
    found = {}
    for category, skills in SKILL_DATABASE.items():
        matched = [s for s in skills if s.lower() in text_lower]
        if matched:
            found[category] = matched
    return found


def flatten_skills(skill_dict: dict) -> list:
    """Flatten categorised skills into a single list."""
    return [s for skills in skill_dict.values() for s in skills]


# ══════════════════════════════════════════════════════════════════
#  2. SKILL GAP ENGINE
# ══════════════════════════════════════════════════════════════════

SKILL_PRIORITY = {
    # Critical
    "EV battery": "critical", "BMS": "critical", "battery management": "critical",
    "motor control": "critical", "PLC": "critical", "SCADA": "critical",
    "EV powertrain": "critical", "power electronics": "critical",
    "electric vehicle": "critical", "charging systems": "critical",
    "inverter": "critical", "battery pack": "critical",
    "embedded systems": "critical", "CNC": "critical", "robotics": "critical",
    # Important
    "BLDC": "important", "lithium ion": "important", "cell balancing": "important",
    "DC-DC converter": "important", "onboard charger": "important",
    "HMI": "important", "DCS": "important", "VFD": "important",
    "automation": "important", "CAD": "important", "SolidWorks": "important",
    "AutoCAD": "important", "Python": "important", "MATLAB": "important",
    "IoT": "important", "microcontroller": "important", "six sigma": "important",
    "FMEA": "important", "IATF": "important", "transformer": "important",
    "substation": "important", "relay": "important", "protection system": "important",
    # Minor
    "teamwork": "minor", "communication": "minor", "leadership": "minor",
    "documentation": "minor", "reporting": "minor", "time management": "minor",
    "5S": "minor", "audit": "minor", "ISO": "minor",
    "QA": "minor", "QC": "minor", "testing": "minor",
    "work permit": "minor", "PPE": "minor",
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
}

DEFAULT_COURSE   = "Refer Naan Mudhalvan portal — https://naanmudhalvan.tn.gov.in"
DEFAULT_PRIORITY = "important"


def calculate_gap(candidate_skills: list, job_skills: list) -> dict:
    """Find missing skills and bucket them by priority."""
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
    """Return a 0–100 match score."""
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
            with open(p, newline="", encoding="utf-8") as f:
                self.courses = [dict(row) for row in csv.DictReader(f)]

    def _matches(self, skill: str, course_skill: str) -> bool:
        import re
        s, cs = skill.lower().strip(), course_skill.lower().strip()
        if s == cs:
            return True
        # Use word boundary matching to avoid "CAD" matching "SCADA"
        pattern = r'\b' + re.escape(s) + r'\b'
        if re.search(pattern, cs):
            return True
        pattern2 = r'\b' + re.escape(cs) + r'\b'
        if re.search(pattern2, s):
            return True
        # multi-word skills: all words present
        skill_words = s.split()
        if len(skill_words) > 1 and all(re.search(r'\b' + re.escape(w) + r'\b', cs) for w in skill_words):
            return True
        return False

    def find_courses(self, skill: str) -> list[CourseRec]:
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

    def recommend(
        self,
        missing_skills: list[str],
        free_only: bool = False,
        max_per_skill: int = 2,
    ) -> list[CourseRec]:
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
print(f"[RecommendationEngine] Loaded {len(_rec_engine.courses)} courses from {_COURSES_CSV}")


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
    reader  = easyocr.Reader(['en'], gpu=False)
    results = reader.readtext(filepath, detail=0, paragraph=True)
    return "\n".join(results).strip()


def parse_resume(filepath: str) -> str:
    """Extract raw text from a resume file (PDF / image / txt)."""
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
#  4. LLM  (llama-cpp — lazy loaded on first chat request)
# ══════════════════════════════════════════════════════════════════

_llm      = None
_llm_lock = threading.Lock()

# ← Set your model path here, or use the MODEL_PATH env variable
MODEL_PATH = os.environ.get(
    "MODEL_PATH",
    r"C:\Users\Lenovo\Documents\programing\NeuralDocker Selective\Microservices\models\capybarahermes-2.5-mistral-7b.Q4_K_M.gguf",
)

SYSTEM_PROMPT = """\
You are SkillTech AI — a friendly, knowledgeable career assistant for students and \
job-seekers in Tamil Nadu's automotive and EV manufacturing industry.

You can help with a wide range of questions, including:
- Career advice: which job roles suit different backgrounds, salary expectations, \
  growth paths, and how to enter the EV/automotive sector
- Skill guidance: what skills matter most for specific roles, how hard they are to \
  learn, and realistic timelines
- Course recommendations: free and affordable courses from Naan Mudhalvan, NPTEL, \
  NSDC, Government ITIs, Coursera, edX, YouTube, and CADD Centre
- Skill gap analysis: if the user shares their background or the tool has run an \
  analysis, explain their gaps clearly and suggest a practical learning plan
- Resume and interview tips: how to frame skills, what interviewers in TN automotive \
  companies look for, and how to prepare
- General industry knowledge: EV trends in India, companies hiring in Tamil Nadu, \
  which sectors are growing (Ather, Ola Electric, Tata EV, etc.)

Tone guidelines:
- Be warm, encouraging, and direct — like a helpful senior colleague
- Use simple language; avoid jargon unless the user clearly understands it
- Keep answers focused and scannable; use short bullet points for lists
- When you don't know something specific, say so honestly and suggest where to look
- Do NOT refuse to answer general career or learning questions — you are a broad \
  career helper first, not just a skill gap tool

If the user's profile or gap analysis results are provided below as context, \
use them to give personalised answers. If no context is provided, answer generally \
and helpfully — never ask the user to complete the analysis before helping them.\
"""


def _build_system_prompt(
    candidate_skills: list = None,
    job_role: str = None,
    gap_score: int = None,
    gap_skills: list = None,
) -> str:
    """Build system prompt with structured context appended only when available."""
    prompt = SYSTEM_PROMPT
    sections = []

    if candidate_skills:
        sections.append(
            "USER'S SKILLS (from resume / manual entry):\n"
            + ", ".join(candidate_skills[:40])
        )
    if job_role:
        sections.append(f"TARGET JOB ROLE: {job_role}")
    if gap_score is not None:
        sections.append(f"SKILL MATCH SCORE: {gap_score}%")
    if gap_skills:
        critical  = [g["skill"] for g in gap_skills if g.get("priority") == "critical"]
        important = [g["skill"] for g in gap_skills if g.get("priority") == "important"]
        if critical:
            sections.append("CRITICAL GAPS (must learn first):\n" + ", ".join(critical))
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
                from llama_cpp import Llama
                _llm = Llama(
                    model_path=MODEL_PATH,
                    n_ctx=4096,
                    n_threads=8,
                    n_gpu_layers=0,
                    verbose=False,
                )
    return _llm


# ══════════════════════════════════════════════════════════════════
#  FASTAPI APP + ROUTES
# ══════════════════════════════════════════════════════════════════

app = FastAPI(title="SkillTech AI", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

STATIC_DIR = Path(__file__).parent / "static"
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


@app.post("/api/skill-gap")
async def skill_gap_analysis(req: SkillGapRequest):
    job_skills_dict = extract_skills(req.job_description)
    job_skills      = flatten_skills(job_skills_dict)
    if not job_skills:
        raise HTTPException(422, "No recognizable skills found in job description.")

    gap  = calculate_gap(req.candidate_skills, job_skills)
    score = match_score(req.candidate_skills, job_skills)

    # Get rich course recommendations for all missing skills
    missing_skills = [g["skill"] for g in gap["all"]]
    recommendations = _rec_engine.recommend(missing_skills, max_per_skill=2)
    courses_by_skill = {}
    for rec in recommendations:
        courses_by_skill.setdefault(rec.skill, []).append(rec.to_dict())

    # Enrich gap items with course details
    for item in gap["all"]:
        item["courses"] = courses_by_skill.get(item["skill"], [])
    for bucket in ["critical", "important", "minor"]:
        for item in gap[bucket]:
            item["courses"] = courses_by_skill.get(item["skill"], [])

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
    # Structured context — all optional; only set when the user has that data
    candidate_skills: list[str]  = []
    job_role:         str        = ""
    gap_score:        int        = -1   # -1 means not yet run
    gap_skills:       list[dict] = []   # list of {skill, priority} dicts


@app.post("/api/chat/stream")
async def chat_stream(req: ChatMessage):
    """Streaming chat via SSE."""
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
                temperature=0.72, top_p=0.95,
                repeat_penalty=1.1, stream=True,
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
    """Non-streaming chat (convenience endpoint)."""
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