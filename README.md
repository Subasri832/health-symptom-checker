# 🏥 HealthAI — AI-Powered Symptom Checker & Doctor Finder

An intelligent healthcare web application that analyzes patient symptoms 
using AI, detects severity levels, and connects users with the right 
doctors — available in both English and Tamil.

🔗 **Live Demo:** https://health-symptom-checker-t6mo.onrender.com

---

## ✨ Features

- 🧠 **AI Symptom Analysis** — Describe symptoms in natural language, get 
  instant AI-powered diagnosis using Groq's LLaMA 3.3 70B model
- 🌡️ **Severity Detection** — Automatically classifies conditions as 
  Mild, Moderate, or Serious with color-coded alerts
- 🗣️ **Multilingual Support** — Full support for English and Tamil — 
  type and receive responses in your preferred language
- 💬 **Conversational AI** — AI asks follow-up questions like a real 
  doctor to better understand symptoms
- 🗺️ **Doctor Finder** — Locate nearby doctors by speciality with 
  ratings, fees, and contact details on an interactive map
- 📊 **Health History Dashboard** — Track all past symptom checks 
  with timestamps and AI analysis
- 🔐 **User Authentication** — Secure registration and login system

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Backend | Django, Django REST Framework |
| Database | PostgreSQL / SQLite |
| AI Model | Groq LLaMA 3.3 70B |
| Translation | Deep Translator |
| Frontend | HTML, CSS, JavaScript |
| Maps | Google Maps API |
| Deployment | Render.com, Gunicorn, WhiteNoise |

---

## ⚙️ How It Works

1. User describes symptoms in English or Tamil
2. Input is translated to English (if needed) for AI processing
3. Groq LLaMA 3.3 analyzes symptoms and returns structured diagnosis
4. System determines severity level and recommended specialist
5. App queries the doctor database filtered by speciality
6. Results — including nearby doctors — are translated back and displayed
7. Each check is saved to the user's health history

---

## 🚀 Running Locally

```bash
git clone https://github.com/Subasri832/health-symptom-checker.git
cd health-symptom-checker
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Create a `.env` file:
```
GROQ_API_KEY=your_groq_key_here
SECRET_KEY=your_django_secret_key
DEBUG=True
```

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

---

## ⚠️ Disclaimer

This is an educational project. AI-generated medical information is 
not a substitute for professional medical advice. Always consult a 
qualified doctor for actual health concerns.

---

## 👩‍💻 Author

Built by **Subasri** — Final year ECE student passionate about AI 
and full-stack development.

🔗 GitHub: [@Subasri832](https://github.com/Subasri832)
