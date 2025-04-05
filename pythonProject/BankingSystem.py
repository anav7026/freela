# BankingSystem.py
from UserDatabase import UserDatabase
from Transaction import Transaction

class BankingSystem:
    def __init__(self, user_db):
        self.user_db = user_db
        # Other initialization code

    
    def get_spendable_balance(self, username):
        """Calculate the spendable balance for a user."""
        user = self.user_db.find_user(username)
        if user:
            # Assuming the spendable balance is total - saving_rate_preference
            return user.total - (1-user.saving_rate_preference)
        return 0
    def get_savings_income(self, username):
        """Calculate the savings income for a user."""
        user = self.user_db.find_user(username)
        if user:
            # Assuming the savings income is total * saving_rate_preference
            return user.total * user.saving_rate_preference
        return 0
    
    def deposit(self, username, amount):
        """Deposit money to the user's account and record the transaction."""
        pass

    def withdraw(self, username, amount):
        pass

    def transfer(self, sender_username, receiver_username, amount):
       pass

    def show_transaction_history(self, username):
        pass

    def get_user_transactions(self, username):
        """Fetch user transactions from the database"""
        from main import get_db_connection  # Move import here to avoid circular import
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, timestamp, transaction_type, amount, sender, receiver FROM transactions WHERE sender = %s OR receiver = %s", (username, username))
        transactions = cur.fetchall()
        cur.close()
        conn.close()

        transaction_list = []
        for tx in transactions:
            transaction = {
                "timestamp": tx[1],
                "transaction_type": tx[2],
                "amount": tx[3],
                "sender": tx[4],
                "receiver": tx[5]
            }
            transaction_list.append(transaction)

        return transaction_list
