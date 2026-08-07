# 💰 Artha – AI Personal Finance Advisor

Artha is an AI-powered Personal Finance Advisor built using **Flask** and **Google Gemini AI**. It helps users track their income and expenses, visualize financial data, and receive personalized budgeting and savings advice based on their real financial records.

---

## 📌 Features

### 🔐 User Authentication
<img width="1053" height="768" alt="image" src="https://github.com/user-attachments/assets/0e8c2dd3-3140-4f36-9556-e45920d600da" />
- Secure user registration and login
- Password hashing using Werkzeug
- Session management with Flask-Login

### 💵 Income & Expense Management
<img width="1257" height="896" alt="image" src="https://github.com/user-attachments/assets/71d6780f-541f-41af-9ee4-e278ff79ecf5" />
- Add income and expense transactions
- Categorize expenses
- Add transaction notes
- Store transaction date
- Delete transactions

### 📊 Dashboard
<img width="1895" height="902" alt="Image" src="https://github.com/user-attachments/assets/099ae070-7747-4749-a7b4-ddf7af79c9bf" />
- Total Income
- Total Expenses
- Remaining Balance
- Savings Rate
- Expense Category Pie Chart
- Monthly Spending Trend
- Automatic Financial Insights

### 🤖 AI Finance Advisor
<img width="1352" height="889" alt="Image" src="https://github.com/user-attachments/assets/bc6db8ba-d6fb-4d74-9787-909ae44c41a6" />
- Powered by **Google Gemini AI**
- Uses your real financial data before answering
- Personalized budgeting advice
- Spending analysis
- Savings recommendations
- Context-aware conversation
- Chat history stored for every user

### 📋 Transaction History
<img width="1801" height="896" alt="Image" src="https://github.com/user-attachments/assets/84732b38-8251-4d1b-b7e8-3b6718b4960f" />
- View all transactions
- Filter transactions
- Delete unwanted entries

---

# 🖼 Application Pages

## 🏠 Dashboard
Displays complete financial summary with charts and insights.

## 💳 Transactions
View and manage all income and expense records.

## ➕ Add Entry
Add a new income or expense transaction.

## 🤖 AI Advisor
Chat with Artha AI and receive personalized financial advice.

---

# 🛠 Tech Stack

## Backend
- Python
- Flask
- SQLAlchemy
- SQLite

## Frontend
- HTML5
- CSS3
- JavaScript
- Jinja2 Templates
- Chart.js

## Authentication
- Flask-Login
- Werkzeug

## AI Integration
- Google Gemini AI
- google-genai SDK

---

# 📂 Project Structure

```text
artha_flask/
│
├── app.py
├── requirements.txt
├── README.md
│
├── static/
│   └── style.css
│
├── templates/
│   ├── base.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── transactions.html
│   ├── add_entry.html
│   └── advisor.html
│
└── instance/
    └── artha.db
```

---

# 🚀 Installation

## 1️⃣ Clone Repository

```bash
git clone https://github.com/pratikpawar004/Artha-Finance-Advisor.git

cd Artha-Finance-Advisor
```

---

## 2️⃣ Create Virtual Environment

### Windows

```bash
python -m venv venv

venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv

source venv/bin/activate
```

---

## 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4️⃣ Add Your Google Gemini API Key

Before running the project, open the `app.py` file.

Find the following code:

```python
client = genai.Client(
    api_key="your_google_genai_api_key_here"
)
```

Replace `your_google_genai_api_key_here` with your own Google Gemini API key.

### 🔑 How to Get a Gemini API Key

1. Visit Google AI Studio:
   https://aistudio.google.com/app/apikey

2. Sign in with your Google account.

3. Click **Create API Key**.

4. Copy the generated API key.

5. Paste it into `app.py`:

```python
client = genai.Client(
    api_key="YOUR_GEMINI_API_KEY"
)
```

> **Important:** Do not upload your real API key to GitHub. Before pushing your project, replace it with:
>
> ```python
> api_key="your_google_genai_api_key_here"
> ```

## ⚠️ Important

This repository does not include a Gemini API key.

To use the AI Advisor, you must:

- Create your own Gemini API key from Google AI Studio.
- Add the key manually in `app.py`.
- Never commit your real API key to GitHub.

---

## 5️⃣ Run the Application

```bash
python app.py
```

---

## 6️⃣ Open Browser

```
http://127.0.0.1:5000
```

---

# 📦 Requirements

```text
Flask==3.0.3
Flask-SQLAlchemy==3.1.1
Flask-Login==0.6.3
Werkzeug==3.0.3
python-dotenv==1.0.1
google-genai==1.34.0
```

---

# 💬 Example AI Questions

- Am I overspending anywhere?
- Suggest a monthly budget.
- How can I save more money?
- Which category should I reduce?
- Can I reach my savings goal?
- Analyze my monthly expenses.

---

# 🎯 Future Scope

- Monthly Budget Goals
- Budget Alerts
- Export to Excel/PDF
- Recurring Transactions
- Email Notifications
- Mobile Responsive UI
- AI Financial Report Generation
- Investment Suggestions
- Bill Reminder System
- Dark Mode
- Multiple Currency Support

---

# 👨‍💻 Author

**Pratik Pawar**

🎓 Bachelor of Technology (B.Tech) – Computer Engineering

🏛️ Dr. Babasaheb Ambedkar Technological University (DBATU)

📍 Maharashtra, India

---

# ⭐ If you like this project

Please give this repository a **Star ⭐**
