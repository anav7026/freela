# BankingSystem.py
from UserDatabase import UserDatabase
from Transaction import Transaction

class BankingSystem:
    def __init__(self, user_db):
        self.user_db = user_db
        # Other initialization code

    def deposit(self, username, amount):
        """Deposit money to the user's account and record the transaction."""
        user = self.user_db.find_user(username)
        if user and amount > 0:
            user.total += amount
            user.spendable_income = float(user.total * 0.80)  # Update spendable income
            user.tax_savings = float(user.total * 0.20)       # Update tax savings
            
            self.user_db.save_users()  # Save user data to DB
            Transaction.create_transaction("deposit", amount, username)  # Record transaction
            
            print(f"✅ Deposited ${amount}. New balance: ${user.total:.2f}")
            return True
        print("❌ Invalid deposit amount!")
        return False

    def withdraw(self, username, amount):
        """Withdraw money from the user's account and record the transaction."""
        user = self.user_db.find_user(username)
        if user and 0 < amount <= user.total:
            user.total -= amount
            user.spendable_income = float(user.total * 0.80)  # Update spendable income
            user.tax_savings = float(user.total * 0.20)       # Update tax savings
            
            self.user_db.save_users()  # Save user data to DB
            Transaction.create_transaction("withdrawal", amount, username)  # Record transaction
            
            print(f"✅ Withdrawn ${amount}. New balance: ${user.total:.2f}")
            return True
        print("❌ Insufficient funds or invalid amount!")
        return False

    def transfer(self, sender_username, receiver_username, amount):
        """Transfer money from sender to receiver and record both transactions."""
        sender = self.user_db.find_user(sender_username)
        receiver = self.user_db.find_user(receiver_username)

        if not sender or not receiver:
            print("❌ Sender or receiver not found!")
            return False

        if sender_username == receiver_username:
            print("❌ Cannot transfer to yourself!")
            return False

        if 0 < amount <= sender.total:
            # Update sender's account
            sender.total -= amount
            sender.spendable_income = float(sender.total * 0.80)  # Update sender's spendable income
            sender.tax_savings = float(sender.total * 0.20)       # Update sender's tax savings

            # Update receiver's account
            receiver.total += amount
            receiver.spendable_income = float(receiver.total * 0.80)  # Update receiver's spendable income
            receiver.tax_savings = float(receiver.total * 0.20)       # Update receiver's tax savings
            
            self.user_db.save_users()  # Save updated user data to DB
            
            # Record transactions for sender and receiver
            Transaction.create_transaction("transfer", amount, sender_username, receiver_username)
            Transaction.create_transaction("received", amount, receiver_username, sender_username)
            
            print(f"✅ Transferred ${amount:.2f} from {sender_username} to {receiver_username}")
            return True

        print("❌ Insufficient funds for transfer!")
        return False

    def show_transaction_history(self, username):
        """Show transaction history for a given user."""
        transactions = Transaction.get_transactions_by_user(username)
        if transactions:
            print(f"📜 Transaction History for {username}:")
            for transaction in transactions:
                print(transaction)
        else:
            print(f"❌ No transactions found for {username}.")

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
