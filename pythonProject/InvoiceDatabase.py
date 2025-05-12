from datetime import datetime
from Invoice import Invoice
from Item import Item

class InvoiceDatabase:
    def __init__(self):
        self.invoices = []
        self.items = []
        self.next_invoice_id = 1
        
        
    def add_invoice(self, freelancer_id, client_id, invoice_date, payment_due_date):
        """Add a new invoice to the database"""
        invoice = Invoice(freelancer_id, client_id, invoice_date, payment_due_date)
        invoice.invoice_id = self.next_invoice_id
        self.next_invoice_id += 1
        self.invoices.append(invoice)
        return invoice
    
    def add_item_to_invoice(self, invoice_id, name, description, quantity, amount):
        """Add an item to an existing invoice"""
        invoice = self.get_invoice_by_id(invoice_id)
        if invoice:
            item = invoice.add_item(name, description, quantity, amount)
            self.items.append(item)
            return item
        return None
        
    def get_invoice_by_id(self, invoice_id):
        """Get an invoice by its ID"""
        for invoice in self.invoices:
            if invoice.invoice_id == invoice_id:
                return invoice
        return None
        
    def get_invoices_by_freelancer_id(self, freelancer_id):
        """Get all invoices created by a freelancer"""
        return [invoice for invoice in self.invoices if invoice.freelancer_id == freelancer_id]
        
    def get_invoices_by_client_id(self, client_id):
        """Get all invoices sent to a client"""
        return [invoice for invoice in self.invoices if invoice.client_id == client_id]