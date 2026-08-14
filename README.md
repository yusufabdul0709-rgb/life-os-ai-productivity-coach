
# 🧠 LIFE-OS

```text
╔════════════════════════════════════════════════════════════╗
║                         LIFE-OS                            ║
║        PERSONAL PRODUCTIVITY COMMAND CENTER                ║
╚════════════════════════════════════════════════════════════╝

> analyze your habits
> understand your time
> improve your life
```

## `$ whoami`

Life-OS is an AI-powered screen-time analytics dashboard that
turns digital activity into actionable lifestyle insights.

Instead of simply telling users to "use their phone less",
Life-OS analyzes where their time goes and recommends
real-world alternatives.

---

## `$ features`

```text
[✓] 14-day screen-time analytics
[✓] Daily screen-time filtering
[✓] Custom screen-time goal
[✓] KPI dashboard
[✓] Category analysis
[✓] App usage analysis
[✓] Gemini AI productivity coach
[✓] Brutal-but-fair lifestyle recommendations
[✓] Dynamic daily avatar
[✓] Streamlit SaaS-style interface
```

---

## `$ tech-stack`

```text
Frontend       → Streamlit
Data           → Pandas
AI             → Google Gemini API
Visualization  → Streamlit Charts
Image API      → Pollinations
Language       → Python
Deployment     → Streamlit Community Cloud
```

---

## `$ architecture`

```text
                 ┌──────────────────┐
                 │  screentime.csv  │
                 └────────┬─────────┘
                          │
                          ▼
                 ┌──────────────────┐
                 │      Pandas      │
                 │  Data Pipeline   │
                 └────────┬─────────┘
                          │
             ┌────────────┴────────────┐
             │                         │
             ▼                         ▼
      ┌──────────────┐         ┌───────────────┐
      │ Streamlit UI │         │ Data Bridge   │
      └──────┬───────┘         └───────┬───────┘
             │                         │
             │                         ▼
             │                  ┌─────────────┐
             │                  │   Gemini    │
             │                  │ AI Coach    │
             │                  └──────┬──────┘
             │                         │
             ▼                         ▼
      ┌──────────────┐         ┌───────────────┐
      │ Visual       │         │ Personalized  │
      │ Dashboard    │         │ Advice        │
      └──────────────┘         └───────────────┘
```

---

## `$ project-structure`

```text
life-os/
│
├── app.py
├── screentime.csv
├── requirements.txt
├── README.md
├── .gitignore
└── .env
```

---

## `$ run`

```bash
git clone <your-repository-url>

cd life-os

python -m venv venv

# Windows
venv\Scripts\activate

pip install -r requirements.txt

streamlit run app.py
```

---

## `$ environment`

Create a `.env` file:

```env
GEMINI_API_KEY=your_api_key_here
```

Never commit `.env` to GitHub.

---

## `$ philosophy`

```text
Your screen time is not the enemy.

Unconscious screen time is.

Life-OS turns digital behavior
into feedback that can improve
real-world behavior.
```

---

## `$ author`

Built as a capstone project combining:

```text
Data Visualization
+
Streamlit UI/UX
+
Pandas
+
Gemini API
+
Prompt Engineering
+
AI-powered Personalization
```

# life-os-ai-productivity-coach
Life-OS is an AI-powered screen-time analytics dashboard that turns digital activity into actionable lifestyle insights.  Instead of simply telling users to "use their phone less", Life-OS analyses where their time goes and recommends real-world alternatives.

