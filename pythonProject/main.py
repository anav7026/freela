from flask import Flask, jsonify, render_template, request, redirect, url_for, session, flash
from BankingSystem import BankingSystem
from UserDatabase import UserDatabase
from User import User
from TaxDocument import TaxDocument
from TaxDocumentDatabase import TaxDocumentDatabase
from Transaction import Transaction
from TransactionDatabase import TransactionDatabase

from Database import Database #this is prostgres database
import os
import psycopg2


app = Flask(__name__)
app.secret_key = os.urandom(24)  # Add a secret key for sessions

# Initialize databases
#tax_doc_db = TaxDocumentDatabase()
#user_db = UserDatabase()
#banking_system = BankingSystem(user_db)

#DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://myuser:mypassword@localhost:5432/mydatabase")



# Load all databases
# Load users, transactions, and tax documents from PostgreSQL
# database = Database()
# database.load_all_databases()
# Load users and transactions from the database
postgres_database = Database()
postgres_database.load_all_databases()


"""Testing : Are Users loading correctly? YES """
@app.route('/users')
def get_users():
    return postgres_database.user_database.list_users()
    
"""Testing : Are Transactions loading correctly? YES """
@app.route('/transactions')
def get_transactions():
    """Route that retrieves all transactions from the database"""
    return postgres_database.transaction_database.print_transactions()

"""PROGRAM STARTS HERE"""

@app.route('/')
def landingpage():
    """Route for the landing page"""
    return render_template('landing.html')
    
    
"""Login Page 
    Working : Yes 
    Description : This page allows the user to login to their account. 
                    If successful, it redirects to the welcome page.
"""
@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if postgres_database.user_database.authenticate(username, password):
            session['username'] = username  # Store username in session
            return redirect(url_for('welcome', username=username))
        else:
            flash("Failed Login: Try Again")
            return render_template('login.html')
        
    return render_template('login.html')
"""
    Welcome Page
    Working : Yes [Page opens and shows the user their information]
    ERROR: WHEN USER CLICKS CARD BUTTON,ERROR APPEARS
    Description : This page is the main page for the user.
"""
@app.route("/welcome/<username>") 
def welcome(username):
    user = postgres_database.user_database.find_user(username) #WORKS :)
    if user:
        spendable_income = user.get_spendable_balance()
        tax_savings = user.get_savings_income()
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
        
        if postgres_database.user_database.find_user(username) is None:
            print(f"Received: {username}, {password}")
            if postgres_database.user_database.add_user(username, password):
                session['username'] = username  # Store username in session
                return redirect(url_for('welcome', username=username))
        
        flash(f"Username: {username} is already taken. Try again!")
        
    return render_template('signup.html')



@app.route("/logout")
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route("/welcome/<username>/card")
def card(username):
    user = postgres_database.user_database.find_user(username)
    if user:
        total = user.get_total() 
        spendable_income = user.get_spendable_balance()
        tax_savings = user.get_savings_income()
        transactions = postgres_database.transaction_database.get_transaction_by_id(user.get_user_id()) 
        print(transactions)
        return render_template('card.html', username=username, total=total, 
                              spendable_income=spendable_income, tax_savings=tax_savings, transactions=transactions)
    return "Error: User not found", 404

@app.route("/welcome/<username>/deposit", methods=["GET", "POST"])
def deposit(username):
    user = postgres_database.user_database.find_user(username)
    if not user:
        return "Error: User not found", 404

    if request.method == "POST":
        try:
            amount = float(request.form.get("deposit_amount"))
            if amount <= 0:
                flash("Invalid deposit amount!")
                return render_template('deposit.html', username=username)

            if postgres_database.banking_system.deposit(username, amount):
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
    user = postgres_database.user_database.find_user(username)
    if not user:
        return "Error: User not found", 404

    if request.method == "POST":
        try:
            amount = float(request.form.get("withdraw_amount"))
            if amount <= 0:
                flash("Invalid withdrawal amount!")
                return render_template('withdraw.html', username=username)

            if postgres_database.banking_system.withdraw(username, amount):
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
    user = postgres_database.user_database.find_user(username)
    if not user:
        return "Error: User not found", 404

    if request.method == "POST":
        try:
            amount = float(request.form.get("transfer_amount"))
            receiver = request.form.get("receiver_username")
            
            if amount <= 0:
                flash("Invalid transfer amount!")
                return render_template('transfer.html', username=username)

            if postgres_database.banking_system.transfer(username, receiver, amount):
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
    doc_dictionary = postgres_database.tax_document_database.global_doc_dictionary  # Access the global dictionary with all documents
    return render_template('taxdoc.html', username=username, doc_dictionary=doc_dictionary)


if __name__ == "__main__":
    app.run(debug=True, port=5001)
