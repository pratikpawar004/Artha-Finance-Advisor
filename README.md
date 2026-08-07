# 💰 Artha – AI Personal Finance Advisor

Artha is an AI-powered Personal Finance Advisor built using **Flask** and **Google Gemini AI**. It helps users track their income and expenses, visualize financial data, and receive personalized budgeting and savings advice based on their real financial records.

---

## 📌 Features

### 🔐 User Authentication
- Secure user registration and login
- Password hashing using Werkzeug
- Session management with Flask-Login

### 💵 Income & Expense Management
- Add income and expense transactions
- Categorize expenses
- Add transaction notes
- Store transaction date
- Delete transactions

### 📊 Dashboard
- Total Income
- Total Expenses
- Remaining Balance
- Savings Rate
- Expense Category Pie Chart
- Monthly Spending Trend
- Automatic Financial Insights

### 🤖 AI Finance Advisor
- Powered by **Google Gemini AI**
- Uses your real financial data before answering
- Personalized budgeting advice
- Spending analysis
- Savings recommendations
- Context-aware conversation
- Chat history stored for every user

### 📋 Transaction History
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
├── .env.example
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

## 4️⃣ Create .env File

Create a `.env` file in the project root.

```env
SECRET_KEY=your_secret_key

GEMINI_API_KEY=your_gemini_api_key
```

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

B.Tech Computer Engineering

Dr. Babasaheb Ambedkar Technological University

---

# ⭐ If you like this project

Please give this repository a **Star ⭐**
