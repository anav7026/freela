from User import User
from UserDatabase import UserDatabase
from Transaction import Transaction
from TransactionDatabase import TransactionDatabase
from TaxDocument import TaxDocument
from TaxDocumentDatabase import TaxDocumentDatabase
from BankingSystem import BankingSystem
import os
import psycopg2

class Database:
    def __init__(self, postgres_database=os.getenv("DATABASE_URL", "postgresql://myuser:mypassword@localhost:5432/mydatabase")):
        self.user_database = UserDatabase()
        self.transaction_database = TransactionDatabase()
        self.tax_document_database = TaxDocumentDatabase()
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
                # User Row: [id, username, password, total, saving_rate_preference]
                self.user_database.add_user(row[0], row[1], row[2], row[3], row[4])
            elif cls == Transaction:
                # Transaction Row: [sender_id, receiver_id, transaction_type, amount, timestamp]
                self.transaction_database.add_transaction(row[0], row[1], row[2], row[3], row[4])
            elif cls == TaxDocument:
                # TaxDocument Row: [form_name, due_date, description, pdf_link]
                self.tax_document_database.add_tax_document(row[0], row[1], row[2], row[3])
        
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
    
    def load_all_databases(self):
        """Load all databases from PostgreSQL."""
        self.load_users()
        self.load_transactions()
        self.load_tax_documents()

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
        query = "INSERT INTO users (id, username, passwords, total, tax_rate) VALUES (%s, %s, %s, %s, %s)"
        values = (user.user_id, user.username, user.password, user.total, user.saving_rate_preference)
        self.insert_execution(query, values)
    
    def insert_transaction(self, transaction):
        """Insert a transaction into the database."""
        query = "INSERT INTO transactions (sender_id, receiver_id, transaction_type, amount, timestamp) VALUES (%s, %s, %s, %s, %s)"
        values = (transaction.sender_id, transaction.receiver_id, transaction.transaction_type, transaction.amount, transaction.timestamp)
        self.insert_execution(query, values)
    
    def insert_all_transactions(self):
        """Insert all transactions into the database."""
        for transaction in self.transaction_database.transactions:
            self.insert_transaction(transaction)
        return True

    def update_user_balance(self, user):
        """Update a user's balance in the database."""
        query = "UPDATE users SET total = %s WHERE id = %s"
        values = (user.total, user.user_id)
        self.insert_execution(query, values)

    