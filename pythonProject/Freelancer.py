from Invoice import Invoice
from TaxDocument import TaxDocument

class Freelancer:
    def __init__(self, user_id, total_income, tax_saving_rate):
        self.user_id = user_id
        self.total_income = float(total_income)
        self.tax_saving_rate = float(tax_saving_rate)
        self.client_list = []
        self.invoice_list = []
        self.tax_doc_list = {}  # {irs_id: {"tax_doc": TaxDocument, "completed": bool}}

    def add_client(self, client_id):
        if client_id not in self.client_list:
            self.client_list.append(client_id)
            return True
        return False

    def create_invoice(self, client_id, invoice_date, payment_due_date):
        """Create a new invoice for a client"""
        invoice = Invoice(self.user_id, client_id, invoice_date, payment_due_date)
        self.invoice_list.append(invoice)
        return invoice

    def get_invoices(self):
        """Return all invoices created by this freelancer"""
        return self.invoice_list

    def add_tax_document(self, irs_id, tax_document):
        """Add a tax document to the freelancer's tax_doc_list"""
        if irs_id not in self.tax_doc_list:
            self.tax_doc_list[irs_id] = {"tax_doc": tax_document, "completed": False}
            return True
        return False

    def mark_tax_document_completed(self, irs_id):
        """Mark a tax document as completed"""
        if irs_id in self.tax_doc_list:
            self.tax_doc_list[irs_id]["completed"] = True
            return True
        return False

    def get_tax_documents(self):
        """Return all tax documents for this freelancer"""
        return self.tax_doc_list




