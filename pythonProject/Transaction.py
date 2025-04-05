import psycopg2
import os
from datetime import datetime



class Transaction:
    def __init__(self, sender_id, receiver_id, transaction_type, amount, timestamp=None):
        self.sender_id = sender_id
        self.receiver_id = receiver_id
        self.transaction_type = transaction_type  # "deposit", "withdrawal", "transfer"
        self.amount = amount
        self.timestamp = timestamp if timestamp else datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    
    def to_str(self):
        return f"Transaction({self.sender_id}, {self.receiver_id}, {self.transaction_type}, {self.amount}, {self.timestamp})"
    
    