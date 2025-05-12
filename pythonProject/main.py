from flask import Flask, jsonify, render_template, request, redirect, url_for, session, flash
from BankingSystem import BankingSystem
from UserDatabase import UserDatabase
from User import User
from TaxDocument import TaxDocument
from TaxDocumentDatabase import TaxDocumentDatabase
from Transaction import Transaction
from TransactionDatabase import TransactionDatabase
from Database import Database
from datetime import datetime,date
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
            user=postgres_database.user_database.find_user(username)
            session['username'] = username  # Store username in session

            return redirect(url_for('welcome'))
        else:
            flash("Failed Login: Try Again")
    
    return render_template('login.html')


@app.route("/welcome")
def welcome():
    """Welcome page with user information"""
    username = session.get('username')
    user = postgres_database.user_database.find_user(username)

    spendable_income = postgres_database.banking_system.get_spendable_balance(username) if user else 0
    tax_savings = postgres_database.banking_system.get_savings_income(username) if user else 0
    total = user.get_total_income() if user else 0

    # Tax document reminder logic
    """today = date.today()
    upcoming_reminders = []
    for doc in postgres_database.tax_document_database.get_all_documents():
        days_left = (doc.due_date - today).days
        if 0 <= days_left <= 60:
            upcoming_reminders.append({
                "name": doc.form_name,
                "due_date": doc.due_date.strftime("%B %d, %Y"),
                "days_left": days_left
            })"""

    return render_template('home.html', user=user, spendable_income=spendable_income,
                           tax_savings=tax_savings, total=total)

@app.route("/signup", methods=['GET', 'POST'])
def signup():
    """Handle user signup"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        street_address = request.form.get('street_address')
        apt = request.form.get('apt')
        city = request.form.get('city')
        state = request.form.get('state')
        zip_code = request.form.get('zip_code')
        ssn = request.form.get('SSN')
        email = request.form.get('email')
        role= request.form.get('role')
        
        
        if postgres_database.user_database.find_user(username) is None:
            new_user_id = len(postgres_database.user_database.users) + 1 
            user = User(new_user_id, username, password, first_name, last_name, street_address, apt, city, state, zip_code, ssn, email,role,total_income=0,tax_saving_rate=0)
            
            if postgres_database.user_database.add_user(new_user_id, username, password, first_name, last_name, street_address, apt, city, state, zip_code, ssn, email, role,total_income=0,tax_saving_rate=0):
                session['username'] = username  # Store username in session
                postgres_database.insert_new_user(user)
                return redirect(url_for('welcome'))
        
        flash(f"Username: {username} is already taken. Try again!")
        
    return render_template('signup.html')

@app.route("/logout")
def logout():
    """Handle user logout"""
    session.pop('username', None)
    return redirect(url_for('landingpage'))

@app.route("/welcome/card")
def card():
    """Show user card with transaction history"""
    username=session.get('username')
    user = postgres_database.user_database.find_user(username)
    if user:
        total = postgres_database.banking_system.get_total_income(username)
        spendable_income = postgres_database.banking_system.get_spendable_balance(username)
        tax_savings = postgres_database.banking_system.get_savings_income(username)
        transactions = postgres_database.banking_system.show_transaction_history(username)
        
        return render_template('card.html', user=user, total=total, 
                              spendable_income=spendable_income, tax_savings=tax_savings, transactions=transactions)
    
    return "Error: User not found", 404

@app.route("/welcome/deposit", methods=["GET", "POST"])
def deposit():
    """Handle deposit operation"""
    username=session.get('username')
    user = postgres_database.user_database.find_user(username)
    if not user:
        return "Error: User not found", 404

    if request.method == "POST":
        try:
            amount = float(request.form.get("deposit_amount"))
            if amount <= 0:
                flash("Invalid deposit amount!")
                return render_template('deposit.html', user=user)

            if postgres_database.banking_system.deposit(user.user_id, amount):
                # Update user balance in database
                postgres_database.update_user_balance(user)
                postgres_database.insert_all_transactions()
                flash(f"Successfully deposited ${amount:.2f}!")
                return redirect(url_for("welcome"))
            else:
                flash("Deposit failed!")
        except ValueError:
            flash("Invalid input! Please enter a numeric value.")
    
    return render_template('deposit.html')

@app.route("/welcome/withdraw", methods=["GET", "POST"])
def withdraw():
    """Handle withdrawal operation"""
    username=session.get('username')
    user = postgres_database.user_database.find_user(username)
    if not user:
        return "Error: User not found", 404

    if request.method == "POST":
        try:
            amount = float(request.form.get("withdraw_amount"))
            if amount <= 0:
                flash("Invalid withdrawal amount!")
                return render_template('withdraw.html')

            if postgres_database.banking_system.withdraw(user.user_id, amount):
                # Update user balance in database
                postgres_database.update_user_balance(user)
                postgres_database.insert_all_transactions()
                flash(f"Successfully withdrew ${amount:.2f}!")
                return redirect(url_for("welcome"))
            else:
                flash("Withdrawal failed! Insufficient funds or invalid amount.")
        except ValueError:
            flash("Invalid input! Please enter a numeric value.")
    
    return render_template('withdraw.html')

@app.route("/welcome/transfer", methods=["GET", "POST"])
def transfer():
    """Handle transfer operation"""
    username=session.get('username')
    user = postgres_database.user_database.find_user(username)
    if not user:
        return "Error: User not found", 404

    if request.method == "POST":
        try:
            amount = float(request.form.get("transfer_amount"))
            receiver_id = int(request.form.get("receiver_id"))
            
            if amount <= 0:
                flash("Invalid transfer amount!")
                return render_template('transfer.html')

            receiver_user = postgres_database.user_database.find_user_with_id(receiver_id)

            if postgres_database.banking_system.transfer(user.user_id, receiver_id, amount):
                # Update user balances in database
                postgres_database.update_user_balance(user)
                postgres_database.update_user_balance(receiver_user)
                postgres_database.insert_all_transactions()
                flash(f"Successfully transferred ${amount:.2f} to {receiver_user.user_id}!")
                return redirect(url_for("welcome"))
            else:
                flash("Transfer failed! Check recipient username and available funds.")
        except ValueError:
            flash("Invalid input! Please enter a numeric value.")
    
    return render_template('transfer.html',users=postgres_database.user_database.users)
@app.route("/welcome/tax_savings", methods=["GET", "POST"])
def tax_savings():
    """Show tax savings"""
    username=session.get('username')
    user = postgres_database.user_database.find_user(username)
    current_tax_rate = user.tax_saving_rate
    current_tax_savings = postgres_database.banking_system.get_savings_income(username)
    
    if user:
        if request.method == "POST": 
            updated_tax_rate=float(request.form.get("tax_rate"))
            if updated_tax_rate:
                # Update the user's tax rate in the database
                user.tax_saving_rate = float(updated_tax_rate)
                user.tax_saving_rate = float(updated_tax_rate)
                postgres_database.update_tax_saving_rate(user)
                postgres_database.update_user_balance(user)
                postgres_database.insert_all_transactions()
            #flash(f"Successfully updated tax rate to {updated_tax_rate}!")
            
                return redirect(url_for("welcome"))
            #tax_savings = postgres_database.banking_system.get_savings_income(username)
            
    
    return render_template('tax_savings.html', user=user,current_tax_savings=current_tax_savings, current_tax_rate=current_tax_rate)
    
@app.route("/welcome/taxDoc")
def taxdoc():
    """Show tax documents"""
    username=session.get('username')
    user=postgres_database.user_database.find_user(username)
    #doc_dictionary = postgres_database.tax_document_database.global_doc_dictionary
    doc_list = postgres_database.tax_document_database.get_all_documents()
    return render_template('taxdoc.html', user=user, doc_list=doc_list)

@app.route("/welcome/my_tax_documents")
def my_tax_documents():
    """Show user's tax documents with completion status"""
    username = session.get('username')
    user = postgres_database.user_database.find_user(username)
    
    if not user:
        flash("User not found. Please log in.")
        return redirect(url_for('login'))
    
    # Get all tax documents
    all_tax_docs = postgres_database.tax_document_database.get_all_documents()
    
    # Get user's tax document completion status
    user_tax_docs = postgres_database.user_tax_document_database.get_user_tax_documents(user.user_id)
    
    # Create a dictionary for quick lookup of completion status
    status_dict = {doc.irs_key: doc.completion_status for doc in user_tax_docs}
    
    # Create a combined list with documents and their completion status
    tax_docs_with_status = []
    for doc in all_tax_docs:
        status = status_dict.get(doc.key, "Not Started")
        due_date_status = doc.check_due_date_status()
        tax_docs_with_status.append({
            "document": doc,
            "status": status,
            "due_date_status": due_date_status
        })
    
    return render_template('my_tax_documents.html', user=user, tax_docs=tax_docs_with_status)

@app.route("/welcome/update_tax_document_status", methods=["POST"])
def update_tax_document_status():
    """Update the completion status of a tax document for the current user"""
    username = session.get('username')
    user = postgres_database.user_database.find_user(username)
    
    if not user:
        flash("User not found. Please log in.")
        return redirect(url_for('login'))
    
    irs_key = request.form.get('irs_key')
    new_status = request.form.get('status')
    
    # Check if the tax document exists
    tax_doc = postgres_database.tax_document_database.global_doc_dictionary.get(irs_key)
    if not tax_doc:
        flash("Tax document not found.")
        return redirect(url_for('my_tax_documents'))
    
    # Check if there's already a record for this user and tax document
    user_tax_doc = postgres_database.user_tax_document_database.get_user_tax_document(user.user_id, irs_key)
    
    if user_tax_doc:
        # Update existing record
        if user_tax_doc.update_status(new_status):
            postgres_database.update_user_tax_document_status(user_tax_doc)
            flash(f"Updated status for {tax_doc.form_name} to {new_status}.")
        else:
            flash(f"Invalid status: {new_status}")
    else:
        # Create new record
        user_tax_doc = postgres_database.user_tax_document_database.add_user_tax_document(user.user_id, irs_key, new_status)
        postgres_database.insert_user_tax_document(user_tax_doc)
        flash(f"Set status for {tax_doc.form_name} to {new_status}.")
    
    return redirect(url_for('my_tax_documents'))

@app.route("/welcome/tax_document_details/<irs_key>")
def tax_document_details(irs_key):
    """Show details for a specific tax document"""
    username = session.get('username')
    user = postgres_database.user_database.find_user(username)
    
    if not user:
        flash("User not found. Please log in.")
        return redirect(url_for('login'))
    
    # Get the tax document
    tax_doc = postgres_database.tax_document_database.global_doc_dictionary.get(irs_key)
    if not tax_doc:
        flash("Tax document not found.")
        return redirect(url_for('my_tax_documents'))
    
    # Get user's completion status for this document
    user_tax_doc = postgres_database.user_tax_document_database.get_user_tax_document(user.user_id, irs_key)
    status = user_tax_doc.completion_status if user_tax_doc else "Not Started"
    
    due_date_status = tax_doc.check_due_date_status()
    
    return render_template('tax_document_details.html', user=user, tax_doc=tax_doc, 
                          status=status, due_date_status=due_date_status)

####################INVOICE SYSTEM#############################
@app.route("/welcome/invoice_homepage")
def invoice_homepage():
    username=session.get('username')
    user=postgres_database.user_database.find_user(username)
    if user.role == 'freelancer':
        invoices=postgres_database.invoice_database.get_invoices_by_freelancer_id(user.user_id)
    elif user.role == 'client':
        invoices=postgres_database.invoice_database.get_invoices_by_client_id(user.user_id)
    else:
        invoices=[]
        flash (f'{user.role} is not freelancer or client')
    return render_template('invoice_homepage.html',user=user,invoices=invoices)

@app.route("/welcome/invoice_homepage/view_all_invoices")
def view_all_invoices():
    username=session.get('username')
    user=postgres_database.user_database.find_user(username)
    if user.role == 'freelancer':
        invoices=postgres_database.invoice_database.get_invoices_by_freelancer_id(user.user_id)
    elif user.role == 'client':
        invoices=postgres_database.invoice_database.get_invoices_by_client_id(user.user_id)
    else:
        invoices=[]
        flash (f'{user.role} is not freelancer or client')
    return render_template('view_all_invoices.html',user=user,invoices=invoices)

@app.route("/welcome/invoice_homepage/create", methods=["GET", "POST"])
def create_invoice():
    username = session.get('username')
    user = postgres_database.user_database.find_user(username)

    if not user:
        flash("User not found. Please log in.")
        return redirect(url_for('login'))

    clients = postgres_database.user_database.clients
    client_id = None
    invoice_date = ''
    payment_due_date = ''
    count_items = int(request.form.get('count_items', 1))

    if request.method == "POST":
        client_id = request.form.get('client_id')
        invoice_date = request.form.get('invoice_date')
        payment_due_date = request.form.get('payment_due_date')

        print(f"Creating invoice with client_id: {client_id}")  # Debugging

        if request.form.get('action') == 'add_row':
            count_items += 1  # Add one more row
        elif request.form.get('action') == 'submit_invoice':
            items = []
            for i in range(count_items):
                name = request.form.get(f'item_name_{i}')
                desc = request.form.get(f'item_description_{i}')
                qty = int(request.form.get(f'item_quantity_{i}', 1))
                price = float(request.form.get(f'item_unit_price_{i}', 0.0))
                items.append({'name': name, 'description': desc, 'quantity': qty, 'amount': price})

            invoice = postgres_database.invoice_database.add_invoice(user.user_id, client_id, invoice_date, payment_due_date)
            print(f"Created invoice with ID: {invoice.invoice_id}, client_id: {invoice.client_id}")  # Debugging

            total_amount = 0
            for item in items:
                postgres_database.invoice_database.add_item_to_invoice(invoice.invoice_id, item['name'], item['description'], item['quantity'], item['amount'])
                total_amount += item['quantity'] * item['amount']

            flash(f"Invoice created successfully! Total: ${total_amount:.2f}")
            return redirect(url_for('view_invoice', invoice_id=invoice.invoice_id))

    return render_template("create_invoice.html",
                           user=user,
                           clients=clients,
                           client_id=client_id,
                           invoice_date=invoice_date,
                           payment_due_date=payment_due_date,
                           count_items=count_items)

@app.route("/welcome/invoice_homepage/view_invoice/<int:invoice_id>")
def view_invoice(invoice_id):
    """View a specific invoice"""
    username = session.get('username')
    user = postgres_database.user_database.find_user(username)
    invoice = postgres_database.invoice_database.get_invoice_by_id(invoice_id)
    if not invoice:
        flash("Invoice not found.")
        return redirect(url_for('invoice_homepage'))

    print(f"Invoice ID: {invoice.invoice_id}, Client ID: {invoice.client_id}")  # Debugging

    freelancer = postgres_database.user_database.find_user_with_id(invoice.freelancer_id)
    client = postgres_database.user_database.find_user_with_id(invoice.client_id)

    if not client:
        print(f"Client with ID {invoice.client_id} not found.")  # Debugging
        flash("Client not found.")
        return redirect(url_for('invoice_homepage'))

    return render_template("view_invoice.html", freelancer=freelancer, invoice=invoice, client=client, user=user)

@app.route("/contact")
def contact():
    """Contact page"""
    return render_template('contact.html')
@app.route("/payinvoice/<int:invoice_id>", methods=["POST"])
def pay_invoice(invoice_id):
    """Handle invoice payment"""
    username = session.get('username')
    user = postgres_database.user_database.find_user(username)
    invoice = postgres_database.invoice_database.get_invoice_by_id(invoice_id)

    if not invoice:
        flash("Invoice not found.")
        return redirect(url_for('invoice_homepage'))
    
    if postgres_database.banking_system.transfer(user.user_id,invoice.client_id, invoice.total_amount):
        # Update user balances in database
        postgres_database.update_user_balance(user)
        postgres_database.update_user_balance(invoice.client_id)
        postgres_database.insert_all_transactions()
        flash(f"Successfully paid invoice ${invoice.total_amount:.2f}!")
        if invoice.mark_as_paid():
            postgres_database.update_invoice_status(invoice)
            flash("Invoice marked as paid!")
        else:
            flash("Failed to mark invoice as paid.")

    return redirect(url_for('view_invoice', invoice=invoice))

if __name__ == "__main__":
    app.run(debug=True, port=5000)