class Item:
    def __init__(self,item_id,invoice_id,name,description, quantity, amount):
        self.item_id=item_id
        self.invoice_id=invoice_id
        self.name=name
        self.description=description
        self.quantity=quantity
        self.amount=amount

    def get_total(self):
        """Calculate the total cost for this item"""
        return self.quantity * self.amount
        
    def to_dict(self):
        """Convert item to dictionary for display purposes"""
        return {
            "item_id": self.item_id,
            "invoice_id": self.invoice_id,
            "name": self.name,
            "description": self.description,
            "quantity": self.quantity,
            "amount": self.amount,
            "total": self.get_total()
        }