from User import User
from UserDatabase import UserDatabase
from Transaction import Transaction
from TransactionDatabase import TransactionDatabase
from TaxDocument import TaxDocument
from TaxDocumentDatabase import TaxDocumentDatabase
from BankingSystem import BankingSystem
import os
import psycopg2

user_db = UserDatabase()
transaction_db = TransactionDatabase()
TaxDocument_db = TaxDocumentDatabase()
banking_system = BankingSystem(user_db)

class Database:
    def __init__(self, postgres_database=os.getenv("DATABASE_URL", "postgresql://myuser:mypassword@localhost:5432/mydatabase")):
        
        self.user_database = user_db
        self.transaction_database = transaction_db
        self.tax_document_database = TaxDocument_db
        self.banking_system = banking_system
        self.postgres_database = postgres_database
        

        

    def connect_to_postgres(self):
        """Create and return a connection to the PostgreSQL database."""
        postgres_connection = psycopg2.connect(self.postgres_database)
        return postgres_connection
    
    def disconnect_from_postgres(self, postgres_connection):
        """Close the connection to the PostgreSQL database."""
        postgres_connection.close()

    def load_execution(self,cls,execution):
        connection = self.connect_to_postgres()
        cursor = connection.cursor()
        cursor.execute(execution)
        rows = cursor.fetchall()
        for row in rows:
            user = row  #User Row : [id,username, password, total, saving_rate_preference]
                        #Transaction Row : [sender_id, reciever_id, transaction_type, amount, timestamp]
                        #TaxDocument Row : [form name, due date, description, pdf link]
            
            
            if cls == User : 
                self.user_database.add_user(user[0],user[1],user[2],user[3],user[4])
                print (user[0],user[1],user[2],user[3],user[4])
            if cls == Transaction : 
                self.transaction_database.add_transaction(user[0],user[1],user[2],user[3],user[4])
                print (user[0],user[1],user[2],user[3],user[4])
            if cls == TaxDocument : 
                self.tax_document_database.add_tax_document(user[0],user[1],user[2],user[3])
                print (user[0],user[1],user[2],user[3])
        cursor.close()
        self.disconnect_from_postgres(connection)

    

    def load_users(self):
        self.load_execution(User,"SELECT * FROM users")
    def load_tax_documents(self):
        self.load_execution(TaxDocument,"SELECT * FROM tax_documents")
    def load_transactions(self):
        self.load_execution(Transaction,"SELECT * FROM transactions")
    
    def load_all_databases(self):
        """Load all databases from PostgreSQL."""
        self.load_users()
        self.load_transactions()
        self.load_tax_documents()

   
    