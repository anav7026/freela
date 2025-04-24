# BankingSystem.py
from UserDatabase import UserDatabase
from Transaction import Transaction
from TransactionDatabase import TransactionDatabase

class BankingSystem:
    def __init__(self, user_db, transaction_db):
        self.user_db = user_db
        self.transaction_db = transaction_db
    
    def get_spendable_balance(self, username):
        """Calculate the spendable balance for a user."""
        user = self.user_db.find_user(username)
        if user:
            # Spendable balance is total minus savings portion 
            return user.total * (1 - user.saving_rate_preference)
        return 0
    
    def get_savings_income(self, username):
        """Calculate the savings income for a user."""
        user = self.user_db.find_user(username)
        if user:
            # Savings income is savings portion of total
            return user.total * user.saving_rate_preference
        return 0
    
    def deposit(self, username, amount):
        """Deposit money to the user's account and record the transaction."""
        user = self.user_db.find_user(username)
        if user and amount > 0:
            user.total += amount
            
            # Record the transaction
            self.transaction_db.add_transaction(
                user.user_id,  # sender (self in this case)
                user.user_id,  # receiver (self in this case)
                "deposit",
                amount,
                None  # Let Transaction class set timestamp to now
            )
            return True
        return False

    def withdraw(self, username, amount):
        """Withdraw money from the user's account and record the transaction."""
        user = self.user_db.find_user(username)
        if user and amount > 0:
            # Check if user has enough funds
            if user.total >= amount:
                user.total -= amount
                
                # Record the transaction
                self.transaction_db.add_transaction(
                    user.user_id,  # sender
                    user.user_id,  # receiver (self in this case)
                    "withdrawal",
                    amount,
                    None  # Let Transaction class set timestamp to now
                )
                return True
        return False

    def transfer(self, sender_username, receiver_username, amount):
        """Transfer money between users and record the transaction."""
        sender = self.user_db.find_user(sender_username)
        receiver = self.user_db.find_user(receiver_username)
        
        if sender and receiver and amount > 0:
            # Check if sender has enough funds
            if sender.total >= amount:
                sender.total -= amount
                receiver.total += amount
                
                # Record the transaction
                self.transaction_db.add_transaction(
                    sender.user_id,
                    receiver.user_id,
                    "transfer",
                    amount,
                    None  # Let Transaction class set timestamp to now
                )
                return True
        return False

    def show_transaction_history(self, username):
        """Get transaction history for a user."""
        user = self.user_db.find_user(username)
        if user:
            return self.transaction_db.get_transaction_by_id(user.user_id)
        return []