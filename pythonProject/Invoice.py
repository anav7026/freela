from Item import Item
class Invoice:
    def __init__(self,freelancer_id,client_id,invoice_date,payment_due_date):
        self.invoice_id = None  # Will be set when added to database
        self.freelancer_id = freelancer_id
        self.client_id = client_id
        self.invoice_date = invoice_date
        self.payment_due_date = payment_due_date
        self.receipt_items = []  # Fixed variable name
        self.status = "unpaid"  # Can be "unpaid", "paid", "overdue"
        self.total_amount = 0.0

    def add_item(self, name, description, quantity, amount):
        """Add an item to this invoice"""
        item_id = len(self.receipt_items) + 1  
        item = Item(item_id,self.invoice_id,name, description, quantity, amount)
        self.receipt_items.append(item)
        self.total_amount += quantity * amount
        return item
        
    def finalize(self):
        """Finalize the invoice, changing status from draft to sent"""
        if self.status == "unpaid" and len(self.receipt_items) > 0:
            self.status = "unpaid"
            return True
        return False
        
    def mark_as_paid(self):
        """Mark the invoice as paid"""
        if self.status == "unpaid" or self.status == "overdue":
            self.status = "paid"
            return True
        return False
    
    def to_dict(self):
        """Convert invoice to dictionary for display purposes"""
        return {
            "invoice_id": self.invoice_id,
            "freelancer_id": self.freelancer_id,
            "client_id": self.client_id,
            "invoice_date": self.invoice_date,
            "payment_due_date": self.payment_due_date,
            "items": [item.to_dict() for item in self.receipt_items],
            "status": self.status,
            "total_amount": self.total_amount
        }
    