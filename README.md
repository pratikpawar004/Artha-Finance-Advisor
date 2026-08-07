# Artha — AI Finance Advisor (Flask)

A personal finance tracker with login, income/expense tracking, dashboards,
and an AI advisor chat — built with Python, Flask, SQLite, and the Anthropic API.

## Features
- Sign up / log in (passwords hashed with Werkzeug, sessions via Flask-Login)
- Add income/expense entries with category, date, and notes
- Dashboard: balance card, income vs expense, savings rate, category pie chart,
  6-month trend chart, auto-generated insights
- Transaction list with filtering and delete
- AI Advisor: chat with Claude, which reads your real transaction data and
  gives personalized budgeting advice — conversation history is saved per user

## Project structure
```
artha_flask/
  app.py                 - Flask app, routes, database models
  requirements.txt
  .env.example
  templates/              - Jinja2 HTML templates
  static/style.css         - All styling
```

## Setup

1. **Create a virtual environment and install dependencies**
   ```bash
   cd artha_flask
   python -m venv venv
   source venv/bin/activate      # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Configure your Groq API key**
   ```bash
   cp .env.example .env
   ```
   Edit `.env` and paste your key from https://console.groq.com/keys
   (This step is only needed for the AI Advisor chat — everything else works without it.)

3. **Run the app**
   ```bash
   python app.py
   ```
   The database file `artha.db` is created automatically on first run.
   Open **http://127.0.0.1:5000** in your browser.

4. **Use it**
   - Sign up with a username and password
   - Add a few income/expense entries
   - Check the Dashboard for charts and insights
   - Open AI Advisor and ask things like "Suggest a monthly budget for me"

## Notes for your project report
- **Backend:** Flask (Python), SQLAlchemy ORM, SQLite database
- **Auth:** Flask-Login sessions, Werkzeug password hashing
- **Frontend:** Server-rendered Jinja2 templates, Chart.js for visualizations, vanilla JS for the chat widget
- **AI layer:** Groq API (`openai/gpt-oss-20b`, via the OpenAI-compatible client
  pointed at `https://api.groq.com/openai/v1`), given a summary of the user's
  real transactions as context before answering
- **Database models:** `User`, `Transaction`, `ChatMessage` (see `app.py`)

## Troubleshooting

**Charts not showing on the Dashboard:** the charts use Chart.js loaded from a
CDN. If your network or an ad-blocker blocks the first CDN, the page
automatically retries a second CDN — but if both are blocked (e.g. no
internet, or a very strict campus network), the chart area will show a
message telling you the library failed to load. Open the browser console
(F12 → Console) to see the exact error if this happens.

## Possible extensions (good for "future scope" in your report)
- Monthly budget limits with alerts when a category is close to the cap
- Export transactions to Excel/PDF
- Recurring transactions (rent, subscriptions)
- Multi-currency support
- Email/SMS reminders for bill due dates
