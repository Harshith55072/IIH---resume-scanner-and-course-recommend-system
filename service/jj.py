"""
======================================================
  Automotive & EV Industry Dataset Generator
  Member 1 — Data Collection & Dataset Builder
  Generates 10,000 job records + 10,000 student records
  Output: jobs.csv, students.csv, jobs.json, students.json
======================================================
"""

import json
import csv
import random
import os
from datetime import datetime, timedelta

# ─────────────────────────────────────────────
# 1. SEED DATA — Real Industry Knowledge Base
# ─────────────────────────────────────────────

COMPANIES = [
    "Hyundai Motor India", "Ashok Leyland", "TVS Motor Company",
    "Tata Motors", "Mahindra Electric", "Maruti Suzuki",
    "Hero MotoCorp", "Bajaj Auto", "Ola Electric", "Ather Energy",
    "Revolt Motors", "Ampere Vehicles", "Okinawa Autotech",
    "Exide Industries", "Amara Raja Batteries", "Motherson Sumi",
    "Bosch India", "Minda Industries", "Varroc Engineering",
    "Sona BLW Precision", "Greaves Electric", "KPIT Technologies",
    "Tata AutoComp", "Uno Minda", "Schaeffler India",
    "ZF India", "Continental Automotive", "Delphi Technologies India",
    "Cummins India", "Eicher Motors",
]

SOURCES = ["LinkedIn", "Naukri", "Indeed", "Company Career Page", "Shine.com", "Monster India"]

LOCATIONS = [
    "Chennai", "Pune", "Bangalore", "Hyderabad", "Mumbai",
    "Delhi NCR", "Ahmedabad", "Coimbatore", "Hosur", "Manesar",
    "Chakan", "Gurgaon", "Noida", "Faridabad", "Lucknow",
]

EXPERIENCE_LEVELS = ["Fresher", "1-2 Years", "2-4 Years", "4-7 Years", "7-10 Years", "10+ Years"]

SALARY_RANGES = [
    "2.5-3.5 LPA", "3-5 LPA", "5-8 LPA", "8-12 LPA",
    "12-18 LPA", "18-25 LPA", "25-35 LPA", "35+ LPA",
]

EDUCATION = [
    "BE/B.Tech (Mechanical)", "BE/B.Tech (Electrical)", "BE/B.Tech (Electronics)",
    "BE/B.Tech (Automobile)", "Diploma (Mechanical)", "Diploma (Electrical)",
    "Diploma (Automobile)", "ITI (Fitter)", "ITI (Electrician)", "ITI (Welder)",
    "M.Tech (EV Technology)", "MBA (Operations)", "B.Sc (Physics/Chemistry)",
]

# ─────────────────────────────────────────────
# 2. JOB ROLES + SKILL CLUSTERS
# ─────────────────────────────────────────────

JOB_SKILL_MAP = {
    "EV Technician": [
        "battery management system", "EV diagnostics", "high voltage safety",
        "electric motor testing", "CAN bus protocol", "BMS calibration",
        "thermal management", "OBC (onboard charger)", "DC-DC converter",
        "EV drivetrain", "regenerative braking", "DCFC charging standards",
        "oscilloscope usage", "multimeter proficiency", "HV battery replacement",
    ],
    "Battery Engineer": [
        "lithium-ion chemistry", "cell characterization", "BMS design",
        "battery pack assembly", "electrochemical testing", "SOC/SOH estimation",
        "thermal runaway prevention", "NMC/LFP technology", "cycle life testing",
        "impedance spectroscopy", "formation cycling", "aging analysis",
        "Python for data analysis", "MATLAB", "CAD for battery pack",
    ],
    "Powertrain Engineer": [
        "electric motor design", "PMSM/BLDC motors", "inverter design",
        "motor control algorithms", "FOC (field oriented control)", "gear ratio optimization",
        "NVH analysis", "thermal management", "MATLAB/Simulink", "dyno testing",
        "CAN/LIN protocols", "AUTOSAR", "MISRA C", "HIL testing",
    ],
    "Automation Technician": [
        "PLC programming", "SCADA systems", "HMI programming",
        "Siemens S7", "Allen Bradley", "pneumatics",
        "hydraulics", "conveyor systems", "robotic integration",
        "sensor calibration", "ladder logic", "fault diagnosis",
        "preventive maintenance", "ISO 9001", "lean manufacturing",
    ],
    "Robotics Engineer": [
        "ROS (Robot Operating System)", "industrial robotics", "FANUC programming",
        "ABB robot programming", "KUKA robot programming", "path planning",
        "end-effector design", "computer vision", "OpenCV", "Python",
        "C++", "motion control", "force/torque sensing", "simulation (Gazebo)",
        "servo motor control",
    ],
    "CNC Machinist": [
        "CNC turning", "CNC milling", "G-code programming",
        "M-code programming", "Fanuc CNC", "Siemens CNC",
        "precision measurement", "Vernier caliper", "CMM operation",
        "fixture design", "tooling selection", "GD&T",
        "SPC (Statistical Process Control)", "CAM software", "surface finish analysis",
    ],
    "Quality Engineer": [
        "IATF 16949", "PPAP", "FMEA",
        "control plan", "MSA (Measurement System Analysis)", "SPC",
        "8D problem solving", "APQP", "Six Sigma",
        "lean manufacturing", "Poka-yoke", "CMM programming",
        "GD&T", "defect analysis", "supplier quality management",
    ],
    "Embedded Systems Engineer": [
        "C/C++ programming", "RTOS", "CAN bus",
        "LIN bus", "AUTOSAR", "ECU development",
        "MISRA C", "MATLAB/Simulink", "model-based development",
        "HIL testing", "SIL testing", "ISO 26262",
        "microcontroller (ARM Cortex)", "bootloader development", "OTA updates",
    ],
    "Welding Engineer": [
        "MIG welding", "TIG welding", "spot welding",
        "laser welding", "weld quality inspection", "NDT (non-destructive testing)",
        "welding procedure specification", "ASME standards", "robotic welding",
        "metallurgy", "heat treatment", "distortion control",
        "weld mapping", "ultrasonic testing", "radiographic testing",
    ],
    "R&D Engineer – EV": [
        "vehicle dynamics", "range optimization", "aerodynamics",
        "lightweight materials", "CFD simulation", "FEA analysis",
        "ADAS integration", "V2G technology", "solid-state batteries",
        "charging infrastructure", "energy management systems", "MATLAB/Simulink",
        "Python", "patent writing", "prototype development",
    ],
    "Production Supervisor": [
        "production planning", "OEE optimization", "5S methodology",
        "Kaizen", "TPM (Total Productive Maintenance)", "line balancing",
        "ERP (SAP)", "team management", "shift scheduling",
        "safety compliance", "IATF 16949", "cost reduction",
        "inventory management", "root cause analysis", "KPI monitoring",
    ],
    "Supply Chain Manager": [
        "SAP ERP", "vendor management", "logistics coordination",
        "demand forecasting", "just-in-time (JIT)", "kanban",
        "import/export compliance", "cost negotiation", "supplier development",
        "risk management", "procurement strategy", "inventory optimization",
        "INCOTERMS", "ERP (Oracle)", "sustainability procurement",
    ],
    "EV Charging Infrastructure Engineer": [
        "AC/DC charging protocols", "CHAdeMO", "CCS (Combined Charging System)",
        "OCPP protocol", "smart grid integration", "load balancing",
        "electrical panel design", "site assessment", "energy metering",
        "IoT for EV charging", "V2G (Vehicle to Grid)", "network management",
        "cybersecurity for EV", "Python for backend", "cloud platforms",
    ],
    "Automotive Software Engineer": [
        "AUTOSAR Classic/Adaptive", "C/C++", "Python",
        "ISO 26262 functional safety", "SOTIF", "DevOps for automotive",
        "CI/CD pipelines", "Git", "DOORS (requirements management)",
        "Vector tools (CANalyzer, CANoe)", "Jira", "Agile/Scrum",
        "model-based design", "dSPACE", "MATLAB/Simulink",
    ],
    "Mechanical Design Engineer": [
        "CATIA V5/V6", "SolidWorks", "AutoCAD",
        "NX (Siemens)", "FEA (ANSYS)", "GD&T",
        "sheet metal design", "casting/forging design", "DFM/DFA",
        "tolerance stack-up analysis", "BOM management", "PLM tools",
        "prototype fabrication", "material selection", "cost estimation",
    ],
    "EV Motor Design Engineer": [
        "PMSM design", "BLDC motor design", "winding design",
        "magnetic circuit analysis", "FEA (ANSYS Maxwell)", "thermal analysis",
        "efficiency mapping", "NVH optimization", "motor testing protocols",
        "Simulink motor models", "inverter-motor co-design", "rare earth magnets",
        "copper loss analysis", "iron loss analysis", "cooling design",
    ],
    "Data Analyst – Automotive": [
        "Python (pandas, numpy)", "SQL", "Power BI",
        "Tableau", "vehicle telematics data", "predictive maintenance",
        "machine learning basics", "statistical analysis", "A/B testing",
        "data pipeline creation", "Excel (advanced)", "R programming",
        "KPI dashboards", "anomaly detection", "fleet analytics",
    ],
    "IoT Engineer – Connected Vehicles": [
        "MQTT protocol", "AWS IoT", "Azure IoT Hub",
        "OBD-II integration", "CAN bus data parsing", "edge computing",
        "Python", "C++", "embedded Linux",
        "cloud data storage", "API development", "cybersecurity basics",
        "GPS/GNSS systems", "4G/5G connectivity", "OTA firmware updates",
    ],
    "Safety Engineer – EV": [
        "ISO 26262", "IEC 61851", "FMEA",
        "FTA (Fault Tree Analysis)", "high voltage safety (HVIL)", "arc flash analysis",
        "thermal runaway mitigation", "crash test analysis", "NCAP standards",
        "risk assessment", "safety case development", "SOTIF",
        "EMC testing", "IP67/IP68 certification", "UL certification",
    ],
    "ITI Fitter – Automotive": [
        "assembly fitting", "precision measurement", "drilling",
        "tapping", "grinding", "filing",
        "blueprint reading", "hydraulic systems", "pneumatics",
        "preventive maintenance", "safety procedures", "hand tools usage",
        "surface plate work", "marking and scribing", "quality checking",
    ],
}

# ─────────────────────────────────────────────
# 3. STUDENT PROFILES SEED DATA
# ─────────────────────────────────────────────

FIRST_NAMES = [
    "Arun", "Priya", "Rahul", "Sneha", "Vikram", "Kavya", "Suresh", "Anitha",
    "Manoj", "Deepika", "Ravi", "Pooja", "Karthik", "Meena", "Arjun", "Nisha",
    "Dinesh", "Lakshmi", "Rajesh", "Divya", "Sanjay", "Anu", "Gopal", "Swathi",
    "Venkat", "Bhavana", "Harish", "Rekha", "Naveen", "Sindhu", "Praveen", "Uma",
    "Balaji", "Nalini", "Selvam", "Geetha", "Muthukumar", "Saranya", "Elan", "Kiruba",
    "Mohammed", "Fatima", "Imran", "Zainab", "Farhan", "Sana", "Aarav", "Ishaan",
    "Rohan", "Ananya", "Kabir", "Zara", "Dev", "Tanvi", "Nikhil", "Shreya",
    "Akash", "Ritu", "Yash", "Nidhi", "Aryan", "Palak", "Vivek", "Komal",
]

LAST_NAMES = [
    "Kumar", "Sharma", "Patel", "Singh", "Reddy", "Nair", "Iyer", "Pillai",
    "Krishnan", "Venkatesh", "Murugan", "Rajan", "Subramaniam", "Chandran",
    "Gupta", "Mehta", "Shah", "Joshi", "Desai", "Verma", "Mishra", "Tiwari",
    "Yadav", "Pandey", "Sinha", "Das", "Roy", "Ghosh", "Bose", "Chatterjee",
    "Khan", "Ali", "Ahmed", "Shaikh", "Siddiqui", "Ansari", "Qureshi",
]

COLLEGES = [
    "Anna University", "VIT Vellore", "NIT Trichy", "PSG Tech Coimbatore",
    "SRM Institute of Science and Technology", "Amrita School of Engineering",
    "College of Engineering Pune", "Pune Vidyarthi Griha", "Symbiosis Institute",
    "Manipal Institute of Technology", "BITS Pilani", "IIT Madras",
    "IIT Bombay", "IIT Delhi", "RVCE Bangalore", "MSRIT Bangalore",
    "Osmania University", "JNTU Hyderabad", "Andhra University",
    "Government Polytechnic Chennai", "Central Polytechnic College",
    "Bharathiar University", "Kongu Engineering College", "Kumaraguru College",
    "Sri Venkateswara College of Engineering", "Rajalakshmi Engineering College",
    "ITI Coimbatore", "ITI Chennai", "ITI Pune", "ITI Hyderabad",
]

STUDENT_SKILL_POOL = {
    "mechanical": [
        "welding", "CNC machining", "lathe operation", "milling", "drilling",
        "AutoCAD", "SolidWorks", "CATIA", "GD&T", "blueprint reading",
        "fitting", "sheet metal work", "casting", "forging", "heat treatment",
        "hydraulics", "pneumatics", "preventive maintenance",
    ],
    "electrical": [
        "electronics", "circuit design", "PCB design", "Arduino",
        "Raspberry Pi", "embedded C", "MATLAB", "power electronics",
        "motor control", "PLC basics", "sensor interfacing",
        "oscilloscope", "multimeter", "soldering", "wiring",
    ],
    "ev_specific": [
        "EV systems basics", "battery management", "electric motors",
        "Python programming", "IoT basics", "CAN bus fundamentals",
        "EV charging systems", "BMS awareness", "high voltage awareness",
        "vehicle diagnostics", "telematics",
    ],
    "software": [
        "Python", "C programming", "MATLAB/Simulink", "SQL basics",
        "Excel (advanced)", "data analysis", "machine learning basics",
        "Git", "Linux basics", "REST API basics",
    ],
    "soft_skills": [
        "team collaboration", "problem solving", "communication",
        "time management", "report writing", "project management basics",
        "leadership", "critical thinking",
    ],
}

# ─────────────────────────────────────────────
# 4. DATA GENERATION FUNCTIONS
# ─────────────────────────────────────────────

def generate_job_id(index):
    return f"JOB-{str(index).zfill(5)}"

def generate_student_id(index):
    return f"STU-{str(index).zfill(5)}"

def pick_skills(role, min_skills=3, max_skills=8):
    """Pick a random subset of skills for a job role."""
    pool = JOB_SKILL_MAP.get(role, [])
    n = random.randint(min_skills, min(max_skills, len(pool)))
    return random.sample(pool, n)

def pick_student_skills():
    """Randomly combine skills from multiple categories for a student."""
    selected = []
    for category, skills in STUDENT_SKILL_POOL.items():
        weight = {
            "mechanical": 0.75,
            "electrical": 0.65,
            "ev_specific": 0.45,
            "software": 0.55,
            "soft_skills": 0.85,
        }.get(category, 0.5)
        if random.random() < weight:
            n = random.randint(1, min(4, len(skills)))
            selected.extend(random.sample(skills, n))
    # ensure at least 3 skills
    if len(selected) < 3:
        selected += random.sample(STUDENT_SKILL_POOL["mechanical"], 3)
    return list(dict.fromkeys(selected))  # deduplicate while preserving order

def random_date(start_days_ago=365, end_days_ago=0):
    today = datetime.today()
    delta = random.randint(end_days_ago, start_days_ago)
    d = today - timedelta(days=delta)
    return d.strftime("%Y-%m-%d")

def generate_job_record(index):
    role = random.choice(list(JOB_SKILL_MAP.keys()))
    skills = pick_skills(role)
    company = random.choice(COMPANIES)
    location = random.choice(LOCATIONS)
    source = random.choice(SOURCES)
    exp = random.choice(EXPERIENCE_LEVELS)
    salary = random.choice(SALARY_RANGES)
    edu = random.choice(EDUCATION)
    posted_date = random_date()
    openings = random.randint(1, 15)

    is_ev = any(kw in role.lower() for kw in ["ev", "battery", "electric", "charging"])
    industry_segment = "Electric Vehicle (EV)" if is_ev else "Conventional Automotive"

    return {
        "job_id": generate_job_id(index),
        "job_role": role,
        "company": company,
        "location": location,
        "industry_segment": industry_segment,
        "experience_required": exp,
        "education": edu,
        "salary_range": salary,
        "openings": openings,
        "source": source,
        "date_posted": posted_date,
        "skills": skills,
        "skills_str": ", ".join(skills),   # flat string for CSV
    }

def generate_student_record(index):
    first = random.choice(FIRST_NAMES)
    last = random.choice(LAST_NAMES)
    name = f"{first} {last}"
    college = random.choice(COLLEGES)
    edu = random.choice(EDUCATION)
    grad_year = random.randint(2018, 2025)
    skills = pick_student_skills()
    exp_years = random.choice(["Fresher", "0.5 Years", "1 Year", "1.5 Years", "2 Years", "3 Years"])
    location = random.choice(LOCATIONS)
    age = random.randint(19, 30)

    # preferred roles based on skills
    ev_interest = any(s in skills for s in ["EV systems basics", "battery management",
                                             "electric motors", "IoT basics", "CAN bus fundamentals"])
    preferred_roles = random.sample(list(JOB_SKILL_MAP.keys()), 3)

    return {
        "student_id": generate_student_id(index),
        "student": name,
        "age": age,
        "college": college,
        "education": edu,
        "graduation_year": grad_year,
        "location": location,
        "experience": exp_years,
        "ev_interest": "Yes" if ev_interest else "No",
        "preferred_roles": preferred_roles,
        "preferred_roles_str": ", ".join(preferred_roles),
        "skills": skills,
        "skills_str": ", ".join(skills),
    }

# ─────────────────────────────────────────────
# 5. MAIN GENERATOR — 10,000 RECORDS EACH
# ─────────────────────────────────────────────

def generate_all_datasets(n=10000, output_dir="."):
    os.makedirs(output_dir, exist_ok=True)
    print(f"\n{'='*55}")
    print(f"  Automotive & EV Dataset Generator")
    print(f"  Generating {n:,} job records + {n:,} student records")
    print(f"{'='*55}\n")

    # ── JOBS ──────────────────────────────────────
    print("⚙️  Generating job records...")
    jobs = [generate_job_record(i + 1) for i in range(n)]
    print(f"   ✅ {len(jobs):,} job records generated")

    # jobs.csv
    jobs_csv_path = os.path.join(output_dir, "jobs.csv")
    with open(jobs_csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "job_id", "job_role", "company", "location", "industry_segment",
            "experience_required", "education", "salary_range", "openings",
            "source", "date_posted", "skills_str"
        ])
        writer.writeheader()
        for job in jobs:
            row = {k: v for k, v in job.items() if k != "skills" and k != "preferred_roles"}
            writer.writerow(row)
    print(f"   📄 Saved: {jobs_csv_path}")

    # jobs.json (full, with skills as array)
    jobs_json_path = os.path.join(output_dir, "jobs.json")
    jobs_clean = [{k: v for k, v in j.items() if k != "skills_str"} for j in jobs]
    with open(jobs_json_path, "w", encoding="utf-8") as f:
        json.dump({
            "metadata": {
                "dataset": "Automotive & EV Job Descriptions",
                "total_records": n,
                "generated_on": datetime.today().strftime("%Y-%m-%d"),
                "sources": SOURCES,
                "companies_covered": COMPANIES,
                "job_roles": list(JOB_SKILL_MAP.keys()),
            },
            "jobs": jobs_clean,
        }, f, indent=2, ensure_ascii=False)
    print(f"   📦 Saved: {jobs_json_path}")

    # ── STUDENTS ──────────────────────────────────
    print("\n👨‍🎓 Generating student records...")
    students = [generate_student_record(i + 1) for i in range(n)]
    print(f"   ✅ {len(students):,} student records generated")

    # students.csv
    students_csv_path = os.path.join(output_dir, "students.csv")
    with open(students_csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "student_id", "student", "age", "college", "education",
            "graduation_year", "location", "experience", "ev_interest",
            "preferred_roles_str", "skills_str"
        ])
        writer.writeheader()
        for s in students:
            row = {k: v for k, v in s.items() if k not in ("skills", "preferred_roles")}
            writer.writerow(row)
    print(f"   📄 Saved: {students_csv_path}")

    # students.json
    students_json_path = os.path.join(output_dir, "students.json")
    students_clean = [{k: v for k, v in s.items() if k not in ("skills_str", "preferred_roles_str")} for s in students]
    with open(students_json_path, "w", encoding="utf-8") as f:
        json.dump({
            "metadata": {
                "dataset": "Automotive Industry Student Skill Profiles",
                "total_records": n,
                "generated_on": datetime.today().strftime("%Y-%m-%d"),
                "skill_categories": list(STUDENT_SKILL_POOL.keys()),
            },
            "students": students_clean,
        }, f, indent=2, ensure_ascii=False)
    print(f"   📦 Saved: {students_json_path}")

    # ── SUMMARY JSON ──────────────────────────────
    summary = {
        "project": "Automotive & EV Industry Skill Gap Analysis",
        "member": "Member 1 — Data Collection & Dataset Builder",
        "generated_on": datetime.today().strftime("%Y-%m-%d %H:%M"),
        "total_records": n * 2,
        "files": {
            "jobs_csv": "jobs.csv",
            "jobs_json": "jobs.json",
            "students_csv": "students.csv",
            "students_json": "students.json",
        },
        "statistics": {
            "total_job_records": n,
            "total_student_records": n,
            "unique_job_roles": len(JOB_SKILL_MAP),
            "unique_companies": len(COMPANIES),
            "unique_locations": len(LOCATIONS),
            "unique_colleges": len(COLLEGES),
        },
        "top_companies": COMPANIES[:10],
        "job_roles_covered": list(JOB_SKILL_MAP.keys()),
        "sources": SOURCES,
    }
    summary_path = os.path.join(output_dir, "dataset_summary.json")
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)
    print(f"\n📊 Summary saved: {summary_path}")

    # ── FINAL REPORT ──────────────────────────────
    print(f"\n{'='*55}")
    print("  ✅ ALL DATASETS GENERATED SUCCESSFULLY")
    print(f"{'='*55}")
    print(f"  📁 Output Directory  : {os.path.abspath(output_dir)}")
    print(f"  📄 jobs.csv          : {n:,} records")
    print(f"  📦 jobs.json         : {n:,} records")
    print(f"  📄 students.csv      : {n:,} records")
    print(f"  📦 students.json     : {n:,} records")
    print(f"  📊 dataset_summary   : 1 file")
    print(f"{'='*55}")
    print(f"\n  Sample job record:")
    sample_job = jobs[0]
    print(f"    Role    : {sample_job['job_role']}")
    print(f"    Company : {sample_job['company']}")
    print(f"    Skills  : {sample_job['skills_str']}")
    print(f"\n  Sample student record:")
    sample_stu = students[0]
    print(f"    Name    : {sample_stu['student']}")
    print(f"    College : {sample_stu['college']}")
    print(f"    Skills  : {sample_stu['skills_str']}")
    print()

    return jobs, students


# ─────────────────────────────────────────────
# 6. ENTRY POINT
# ─────────────────────────────────────────────

if __name__ == "__main__":
    OUTPUT_DIR = "./automotive_ev_dataset"
    generate_all_datasets(n=10000, output_dir=OUTPUT_DIR)