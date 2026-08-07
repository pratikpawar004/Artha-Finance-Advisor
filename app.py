import os
import json
from google import genai
from dotenv import load_dotenv
import os

load_dotenv()
from datetime import datetime
from collections import defaultdict

from flask import Flask, render_template, redirect, url_for, request, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import (
    LoginManager, UserMixin, login_user, logout_user,
    login_required, current_user
)
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-me')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///artha.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please log in to continue.'

EXPENSE_CATEGORIES = ['Food', 'Transport', 'Rent', 'Utilities', 'Education',
                       'Entertainment', 'Shopping', 'Health', 'Other']
INCOME_CATEGORIES = ['Pocket Money', 'Salary', 'Freelance', 'Scholarship', 'Gift', 'Other']


# ---------------- Models ----------------

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    transactions = db.relationship('Transaction', backref='user', lazy=True,
                                    cascade='all, delete-orphan')
    messages = db.relationship('ChatMessage', backref='user', lazy=True,
                                cascade='all, delete-orphan')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    type = db.Column(db.String(10), nullable=False)  # 'income' or 'expense'
    category = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.String(10), nullable=False)  # YYYY-MM-DD
    note = db.Column(db.String(255), default='')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class ChatMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    role = db.Column(db.String(10), nullable=False)  # 'user' or 'assistant'
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# ---------------- Helpers ----------------

def fmt_inr(n):
    try:
        n = float(n)
    except (TypeError, ValueError):
        n = 0
    return '₹{:,.0f}'.format(n)


app.jinja_env.filters['inr'] = fmt_inr


def build_financial_summary(user):
    txns = Transaction.query.filter_by(user_id=user.id).all()
    income = sum(t.amount for t in txns if t.type == 'income')
    expense = sum(t.amount for t in txns if t.type == 'expense')
    by_cat = defaultdict(float)
    for t in txns:
        if t.type == 'expense':
            by_cat[t.category] += t.amount
    cat_lines = '\n'.join(f'- {c}: ₹{v:,.0f}' for c, v in sorted(by_cat.items(), key=lambda x: -x[1]))
    return (
        f"Total income: ₹{income:,.0f}\n"
        f"Total expenses: ₹{expense:,.0f}\n"
        f"Balance: ₹{income - expense:,.0f}\n"
        f"Expense breakdown:\n{cat_lines or 'No expenses logged yet.'}\n"
        f"Number of transactions logged: {len(txns)}"
    )


# ---------------- Auth routes ----------------

@app.route('/')
def index():
    return redirect(url_for('dashboard') if current_user.is_authenticated else url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        if not username or not password:
            flash('Please fill in both fields.', 'error')
            return render_template('register.html')
        if User.query.filter_by(username=username).first():
            flash('That username is already taken. Try logging in instead.', 'error')
            return render_template('register.html')
        user = User(username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for('dashboard'))
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        user = User.query.filter_by(username=username).first()
        if not user or not user.check_password(password):
            flash('Username or password is incorrect.', 'error')
            return render_template('login.html')
        login_user(user)
        return redirect(url_for('dashboard'))
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


# ---------------- App routes ----------------

@app.route('/dashboard')
@login_required
def dashboard():
    txns = Transaction.query.filter_by(user_id=current_user.id).all()
    income = sum(t.amount for t in txns if t.type == 'income')
    expense = sum(t.amount for t in txns if t.type == 'expense')
    balance = income - expense
    savings_rate = round(((income - expense) / income) * 100) if income > 0 else 0

    by_cat = defaultdict(float)
    for t in txns:
        if t.type == 'expense':
            by_cat[t.category] += t.amount
    cat_labels = list(by_cat.keys())
    cat_values = list(by_cat.values())

    monthly = defaultdict(lambda: {'income': 0, 'expense': 0})
    for t in txns:
        key = t.date[:7]
        monthly[key][t.type] += t.amount
    month_keys = sorted(monthly.keys())[-6:]
    month_income = [monthly[m]['income'] for m in month_keys]
    month_expense = [monthly[m]['expense'] for m in month_keys]

    insights = []
    if not txns:
        insights.append("No entries yet — add your first income or expense to see insights here.")
    else:
        if expense > income:
            insights.append(f"You've spent {fmt_inr(expense - income)} more than you earned this period. "
                             f"Consider trimming discretionary categories.")
        if cat_labels:
            top_cat = max(by_cat.items(), key=lambda x: x[1])
            pct = round((top_cat[1] / expense) * 100) if expense else 0
            insights.append(f"{top_cat[0]} is your biggest expense category at {fmt_inr(top_cat[1])} ({pct}% of spending).")
        if income > 0:
            tip = "That's a healthy buffer — keep it up." if savings_rate >= 20 else \
                  "Financial advisors often suggest aiming for at least 20%."
            insights.append(f"Your savings rate is {savings_rate}%. {tip}")

    return render_template(
        'dashboard.html',
        income=income, expense=expense, balance=balance, savings_rate=savings_rate,
        cat_labels=json.dumps(cat_labels), cat_values=json.dumps(cat_values),
        month_keys=json.dumps(month_keys), month_income=json.dumps(month_income),
        month_expense=json.dumps(month_expense), insights=insights,
    )


@app.route('/transactions')
@login_required
def transactions():
    filter_type = request.args.get('type', 'all')
    query = Transaction.query.filter_by(user_id=current_user.id)
    if filter_type in ('income', 'expense'):
        query = query.filter_by(type=filter_type)
    txns = query.order_by(Transaction.date.desc()).all()
    return render_template('transactions.html', txns=txns, filter_type=filter_type)


@app.route('/transactions/add', methods=['GET', 'POST'])
@login_required
def add_transaction():
    if request.method == 'POST':
        t_type = request.form.get('type', 'expense')
        category = request.form.get('category', 'Other')
        amount = request.form.get('amount', '0')
        date = request.form.get('date') or datetime.utcnow().strftime('%Y-%m-%d')
        note = request.form.get('note', '').strip()
        try:
            amount = float(amount)
        except ValueError:
            amount = 0
        if amount <= 0:
            flash('Please enter a valid amount.', 'error')
            return render_template('add_entry.html',
                                    expense_categories=EXPENSE_CATEGORIES,
                                    income_categories=INCOME_CATEGORIES)
        txn = Transaction(user_id=current_user.id, type=t_type, category=category,
                           amount=amount, date=date, note=note)
        db.session.add(txn)
        db.session.commit()
        flash('Entry saved.', 'success')
        return redirect(url_for('transactions'))
    return render_template('add_entry.html',
                            expense_categories=EXPENSE_CATEGORIES,
                            income_categories=INCOME_CATEGORIES)


@app.route('/transactions/delete/<int:txn_id>', methods=['POST'])
@login_required
def delete_transaction(txn_id):
    txn = Transaction.query.filter_by(id=txn_id, user_id=current_user.id).first()
    if txn:
        db.session.delete(txn)
        db.session.commit()
    return redirect(url_for('transactions'))


@app.route('/advisor')
@login_required
def advisor():
    history = ChatMessage.query.filter_by(user_id=current_user.id).order_by(ChatMessage.created_at).all()
    return render_template('advisor.html', history=history)


@app.route('/advisor/ask', methods=['POST'])
@login_required
def advisor_ask():

    question = (request.json or {}).get('question', '').strip()

    if not question:
        return jsonify({'error': 'Please type a question.'}), 400

    # Save user message
    user_msg = ChatMessage(
        user_id=current_user.id,
        role='user',
        content=question
    )

    db.session.add(user_msg)
    db.session.commit()

    try:
        from google import genai
        import os

        client = genai.Client(
            api_key="your_google_genai_api_key_here"  # Replace with your actual API key
        )

        history = (
            ChatMessage.query
            .filter_by(user_id=current_user.id)
            .order_by(ChatMessage.created_at)
            .all()
        )

        system_prompt = f"""
You are Artha, an intelligent personal finance advisor.

You help students and young professionals manage their money.

Rules:
- Give practical advice.
- Use the user's financial data.
- Answer in simple English.
- Keep responses short.
- Use bullet points whenever useful.
- Suggest savings and budgeting tips.
- Mention overspending if applicable.
- Be friendly and encouraging.
- Always use Indian Rupees (₹).
- If the user asks about saving money, suggest realistic ways based on their expenses.
- If spending is higher than income, clearly point it out and suggest improvements.

User Financial Summary:

{build_financial_summary(current_user)}

Conversation:
"""

        prompt = system_prompt

        for msg in history:
            if msg.role == "user":
                prompt += f"\nUser: {msg.content}"
            else:
                prompt += f"\nAssistant: {msg.content}"

        prompt += f"\nUser: {question}\nAssistant:"

        response = client.models.generate_content(
            model="gemini-3.6-flash",   # <-- Updated model
            contents=prompt
        )

        answer = response.text.strip()

        if not answer:
            answer = "Sorry, I couldn't generate a response."

    except Exception as e:
        answer = (
            "Sorry, I couldn't reach Gemini AI.\n\n"
            f"Error: {e}"
        )

    bot_msg = ChatMessage(
        user_id=current_user.id,
        role='assistant',
        content=answer
    )

    db.session.add(bot_msg)
    db.session.commit()

    return jsonify({
        'answer': answer
    })


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
