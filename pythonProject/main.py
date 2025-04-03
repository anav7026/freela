from flask import Flask, jsonify, render_template, request, redirect, url_for, session, flash
from BankingSystem import BankingSystem
from UserDatabase import UserDatabase
from User import User
from TaxDocument import TaxDocument
from TaxDocumentDatabase import TaxDocumentDatabase
import os
import psycopg2

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Add a secret key for sessions

# Initialize databases
tax_doc_db = TaxDocumentDatabase()
user_db = UserDatabase()
banking_system = BankingSystem(user_db)

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://myuser:mypassword@localhost:5432/mydatabase")

def get_db_connection():
    #Create and return a connection to the PostgreSQL database
    conn = psycopg2.connect(DATABASE_URL)
    return conn

@app.route('/')
def index():
    """Route that queries the database and returns the result"""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT 'Hello from PostgreSQL!'")
    message = cur.fetchone()[0]  # Get the result from the query
    cur.close()
    conn.close()
    return message

@app.route('/users')
def get_users():
    """Route that retrieves all users from the database"""
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Replace with your actual table name and fields
    cur.execute("SELECT id, username FROM users")
    users = cur.fetchall()  # Fetch all users
    
    # Clean up
    cur.close()
    conn.close()
    
    # Return the users as JSON
    return jsonify(users)

@app.route('/transactions')
def get_transactions():
    """Route that retrieves all users from the database"""
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Replace with your actual table name and fields
    cur.execute("SELECT id, timestamp, transaction_type, amount, sender, receiver FROM transactions")
    transactions = cur.fetchall()  # Fetch all transactions
    
    # Clean up
    cur.close()
    conn.close()
    
    # Return the transactions as JSON
    return jsonify(transactions)

@app.route("/home")
def homepage():
    return render_template('home.html')

@app.route("/welcome/<username>")
def welcome(username):
    user = user_db.find_user(username)
    if user:
        spendable_income = user.spendable_income
        tax_savings = user.tax_savings
        total = user.total
    else:
        spendable_income = 0
        tax_savings = 0
        total = 0
    return render_template('home.html', username=username, spendable_income=spendable_income, 
                           tax_savings=tax_savings, total=total)

@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if user_db.find_user(username) is None:
            print(f"Received: {username}, {password}")
            if user_db.add_user(username, password):
                session['username'] = username  # Store username in session
                return redirect(url_for('welcome', username=username))
        
        flash(f"Username: {username} is already taken. Try again!")
        
    return render_template('signup.html')

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if user_db.authenticate(username, password):
            session['username'] = username  # Store username in session
            return redirect(url_for('welcome', username=username))
        else:
            flash("Failed Login: Try Again")
            return render_template('login.html')
        
    return render_template('login.html')

@app.route("/logout")
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route("/welcome/<username>/card")
def card(username):
    user = user_db.find_user(username)
    if user:
        total = user.total
        spendable_income = user.spendable_income
        tax_savings = user.tax_savings
        transactions = banking_system.get_user_transactions(username)
        return render_template('card.html', username=username, total=total, 
                              spendable_income=spendable_income, tax_savings=tax_savings, transactions=transactions)
    return "Error: User not found", 404

@app.route("/welcome/<username>/deposit", methods=["GET", "POST"])
def deposit(username):
    user = user_db.find_user(username)
    if not user:
        return "Error: User not found", 404

    if request.method == "POST":
        try:
            amount = float(request.form.get("deposit_amount"))
            if amount <= 0:
                flash("Invalid deposit amount!")
                return render_template('deposit.html', username=username)

            if banking_system.deposit(username, amount):
                flash(f"Successfully deposited ${amount:.2f}!")
                return redirect(url_for("welcome", username=username))
            else:
                flash("Deposit failed!")
                return render_template('deposit.html', username=username)
        except ValueError:
            flash("Invalid input! Please enter a numeric value.")
            return render_template('deposit.html', username=username)

    return render_template('deposit.html', username=username)

@app.route("/welcome/<username>/withdraw", methods=["GET", "POST"])
def withdraw(username):
    user = user_db.find_user(username)
    if not user:
        return "Error: User not found", 404

    if request.method == "POST":
        try:
            amount = float(request.form.get("withdraw_amount"))
            if amount <= 0:
                flash("Invalid withdrawal amount!")
                return render_template('withdraw.html', username=username)

            if banking_system.withdraw(username, amount):
                flash(f"Successfully withdrew ${amount:.2f}!")
                return redirect(url_for("welcome", username=username))
            else:
                flash("Withdrawal failed! Insufficient funds or invalid amount.")
                return render_template('withdraw.html', username=username)
        except ValueError:
            flash("Invalid input! Please enter a numeric value.")
            return render_template('withdraw.html', username=username)

    return render_template('withdraw.html', username=username)

@app.route("/welcome/<username>/transfer", methods=["GET", "POST"])
def transfer(username):
    user = user_db.find_user(username)
    if not user:
        return "Error: User not found", 404

    if request.method == "POST":
        try:
            amount = float(request.form.get("transfer_amount"))
            receiver = request.form.get("receiver_username")
            
            if amount <= 0:
                flash("Invalid transfer amount!")
                return render_template('transfer.html', username=username)

            if banking_system.transfer(username, receiver, amount):
                flash(f"Successfully transferred ${amount:.2f} to {receiver}!")
                return redirect(url_for("welcome", username=username))
            else:
                flash("Transfer failed! Check recipient username and available funds.")
                return render_template('transfer.html', username=username)
        except ValueError:
            flash("Invalid input! Please enter a numeric value.")
            return render_template('transfer.html', username=username)

    return render_template('transfer.html', username=username)

@app.route("/welcome/<username>/taxDoc")
def taxdoc(username):
    # Access the tax documents from the database
    doc_dictionary = tax_doc_db.global_doc_dictionary  # Access the global dictionary with all documents
    return render_template('taxdoc.html', username=username, doc_dictionary=doc_dictionary)


if __name__ == "__main__":
    app.run(debug=True, port=5001)
