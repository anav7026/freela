from Transaction import Transaction

class TransactionDatabase:
    def __init__(self):
        self.transactions = []
        self.global_transaction_dictionary = {}

    def add_transaction(self, sender_id, receiver_id, transaction_type, amount, timestamp):
        new_transaction = Transaction(sender_id, receiver_id, transaction_type, amount, timestamp)

        for user_id in [sender_id, receiver_id]:
            if user_id not in self.global_transaction_dictionary:
                self.global_transaction_dictionary[user_id] = []
            self.global_transaction_dictionary[user_id].append(new_transaction)

        self.transactions.append(new_transaction)
        return True

    def print_transactions(self):
        return [transaction.to_str() for transaction in self.transactions]

    def clear_transactions(self):
        self.transactions.clear()
    
    def get_transaction_by_id(self, user_id):
        """Get transaction by user ID."""
        
        return self.global_transaction_dictionary.get(user_id,[]) # using dictionary instead of updating or searching database again