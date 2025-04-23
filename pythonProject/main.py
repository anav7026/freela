from flask import Flask, jsonify, render_template, request, redirect, url_for, session, flash
from BankingSystem import BankingSystem
from UserDatabase import UserDatabase
from User import User
from TaxDocument import TaxDocument
from TaxDocumentDatabase import TaxDocumentDatabase
from Transaction import Transaction
from TransactionDatabase import TransactionDatabase
from Database import Database
import os
import psycopg2

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Add a secret key for sessions

# Initialize the database connection
postgres_database = Database()
postgres_database.load_all_databases()





@app.route('/users')
def get_users():
    """Route that retrieves all users from the database"""
    return postgres_database.user_database.list_users()
    
@app.route('/transactions')
def get_transactions():
    """Route that retrieves all transactions from the database"""
    return postgres_database.transaction_database.print_transactions()

@app.route('/')
def landingpage():
    """Route for the landing page"""
    return render_template('landing.html')
    
@app.route("/login", methods=['GET', 'POST'])
def login():
    """Handle user login"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if postgres_database.user_database.authenticate(username, password):
            session['username'] = username  # Store username in session
            return redirect(url_for('welcome', username=username))
        else:
            flash("Failed Login: Try Again")
    
    return render_template('login.html')

@app.route("/welcome/<username>") 
def welcome(username):
    """Welcome page with user information"""
    user = postgres_database.user_database.find_user(username)
    if user:
        spendable_income = postgres_database.banking_system.get_spendable_balance(username)
        tax_savings = postgres_database.banking_system.get_savings_income(username)
        total = user.get_total()
    else:
        spendable_income = 0
        tax_savings = 0
        total = 0
    
    return render_template('home.html', username=username, spendable_income=spendable_income, 
                           tax_savings=tax_savings, total=total)

@app.route("/signup", methods=['GET', 'POST'])
def signup():
    """Handle user signup"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if postgres_database.user_database.find_user(username) is None:
            new_user_id = len(postgres_database.user_database.users) + 1
            user = User(new_user_id, username, password, 0, 0.20)
            
            if postgres_database.user_database.add_user(new_user_id, username, password, 0, 0.20):
                session['username'] = username  # Store username in session
                postgres_database.insert_new_user(user)
                return redirect(url_for('welcome', username=username))
        
        flash(f"Username: {username} is already taken. Try again!")
        
    return render_template('signup.html')

@app.route("/logout")
def logout():
    """Handle user logout"""
    session.pop('username', None)
    return redirect(url_for('landingpage'))

@app.route("/welcome/<username>/card")
def card(username):
    """Show user card with transaction history"""
    user = postgres_database.user_database.find_user(username)
    if user:
        total = user.get_total() 
        spendable_income = postgres_database.banking_system.get_spendable_balance(username)
        tax_savings = postgres_database.banking_system.get_savings_income(username)
        transactions = postgres_database.banking_system.show_transaction_history(username)
        
        return render_template('card.html', username=username, total=total, 
                              spendable_income=spendable_income, tax_savings=tax_savings, transactions=transactions)
    
    return "Error: User not found", 404

@app.route("/welcome/<username>/deposit", methods=["GET", "POST"])
def deposit(username):
    """Handle deposit operation"""
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
                # Update user balance in database
                postgres_database.update_user_balance(user)
                postgres_database.insert_all_transactions()
                flash(f"Successfully deposited ${amount:.2f}!")
                return redirect(url_for("welcome", username=username))
            else:
                flash("Deposit failed!")
        except ValueError:
            flash("Invalid input! Please enter a numeric value.")
    
    return render_template('deposit.html', username=username)

@app.route("/welcome/<username>/withdraw", methods=["GET", "POST"])
def withdraw(username):
    """Handle withdrawal operation"""
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
                # Update user balance in database
                postgres_database.update_user_balance(user)
                postgres_database.insert_all_transactions()
                flash(f"Successfully withdrew ${amount:.2f}!")
                return redirect(url_for("welcome", username=username))
            else:
                flash("Withdrawal failed! Insufficient funds or invalid amount.")
        except ValueError:
            flash("Invalid input! Please enter a numeric value.")
    
    return render_template('withdraw.html', username=username)

@app.route("/welcome/<username>/transfer", methods=["GET", "POST"])
def transfer(username):
    """Handle transfer operation"""
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

            receiver_user = postgres_database.user_database.find_user(receiver)
            if not receiver_user:
                flash(f"User '{receiver}' not found!")
                return render_template('transfer.html', username=username)

            if postgres_database.banking_system.transfer(username, receiver, amount):
                # Update user balances in database
                postgres_database.update_user_balance(user)
                postgres_database.update_user_balance(receiver_user)
                postgres_database.insert_all_transactions()
                flash(f"Successfully transferred ${amount:.2f} to {receiver}!")
                return redirect(url_for("welcome", username=username))
            else:
                flash("Transfer failed! Check recipient username and available funds.")
        except ValueError:
            flash("Invalid input! Please enter a numeric value.")
    
    return render_template('transfer.html', username=username)
@app.route("/welcome/<username>/tax_savings", methods=["GET", "POST"])
def tax_savings(username):
    """Show tax savings"""
    user = postgres_database.user_database.find_user(username)
    current_tax_rate = user.saving_rate_preference
    current_tax_savings = postgres_database.banking_system.get_savings_income(username)
    
    if user:
        if request.method == "POST": 
            updated_tax_rate=float(request.form.get("tax_rate"))
            if updated_tax_rate:
                # Update the user's tax rate in the database
                user.saving_rate_preference = float(updated_tax_rate)
                postgres_database.update_user_balance(user)
                postgres_database.insert_all_transactions()
            #flash(f"Successfully updated tax rate to {updated_tax_rate}!")
            
                return redirect(url_for("welcome", username=username))
            #tax_savings = postgres_database.banking_system.get_savings_income(username)
            
    
    return render_template('tax_savings.html', username=username,current_tax_savings=current_tax_savings, current_tax_rate=current_tax_rate)
    
@app.route("/welcome/<username>/taxDoc")
def taxdoc(username):
    """Show tax documents"""
    doc_dictionary = postgres_database.tax_document_database.global_doc_dictionary
    return render_template('taxdoc.html', username=username, doc_dictionary=doc_dictionary)

if __name__ == "__main__":
    app.run(debug=True, port=5000)