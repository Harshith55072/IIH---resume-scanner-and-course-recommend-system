/**
 * ═══════════════════════════════════════════════════════════════════
 *  SKILLTECH AI — THEME & LANGUAGE CONTROLLER
 *  theme-lang.js  |  Link this in every page before </body>
 *
 *  Features:
 *    • Dark / Light mode toggle  →  persisted in localStorage
 *    • English / Tamil toggle    →  persisted in localStorage
 *    • Floating pill widget injected automatically
 *    • Zero dependencies — works on every Alar page
 * ═══════════════════════════════════════════════════════════════════
 */

(function () {
  'use strict';

  /* ──────────────────────────────────────────────
     TRANSLATION MAP
     Keys = canonical English strings (trimmed)
     Values = Tamil equivalents
  ────────────────────────────────────────────── */
  const T = {
    /* ── Navigation ── */
    'Overview'        : 'மேலோட்டம்',
    'Analytics'       : 'பகுப்பாய்வு',
    'Skill Analyser'  : 'திறன் பகுப்பாய்வி',
    'Courses'         : 'பாடநெறிகள்',
    'Job Roles'       : 'வேலை பங்குகள்',
    'Companies'       : 'நிறுவனங்கள்',
    'SYSTEM ONLINE'   : 'அமைப்பு இயங்குகிறது',
    'TN · EV · Automotive' : 'TN · EV · வாகன',
    'OFFLINE'         : 'ஆஃப்லைன்',
    'Connecting…'     : 'இணைக்கிறது...',

    /* ── Hero eyebrow ── */
    'Tamil Nadu · EV &amp; Automotive Sector · 2025'  : 'தமிழ்நாடு · EV &amp; வாகன துறை · 2025',
    'Tamil Nadu · EV & Automotive Sector · 2025'      : 'தமிழ்நாடு · EV & வாகன துறை · 2025',
    'Tamil Nadu\'s Free Skill Gap Tool' : 'தமிழ்நாட்டின் இலவச திறன் இடைவெளி கருவி',

    /* ── Hero title lines ── */
    'WORKFORCE'     : 'தொழிலாளர்',
    'INTELLIGENCE'  : 'நுண்ணறிவு',
    'PLATFORM'      : 'தளம்',
    'Find your'     : 'உங்கள்',
    'skill gaps'    : 'திறன் இடைவெளிகள்',
    'get your learning path' : 'உங்கள் கற்றல் பாதையைப் பெறுங்கள்',

    /* ── Hero description ── */
    'AI-powered analytics platform mapping skill demand across Tamil Nadu\'s EV and automotive sector. Identify gaps, find targeted upskilling, and connect to 20+ industry roles in real-time.'
    : 'தமிழ்நாட்டின் EV மற்றும் வாகன துறையில் திறன் தேவையை வரைபடமிடும் AI ஆதரவு பகுப்பாய்வு தளம். இடைவெளிகளை அடையாளம் காணுங்கள், இலக்கு மேம்பாட்டு பயிற்சி கண்டுபிடிக்கவும், 20+ தொழிற்துறை பங்குகளுடன் நேரலையில் இணைக்கவும்.',
    'Upload your resume, choose a job you want, and we\'ll show you exactly what to learn — with free and paid courses from Tamil Nadu\'s top institutions.'
    : 'உங்கள் ரெஸ்யூமை பதிவேற்றவும், உங்களுக்கு தேவையான வேலையைத் தேர்ந்தெடுக்கவும், தமிழ்நாட்டின் சிறந்த நிறுவனங்களின் இலவச மற்றும் கட்டணப் பாடநெறிகளுடன் எதை கற்க வேண்டும் என்பதை நாங்கள் உங்களுக்குக் காண்பிப்போம்.',

    /* ── CTA buttons ── */
    'Launch Skill Analyser' : 'திறன் பகுப்பாய்வியை தொடங்கு',
    'View Analytics →'      : 'பகுப்பாய்வு காண →',
    'Analyze My Skill Gap'  : 'எனது திறன் இடைவெளியை பகுப்பாய்வு செய்',

    /* ── Stat strip ── */
    'EV Jobs by 2030'    : '2030 வரை EV வேலைகள்',
    'Skill Gap Rate'     : 'திறன் இடைவெளி விகிதம்',
    'Courses Mapped'     : 'வரைபடமிடப்பட்ட பாடங்கள்',
    'Hiring Companies'   : 'பணியமர்த்தும் நிறுவனங்கள்',
    '↑ 38% YoY'         : '↑ 38% ஆண்டுதோறும்',
    'Target <30%'        : 'இலக்கு <30%',
    'Ather · Ola · TVS'  : 'ஆதர் · ஓலா · TVS',
    'Job Roles'          : 'வேலை பங்குகள்',
    'Always'             : 'எப்போதும்',
    'Free'               : 'இலவசம்',

    /* ── Steps Bar ── */
    'Your Skills'        : 'உங்கள் திறன்கள்',
    'Target Job'         : 'இலக்கு வேலை',
    'Your Results'       : 'உங்கள் முடிவுகள்',

    /* ── Step 1 ── */
    'Tell us about your skills' : 'உங்கள் திறன்களைப் பற்றி எங்களிடம் கூறுங்கள்',
    'Upload your resume to auto-extract skills, or add them manually. You can combine both approaches.' : 'திறன்களைத் தானாகப் பிரித்தெடுக்க உங்கள் ரெஸ்யூமைப் பதிவேற்றவும் அல்லது கைமுறையாகச் சேர்க்கவும். நீங்கள் இரண்டையும் இணைக்கலாம்.',
    'Upload your resume' : 'உங்கள் ரெஸ்யூமைப் பதிவேற்றவும்',
    'Recommended' : 'பரிந்துரைக்கப்படுகிறது',
    'Drop your resume here' : 'உங்கள் ரெஸ்யூமை இங்கே விடவும்',
    'Supports' : 'ஆதரிக்கிறது',
    'click to browse' : 'உலாவ கிளிக் செய்யவும்',
    'Reading your resume…' : 'உங்கள் ரெஸ்யூமைப் படிக்கிறது...',
    'Uploading file' : 'கோப்பைப் பதிவேற்றுகிறது',
    'Extracting text' : 'உரையைப் பிரித்தெடுக்கிறது',
    'Identifying skills' : 'திறன்களைக் கண்டறிகிறது',
    'Categorising results' : 'முடிவுகளை வகைப்படுத்துகிறது',
    'Remove' : 'நீக்கு',
    'Skills extracted' : 'பிரித்தெடுக்கப்பட்ட திறன்கள்',
    'Used for your gap analysis' : 'உங்கள் இடைவெளி பகுப்பாய்விற்குப் பயன்படுத்தப்படுகிறது',
    'SKILLS' : 'திறன்கள்',
    'Add skills manually' : 'திறன்களைக் கைமுறையாகச் சேர்க்கவும்',
    'Describe your work experience' : 'உங்கள் பணி அனுபவத்தை விவரிக்கவும்',
    'Extract skills from description automatically' : 'விளக்கத்திலிருந்து திறன்களைத் தானாகப் பிரித்தெடுக்கவும்',
    'or add one by one' : 'அல்லது ஒவ்வொன்றாகச் சேர்க்கவும்',
    'Type a skill and press Enter' : 'ஒரு திறனைத் தட்டச்சு செய்து Enter அழுத்தவும்',
    'ADD' : 'சேர்',

    /* ── Step 2 ── */
    'Pick your target role' : 'உங்கள் இலக்கு பங்கைத் தேர்ந்தெடுக்கவும்',
    'Select the job you are aiming for. We will compare your skills against this role\'s requirements.' : 'நீங்கள் இலக்காகக் கொண்ட வேலையைத் தேர்ந்தெடுக்கவும். இந்த பங்கின் தேவைகளுடன் உங்கள் திறன்களை ஒப்பிடுவோம்.',
    'Search roles…' : 'பங்குகளைத் தேடுங்கள்...',
    'Suggested Roles' : 'பரிந்துரைக்கப்பட்ட பங்குகள்',
    'Or paste any job description' : 'அல்லது எந்தவொரு வேலை விளக்கத்தையும் ஒட்டவும்',
    'Paste the text from a job posting here…' : 'வேலை இடுகையிலிருந்து உரையை இங்கே ஒட்டவும்...',

    /* ── Step 3 ── */
    'Your Skill Gap Report' : 'உங்கள் திறன் இடைவெளி அறிக்கை',
    'Here is how you match up against the' : 'நீங்கள் எப்படிப் பொருந்துகிறீர்கள் என்பது இங்கே',
    'role' : 'பங்கு',
    'MATCH SCORE' : 'பொருத்த மதிப்பு',
    'Target Requirements' : 'இலக்கு தேவைகள்',
    'Your Skills' : 'உங்கள் திறன்கள்',
    'Missing Skills' : 'விடுபட்ட திறன்கள்',
    'Recommended Learning Path' : 'பரிந்துரைக்கப்பட்ட கற்றல் பாதை',
    'All Gaps' : 'அனைத்து இடைவெளிகள்',
    'Critical' : 'முக்கியமான',
    'Important' : 'முக்கியமானது',
    'Free Courses' : 'இலவச பாடநெறிகள்',
    'Must Learn First' : 'முதலில் கற்க வேண்டும்',
    'Important to Learn' : 'கற்பது முக்கியம்',
    'Good to Have' : 'இருப்பது நல்லது',
    'Must learn' : 'கண்டிப்பாக கற்க வேண்டும்',
    'Good to have' : 'இருப்பது நல்லது',

    /* ── Section labels ── */
    'Platform Modules'            : 'தள தொகுதிகள்',
    'Live Demand Snapshot'        : 'நேரலை தேவை சுருக்கம்',
    'High-Demand Roles Right Now' : 'இப்போது அதிக தேவையுள்ள பங்குகள்',
    'Platform Guide'              : 'தள வழிகாட்டி',

    /* ── Section titles ── */
    'Three Core '           : 'மூன்று அடிப்படை ',
    'Tools'                 : 'கருவிகள்',
    'Skill Demand '         : 'திறன் தேவை ',
    'Intelligence'          : 'நுண்ணறிவு',
    'Live '                 : 'நேரலை ',
    'Job Market'            : 'வேலைச்சந்தை',

    /* ── Tool card — Skill Analyser ── */
    'SKILL ANALYSER'        : 'திறன் பகுப்பாய்வி',
    'Upload a resume or describe your background. The AI engine extracts skills, scores your match against target roles, and returns a prioritised learning roadmap.'
    : 'ஒரு ரெஸ்யூமை பதிவேற்றவும் அல்லது உங்கள் பின்னணியை விவரிக்கவும். AI என்ஜின் திறன்களை பிரித்தெடுக்கும், இலக்கு பங்குகளுக்கான உங்கள் பொருத்தத்தை மதிப்பிடும், மற்றும் முன்னுரிமை கற்றல் வழிகாட்டியை வழங்கும்.',
    'Resume Upload' : 'ரெஸ்யூமே பதிவேற்றம்',
    'Gap Analysis'  : 'இடைவெளி பகுப்பாய்வு',
    'AI Chat'       : 'AI உரையாடல்',
    'Match Score'   : 'பொருத்த மதிப்பு',
    'LAUNCH →'      : 'தொடங்கு →',

    /* ── Tool card — Course Finder ── */
    'COURSE FINDER' : 'பாடநெறி தேடி',
    'Browse 314 hand-curated courses across 82 skills — NPTEL, Naan Mudhalvan, Coursera, edX, and Government ITIs. Filter by cost, duration, and certification level.'
    : '82 திறன்களில் 314 கைமுறையாக தொகுக்கப்பட்ட பாடநெறிகளை உலாவவும் — NPTEL, நான் முதல்வன், Coursera, edX மற்றும் அரசு ITI. செலவு, காலம் மற்றும் சான்றிதழ் நிலை மூலம் வடிகட்டவும்.',
    '314 Courses'   : '314 பாடநெறிகள்',
    'Free &amp; Paid' : 'இலவசம் &amp; கட்டண',
    'Free & Paid'   : 'இலவசம் & கட்டண',
    'NPTEL / IIT'   : 'NPTEL / IIT',
    'Govt. Programs': 'அரசு திட்டங்கள்',
    'BROWSE →'      : 'உலாவு →',

    /* ── Tool card — Industry Analytics ── */
    'INDUSTRY ANALYTICS' : 'தொழில் பகுப்பாய்வு',
    'Explore live skill demand data for TN\'s EV and automotive sector — top hiring roles, fastest-growing skills, company trends, and regional breakdowns.'
    : 'TN இன் EV மற்றும் வாகன துறைக்கான நேரலை திறன் தேவை தரவை ஆராயுங்கள் — சிறந்த பணியமர்த்தும் பங்குகள், வேகமாக வளரும் திறன்கள், நிறுவன போக்குகள் மற்றும் பிராந்திய பிரிவுகள்.',
    'Skill Demand'  : 'திறன் தேவை',
    'Hiring Trends' : 'பணியமர்த்தல் போக்குகள்',
    'Role Outlook'  : 'பங்கு கண்ணோட்டம்',
    'TN Focused'    : 'TN கவனம்',
    'EXPLORE →'     : 'ஆராய →',

    /* ── Badge labels ── */
    '● LIVE' : '● நேரலை',
    'BETA'   : 'பீட்டா',

    /* ── Chart panel headers ── */
    'SKILL DEMAND — TN AUTOMOTIVE 2025' : 'திறன் தேவை — TN வாகன 2025',
    'HOVER A BAR'                       : 'பட்டியை நகர்த்தவும்',
    'SKILL CLUSTER MAP'                 : 'திறன் கொத்து வரைபடம்',
    'DRAG TO ROTATE'                    : 'சுழற்ற இழுக்கவும்',
    'EV SKILL DEMAND INDEX — 2025 TREND': 'EV திறன் தேவை குறியீடு — 2025 போக்கு',
    'MOVE CURSOR OVER CHART'            : 'விளக்கப்படத்தின் மீது நகர்த்தவும்',

    /* ── Role cards ── */
    'EV Battery Engineer'               : 'EV பேட்டரி பொறியாளர்',
    'Ather Energy · Tata EV'            : 'ஆதர் எனர்ஜி · டாடா EV',
    'Robotics & Automation Tech.'       : 'ரோபாட்டிக்ஸ் & ஆட்டோமேஷன் தொழில்நுட்பம்',
    'TVS Motor · Hyundai Chennai'       : 'TVS மோட்டார் · ஹுண்டாய் சென்னை',
    'EV Charging Infra Engineer'        : 'EV சார்ஜிங் உள்கட்டமைப்பு பொறியாளர்',
    'Tata Power · EESL'                 : 'டாடா பவர் · EESL',
    'Embedded Systems Engineer'         : 'உட்பொதிந்த அமைப்பு பொறியாளர்',
    'KPIT Technologies · Bosch'         : 'KPIT தொழில்நுட்பங்கள் · போஷ்',
    'PLC / SCADA Engineer'              : 'PLC / SCADA பொறியாளர்',
    'ABB India · Siemens'               : 'ABB இந்தியா · சீமென்ஸ்',
    'Production Supervisor (EV)'        : 'உற்பத்தி மேற்பார்வையாளர் (EV)',
    'Ola Electric · Ashok Leyland'      : 'ஓலா எலக்ட்ரிக் · அசோக் லேலாண்ட்',
    'Hot'     : 'சூடான',
    'Growing' : 'வளர்ந்து வருகிறது',
    'Open'    : 'திறந்த',

    /* ── How it works — steps ── */
    'Upload Resume or Describe Background'
    : 'ரெஸ்யூமை பதிவேற்று அல்லது பின்னணியை விவரி',
    'PDF, scanned image, or plain text — skills extracted automatically via pdfplumber and easyOCR.'
    : 'PDF, ஸ்கேன் செய்யப்பட்ட படம், அல்லது எளிய உரை — pdfplumber மற்றும் easyOCR மூலம் திறன்கள் தானாக பிரித்தெடுக்கப்படும்.',

    'Select Your Target Job Role'
    : 'உங்கள் இலக்கு வேலை பங்கை தேர்ந்தெடுக்கவும்',
    'Choose from 20+ real EV & automotive roles — EV Technician, PLC Engineer, Battery Engineer and more.'
    : '20+ உண்மையான EV & வாகன பங்குகளிலிருந்து தேர்வு செய்யுங்கள் — EV தொழில்நுட்பவியலாளர், PLC பொறியாளர், பேட்டரி பொறியாளர் மற்றும் பலர்.',

    'Receive Gap Report & Match Score'
    : 'இடைவெளி அறிக்கை & பொருத்த மதிப்பை பெறுங்கள்',
    'A 0–100% match score with prioritised breakdown of critical, important, and minor skill gaps.'
    : 'முக்கியமான, முக்கியத்துவமான மற்றும் சிறிய திறன் இடைவெளிகளின் முன்னுரிமை பிரிவுடன் 0–100% பொருத்த மதிப்பு.',

    'Get Course Recommendations'
    : 'பாடநெறி பரிந்துரைகளை பெறுங்கள்',
    'Free & paid links from NPTEL, Naan Mudhalvan, Coursera, and YouTube matched to your exact gaps.'
    : 'NPTEL, நான் முதல்வன், Coursera மற்றும் YouTube இலிருந்து உங்கள் சரியான இடைவெளிகளுக்கு பொருத்தப்பட்ட இலவச & கட்டண இணைப்புகள்.',

    'Ask the AI Anything'
    : 'AI யிடம் எதையும் கேளுங்கள்',
    'Chat with Alar AI (Mistral 7B) for career advice, interview prep, and salary benchmarks.'
    : 'வாழ்க்கை ஆலோசனை, நேர்காணல் தயாரிப்பு மற்றும் சம்பள அளவுகோல்களுக்கு Alar AI (Mistral 7B) உடன் உரையாடுங்கள்.',

    /* ── About card ── */
    'About This Project'
    : 'இந்த திட்டத்தைப் பற்றி',

    /* ── Regional activity ── */
    'Regional Activity'  : 'பிராந்திய செயல்பாடு',
    'Chennai'            : 'சென்னை',
    'Hosur'              : 'ஓசூர்',
    'Coimbatore'         : 'கோயம்புத்தூர்',
    'Madurai'            : 'மதுரை',
    '~1.8L jobs · OEM & Tier-1'    : '~1.8L வேலைகள் · OEM & நிலை-1',
    '~1.1L jobs · Ather, Tata, TVS': '~1.1L வேலைகள் · ஆதர், டாடா, TVS',
    '~0.8L jobs · Tier-2 suppliers': '~0.8L வேலைகள் · நிலை-2 சப்ளையர்கள்',
    '~0.3L jobs · Emerging cluster' : '~0.3L வேலைகள் · வளர்ந்து வரும் கொத்து',

    /* ── Footer ── */
    '© 2025 Alar · Tamil Nadu Workforce Analytics'
    : '© 2025 Alar · தமிழ்நாடு தொழிலாளர் பகுப்பாய்வு',
    'Final Year Project · EV &amp; Automotive Sector'
    : 'இறுதி ஆண்டு திட்டம் · EV &amp; வாகன துறை',
    'Final Year Project · EV & Automotive Sector'
    : 'இறுதி ஆண்டு திட்டம் · EV & வாகன துறை',
  };

  /* ──────────────────────────────────────────────
     STORAGE KEYS
  ────────────────────────────────────────────── */
  const THEME_KEY = 'st_theme';   // 'light' | 'dark'
  const LANG_KEY  = 'st_lang';    // 'en'    | 'ta'

  /* ──────────────────────────────────────────────
     STATE
  ────────────────────────────────────────────── */
  let currentTheme = localStorage.getItem(THEME_KEY) || 'light';
  let currentLang  = localStorage.getItem(LANG_KEY)  || 'en';

  /* Store original text nodes so we can swap back to English */
  const originals = new Map();  // element → original innerHTML

  /* ──────────────────────────────────────────────
     APPLY THEME
  ────────────────────────────────────────────── */
  function applyTheme(theme) {
    document.body.setAttribute('data-theme', theme);
    currentTheme = theme;
    localStorage.setItem(THEME_KEY, theme);

    const btn = document.getElementById('st-theme-btn');
    if (!btn) return;
    const icon  = btn.querySelector('.st-theme-icon');
    const label = btn.querySelector('.st-theme-label');
    if (theme === 'dark') {
      icon.textContent  = '☀️';
      label.textContent = 'LIGHT';
    } else {
      icon.textContent  = '🌙';
      label.textContent = 'DARK';
    }
  }

  /* ──────────────────────────────────────────────
     TRANSLATION ENGINE
  ────────────────────────────────────────────── */

  /**
   * Walk every text node in the document.
   * For each one, check if its trimmed content matches a key in T.
   * Store original, then swap in the translation (or restore).
   */
  function translateTextNodes(lang) {
    const walker = document.createTreeWalker(
      document.body,
      NodeFilter.SHOW_TEXT,
      {
        acceptNode(node) {
          /* Skip script/style/canvas/svg text */
          const parent = node.parentElement;
          if (!parent) return NodeFilter.FILTER_REJECT;
          const tag = parent.tagName;
          if (['SCRIPT','STYLE','CANVAS','SVG'].includes(tag)) return NodeFilter.FILTER_REJECT;
          /* Skip the toggle widget itself */
          if (parent.closest('#st-controls')) return NodeFilter.FILTER_REJECT;
          const text = node.textContent.trim();
          if (!text) return NodeFilter.FILTER_REJECT;
          return NodeFilter.FILTER_ACCEPT;
        }
      }
    );

    const nodes = [];
    while (walker.nextNode()) nodes.push(walker.currentNode);

    nodes.forEach(node => {
      const text = node.textContent.trim();

      /* Save original on first encounter */
      if (!originals.has(node)) {
        originals.set(node, node.textContent);
      }

      if (lang === 'ta') {
        /* Try exact match first */
        if (T[text]) {
          node.textContent = T[text];
          return;
        }
        /* Try with HTML-decoded text */
        const decoded = text.replace(/&amp;/g, '&');
        if (T[decoded]) {
          node.textContent = T[decoded];
          return;
        }
        /* Partial match — replace known substrings */
        let replaced = node.textContent;
        for (const [en, ta] of Object.entries(T)) {
          if (replaced.includes(en)) {
            replaced = replaced.split(en).join(ta);
          }
        }
        if (replaced !== node.textContent) {
          node.textContent = replaced;
        }
      } else {
        /* Restore English */
        const orig = originals.get(node);
        if (orig !== undefined) {
          node.textContent = orig;
        }
      }
    });
  }

  function applyLang(lang) {
    document.body.setAttribute('data-lang', lang);
    currentLang = lang;
    localStorage.setItem(LANG_KEY, lang);
    translateTextNodes(lang);
    updateLangUI(lang);
  }

  function updateLangUI(lang) {
    const enBtn = document.querySelector('.st-lang-option[data-val="en"]');
    const taBtn = document.querySelector('.st-lang-option[data-val="ta"]');
    if (!enBtn || !taBtn) return;
    if (lang === 'ta') {
      enBtn.classList.remove('active');
      taBtn.classList.add('active');
    } else {
      taBtn.classList.remove('active');
      enBtn.classList.add('active');
    }
  }

  /* ──────────────────────────────────────────────
     BUILD WIDGET
  ────────────────────────────────────────────── */
  function buildWidget() {
    /* 
       We no longer build a floating widget. 
       Instead, we look for placeholders in the navbar.
       The placeholders should be:
       <div id="st-theme-mount"></div>
       <div id="st-lang-mount"></div>
    */
    const themeMount = document.getElementById('st-theme-mount');
    const langMount = document.getElementById('st-lang-mount');

    if (themeMount) {
      const themeBtn = document.createElement('button');
      themeBtn.id = 'st-theme-btn';
      themeBtn.className = 'nav-control-btn';
      themeBtn.setAttribute('aria-label', 'Toggle dark/light theme');
      themeBtn.innerHTML = `
        <span class="st-theme-icon">${currentTheme === 'dark' ? '☀️' : '🌙'}</span>
        <span class="st-theme-label">${currentTheme === 'dark' ? 'LIGHT' : 'DARK'}</span>
      `;
      themeBtn.addEventListener('click', () => {
        applyTheme(currentTheme === 'dark' ? 'light' : 'dark');
      });
      themeMount.appendChild(themeBtn);
    }

    if (langMount) {
      const langBtn = document.createElement('button');
      langBtn.id = 'st-lang-btn';
      langBtn.className = 'nav-control-btn';
      langBtn.setAttribute('aria-label', 'Toggle language');
      langBtn.innerHTML = `
        <span class="st-lang-option${currentLang === 'en' ? ' active' : ''}" data-val="en">EN</span>
        <span class="st-lang-option${currentLang === 'ta' ? ' active' : ''}" data-val="ta">தமிழ்</span>
      `;
      langBtn.addEventListener('click', () => {
        applyLang(currentLang === 'en' ? 'ta' : 'en');
      });
      langMount.appendChild(langBtn);
    }
  }

  /* ──────────────────────────────────────────────
     INIT — run as early as possible
  ────────────────────────────────────────────── */
  function init() {
    /* Apply theme immediately (before paint to avoid flash) */
    document.body.setAttribute('data-theme', currentTheme);
    document.body.setAttribute('data-lang',  currentLang);

    /* Build widget */
    buildWidget();

    /* Apply language if Tamil is saved */
    if (currentLang === 'ta') {
      /* Wait for DOM content in case script is in <head> */
      translateTextNodes('ta');
    }
  }

  /* ──────────────────────────────────────────────
     Run when DOM is ready
  ────────────────────────────────────────────── */
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

  /* ──────────────────────────────────────────────
     Re-translate after any dynamic content loads
     (Role cards, steps, region bars are generated
      by inline JS — re-run translation 600ms later)
  ────────────────────────────────────────────── */
  window.addEventListener('load', () => {
    if (currentLang === 'ta') {
      setTimeout(() => translateTextNodes('ta'), 400);
      setTimeout(() => translateTextNodes('ta'), 1200);
    }
  });

  /* ──────────────────────────────────────────────
     PUBLIC API — available as window.SkillTechUI
     Useful if other page scripts need to hook in
  ────────────────────────────────────────────── */
  window.SkillTechUI = {
    setTheme : applyTheme,
    setLang  : applyLang,
    getTheme : () => currentTheme,
    getLang  : () => currentLang,
    addTranslation: (key, value) => { T[key] = value; },
  };

})();
