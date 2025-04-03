import psycopg2
import os
from datetime import datetime

# Get DATABASE_URL from environment or fallback to default if not set
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://myuser:mypassword@localhost:5432/mydatabase")

class Transaction:
    def __init__(self, transaction_type, amount, sender, receiver=None, timestamp=None):
        self.timestamp = timestamp if timestamp else datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.transaction_type = transaction_type  # "deposit", "withdrawal", "transfer"
        self.amount = amount
        self.sender = sender
        self.receiver = receiver

    def to_dict(self):
        """Convert the transaction object to a dictionary."""
        return {
            "timestamp": self.timestamp,
            "transaction_type": self.transaction_type,
            "amount": self.amount,
            "sender": self.sender,
            "receiver": self.receiver
        }

    @classmethod
    def from_dict(cls, data):
        """Create a transaction object from a dictionary."""
        return cls(
            transaction_type=data["transaction_type"],
            amount=data["amount"],
            sender=data["sender"],
            receiver=data.get("receiver"),
            timestamp=data["timestamp"]
        )

    def __str__(self):
        """String representation of the transaction."""
        if self.transaction_type == "transfer":
            return f"[{self.timestamp}] {self.sender} transferred ${self.amount:.2f} to {self.receiver}"
        return f"[{self.timestamp}] {self.sender} {self.transaction_type}ed ${self.amount:.2f}"

    @staticmethod
    def get_db_connection():
        """Create and return a connection to the PostgreSQL database."""
        conn = psycopg2.connect(DATABASE_URL)
        return conn

    @classmethod
    def create_transaction(cls, transaction_type, amount, sender, receiver=None):
        """Insert a new transaction into the database."""
        conn = cls.get_db_connection()
        cur = conn.cursor()
        try:
            cur.execute(
                "INSERT INTO transactions (transaction_type, amount, sender, receiver, timestamp) VALUES (%s, %s, %s, %s, %s)",
                (transaction_type, amount, sender, receiver, datetime.now())
            )
            conn.commit()  # Save changes to the database
            cur.close()
            conn.close()
            return True
        except Exception as e:
            print(f"Error creating transaction: {e}")
            conn.rollback()  # Rollback in case of error
            cur.close()
            conn.close()
            return False

    @classmethod
    def get_transactions_by_user(cls, username):
        """Get all transactions related to a specific user (sender or receiver)."""
        conn = cls.get_db_connection()
        cur = conn.cursor()
        cur.execute(
            "SELECT * FROM transactions WHERE sender = %s OR receiver = %s ORDER BY timestamp DESC",
            (username, username)
        )
        transaction_data = cur.fetchall()
        cur.close()
        conn.close()

        # Convert each row into a Transaction object
        transactions = [
            cls(
                transaction_type=row[1],  # transaction_type
                amount=row[2],             # amount
                sender=row[3],             # sender
                receiver=row[4],           # receiver
                timestamp=row[5]          # timestamp
            ) for row in transaction_data
        ]
        return transactions

    @classmethod
    def get_all_transactions(cls):
        """Get all transactions from the database."""
        conn = cls.get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM transactions ORDER BY timestamp DESC")
        transaction_data = cur.fetchall()
        cur.close()
        conn.close()

        # Convert each row into a Transaction object
        transactions = [
            cls(
                transaction_type=row[1],  # transaction_type
                amount=row[2],             # amount
                sender=row[3],             # sender
                receiver=row[4],           # receiver
                timestamp=row[5]          # timestamp
            ) for row in transaction_data
        ]
        return transactions

