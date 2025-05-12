from Item import Item
from User import User
from UserDatabase import UserDatabase
from Transaction import Transaction
from TransactionDatabase import TransactionDatabase
from TaxDocument import TaxDocument
from TaxDocumentDatabase import TaxDocumentDatabase
from BankingSystem import BankingSystem
from InvoiceDatabase import InvoiceDatabase
from Invoice import Invoice
from UserTaxDocument import UserTaxDocument
from UserTaxDocumentDatabase import UserTaxDocumentDatabase
import os
import psycopg2

class Database:
    def __init__(self, postgres_database=os.getenv("DATABASE_URL", "postgresql://myuser:mypassword@localhost:5432/mydatabase")):
        self.user_database = UserDatabase()
        self.transaction_database = TransactionDatabase()
        self.tax_document_database = TaxDocumentDatabase()
        self.invoice_database = InvoiceDatabase()  # Add invoice database
        self.user_tax_document_database = UserTaxDocumentDatabase()
        self.banking_system = BankingSystem(self.user_database, self.transaction_database)
        self.postgres_database = postgres_database

    def connect_to_postgres(self):
        """Create and return a connection to the PostgreSQL database."""
        postgres_connection = psycopg2.connect(self.postgres_database)
        return postgres_connection
    
    def disconnect_from_postgres(self, postgres_connection):
        """Close the connection to the PostgreSQL database."""
        postgres_connection.close()

    def load_execution(self, cls, execution):
        """Execute a query and load results into appropriate database."""
        connection = self.connect_to_postgres()
        cursor = connection.cursor()
        cursor.execute(execution)
        rows = cursor.fetchall()
        
        for row in rows:
            if cls == User:
                # User Row: [id, username, password, first_name,last_name, street_address, apt, city, state, zip_code,ssn,email,role,total_income,tax_saving_rate]
                self.user_database.add_user(row[0], row[1], row[2], row[3], row[4],row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12],row[13],row[14])
            elif cls == Transaction:
                # Transaction Row: [sender_id, receiver_id, transaction_type, amount, timestamp]
                self.transaction_database.add_transaction(row[0], row[1], row[2], row[3], row[4])
            elif cls == TaxDocument:
                # TaxDocument Row: [Tax Doc Name, Due Date(s), PDF Link, IRS Key, why, How To, description]
                self.tax_document_database.add_tax_document(row[0], row[1], row[2], row[3],row[4],row[5],row[6],row[7])
            elif cls == UserTaxDocument:
                # UserTaxDocument Row: [id, user_id, irs_key, completion_status]
                user_tax_doc = UserTaxDocument(row[0], row[1], row[2], row[3])
                self.user_tax_document_database.user_tax_documents.append(user_tax_doc)
                # Update next_id if needed
                if row[0] >= self.user_tax_document_database.next_id:
                    self.user_tax_document_database.next_id = row[0] + 1
            elif cls == Invoice:
                # Invoice Row [invoice_id,freelancer_id,client_id, invoice_date,payment_due_date,reciept_items,status,total_amount]
                invoice = self.invoice_database.add_invoice(row[1], row[2], row[3], row[4])
                invoice.invoice_id = row[0]  # Set the invoice ID
                invoice.status = row[6]
                invoice.total_amount = row[7]
            elif cls == Item:
                # Item Row: [item_id,invoice_id,name,description,quantity,amount]
                invoice = self.invoice_database.get_invoice_by_id(row[1])
                if invoice:
                    item = Item(row[0], row[1], row[2], row[3], row[4], row[5])
                    invoice.receipt_items.append(item)
                    self.invoice_database.items.append(item)
        
        cursor.close()
        self.disconnect_from_postgres(connection)

    def load_users(self):
        """Load users from database."""
        self.load_execution(User, "SELECT * FROM users")
        
    def load_tax_documents(self):
        """Load tax documents from database."""
        self.load_execution(TaxDocument, "SELECT * FROM tax_documents")
        
    def load_transactions(self):
        """Load transactions from database."""
        self.load_execution(Transaction, "SELECT * FROM transactions")

    def load_invoices(self):
        self.load_execution(Invoice,"SELECT * FROM invoices")
    
    def load_items(self):
        self.load_execution(Item,"SELECT * FROM items")
    
    def load_all_databases(self):
        """Load all databases from PostgreSQL."""
        self.load_users()
        self.load_transactions()
        self.load_tax_documents()
        self.load_invoices()
        self.load_items()

    def insert_execution(self, query, values):
        """Execute an insert query with values."""
        connection = self.connect_to_postgres()
        cursor = connection.cursor()
        cursor.execute(query, values)
        connection.commit()
        cursor.close()
        self.disconnect_from_postgres(connection)

    def insert_new_user(self, user):
        """Insert a new user into the database."""
        query = "INSERT INTO users (id, username, password, first_name, last_name, street_address, apt, city, state, zip_code, ssn, email, role, total_income, tax_saving_rate) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        values = (user.user_id, user.username, user.password, user.first_name, user.last_name, user.street_address, user.apt, user.city, user.state, user.zip_code, user.ssn, user.email, user.role, user.total_income, user.tax_saving_rate)
        self.insert_execution(query, values)
    
    def insert_transaction(self, transaction):
        """Insert a transaction into the database."""
        query = "INSERT INTO transactions (sender_id, receiver_id, transaction_type, amount, timestamp) VALUES (%s, %s, %s, %s, %s)"
        values = (transaction.sender_id, transaction.receiver_id, transaction.transaction_type, transaction.amount, transaction.timestamp)
        self.insert_execution(query, values)

    def insert_user_tax_document(self, user_tax_doc):
        """Insert a user tax document into the database."""
        query = "INSERT INTO user_tax_documents (id, user_id, irs_key, completion_status) VALUES (%s, %s, %s, %s)"
        values = (user_tax_doc.id, user_tax_doc.user_id, user_tax_doc.irs_key, user_tax_doc.completion_status)
        self.insert_execution(query, values)

    def insert_all_transactions(self):
        """Insert all transactions into the database."""
        for transaction in self.transaction_database.transactions:
            self.insert_transaction(transaction)
        return True
    
    def insert_invoice(self, invoice):
        """Insert an invoice into the database."""
        query = "INSERT INTO invoices (invoice_id, freelancer_id, client_id, invoice_date, payment_due_date, receipt_items, status, total_amount) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        values = (invoice.invoice_id, invoice.freelancer_id, invoice.client_id, invoice.invoice_date, invoice.payment_due_date, str(invoice.receipt_items), invoice.status, invoice.total_amount)
        self.insert_execution(query, values)

    def insert_item(self, item):
        """Insert an item into the database."""
        query = "INSERT INTO items (item_id, invoice_id, name, description, quantity, amount) VALUES (%s, %s, %s, %s, %s, %s)"
        values = (item.item_id, item.invoice_id, item.name, item.description, item.quantity, item.amount)
        self.insert_execution(query, values)

    def update_user_balance(self, user):
        """Update a user's balance in the database."""
        query = "UPDATE users SET total_income = %s WHERE id = %s"
        values = (user.total_income, user.user_id)
        self.insert_execution(query, values)

    def update_invoice_status(self, invoice):
        """Update an invoice's status in the database."""
        query = "UPDATE invoices SET status = %s WHERE invoice_id = %s"
        values = (invoice.status, invoice.invoice_id)
        self.insert_execution(query, values)
    def update_tax_saving_rate(self, user):
        """Update a user's tax saving rate in the database."""
        query = "UPDATE users SET tax_saving_rate = %s WHERE id = %s"
        values = (user.tax_saving_rate, user.user_id)
        self.insert_execution(query, values)

    def update_user_tax_document_status(self, user_tax_doc):
        """Update a user tax document's completion status in the database."""
        query = "UPDATE user_tax_documents SET completion_status = %s WHERE id = %s"
        values = (user_tax_doc.completion_status, user_tax_doc.id)
        self.insert_execution(query, values)