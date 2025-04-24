from Transaction import Transaction

class TransactionDatabase:
    def __init__(self):
        self.transactions = []
        self.global_transaction_dictionary = {}

    def add_transaction(self, sender_id, receiver_id, transaction_type, amount, timestamp):
        """Add a new transaction to the database."""
        new_transaction = Transaction(sender_id, receiver_id, transaction_type, amount, timestamp)

        # Update user-specific transaction lists
        for user_id in [sender_id, receiver_id]:
            if user_id not in self.global_transaction_dictionary:
                self.global_transaction_dictionary[user_id] = []
            self.global_transaction_dictionary[user_id].append(new_transaction)

        # Add to global transactions
        self.transactions.append(new_transaction)
        return True

    def print_transactions(self):
        """Return string representations of all transactions."""
        return [transaction.to_str() for transaction in self.transactions]

    def clear_transactions(self):
        """Clear all transactions."""
        self.transactions.clear()
        self.global_transaction_dictionary.clear()
    
    def get_transaction_by_id(self, user_id):
        """Get transactions by user ID."""
        return self.global_transaction_dictionary.get(user_id, [])