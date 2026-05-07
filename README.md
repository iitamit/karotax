# KaroTax — SMART ITR FILLING SYSTEM AND AI CHARTERED ACCOUNTANT 🇮🇳

> Free ITR filing + AI CA chat + Financial planning for every Indian

## Features
- ✅ ITR Filing Wizard (ITR-1 to ITR-4) — 10 minutes mein
- ✅ Old vs New Regime auto-comparison by AI
- ✅ AI CA Chat (Gemini 2.5 Flash, free — Hindi/English both)
- ✅ Financial Planner (goal-based investment recommendations)
- ✅ 80C/80D deduction calculator
- ✅ Indian tax calculator (FY 2024-25)
- ✅ Groq fallback when Gemini hits rate limits

## Tech Stack
- **Backend**: Python Django 4.2 + PostgreSQL
- **Frontend**: HTML5 + Tailwind CSS
- **AI**: Google Gemini 2.5 Flash (free, 1500 req/day) → Groq Llama (fallback)

## Setup

### 1. Clone & Install
```bash
pip install -r requirements.txt
```

### 2. Environment Variables
```bash
cp .env.example .env
# Edit .env with your API keys
```

### 3. Get Free API Keys
- **Gemini**: https://aistudio.google.com → Get API Key (free, no card)
- **Groq**: https://console.groq.com → Create key (free, no card)

### 4. Run
```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open http://localhost:8000

## Project Structure
```
KaroTax/          — Django project settings & urls
accounts/         — User auth, profile, PAN/Aadhaar
itr/              — ITR wizard (5 steps), tax calculator
ai_ca/            — AI CA chat (Gemini + Groq)
financial/        — Financial planner, investment recs
dashboard/        — Home dashboard, landing page
templates/        — All HTML templates
```

## Database (PostgreSQL for production)
```sql
CREATE DATABASE KaroTax_db;
CREATE USER KaroTax_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE KaroTax_db TO KaroTax_user;
```
Then set USE_SQLITE=False in .env.

## Roadmap
- [ ] e-Filing API integration (income tax portal)
- [ ] Form 26AS auto-import
- [ ] GST filing module
- [ ] PDF ITR download
- [ ] SMS OTP login
- [ ] Multi-language (Odia, Bengali, Tamil)
