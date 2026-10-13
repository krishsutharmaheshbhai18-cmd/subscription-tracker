# AI Subscription Tracker

Track every subscription in one place, see your real monthly spend, and let
AI catch duplicate categories, unused subscriptions, and savings tips.

## Setup (same process as last time)

```bash
python -m venv venv
venv\Scripts\activate          # Mac/Linux: source venv/bin/activate
pip install -r requirements.txt
```

1. Rename `.env.example` to `.env`
2. Open it in Notepad, paste your key from https://aistudio.google.com/apikey
   after `GEMINI_API_KEY=` (same key from last project works fine)
3. Save

## Run it

```bash
streamlit run app.py
```

## How to use it

1. Sidebar se subscription add karo: name, price, monthly/yearly, category, renewal date
2. Dashboard mein turant dikh jayega total monthly spend
3. "Analyze my subscriptions" button dabao — AI batayega:
   - Duplicate categories (do streaming apps ek saath)
   - 30+ din se unused subscriptions
   - Savings tips (yearly plan, consolidate, etc.)
4. "Used today" button dabao jab bhi us subscription ko use karo — isse
   "unused" tracking accurate rehti hai
5. "Delete" se subscription hata sakte ho

## How it's built (for learning)

| File | What it teaches |
|---|---|
| `db.py` | SQLite — a real database, not just a list in memory. CRUD operations. |
| `insights.py` | Giving an LLM **structured data** (not free text) and asking for **structured JSON back** — this is how real AI features work, not just chat |
| `app.py` | Streamlit forms, columns, buttons with unique keys, session state via rerun |

## Learning exercises

1. Add an "edit subscription" feature (currently you can only add/delete).
2. Add a pie chart of spend by category (use `st.bar_chart` or `plotly`).
3. Add email reminders using a free service like SendGrid (advanced).
4. Export subscriptions to CSV with `st.download_button`.
5. Add user login so multiple people can use the same deployed app
   (their own subscriptions only) — look into `streamlit-authenticator`.
6. Deploy on Streamlit Community Cloud, add `GEMINI_API_KEY` in Secrets,
   and share the link with friends/family. Real usage is the strongest
   resume line you can get from this project.
