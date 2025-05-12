from TaxDocument import TaxDocument
from datetime import datetime, date

class TaxDocumentDatabase:
    def __init__(self, global_doc_dictionary=None):
        self.tax_doc_lst = []
        self.global_doc_dictionary = global_doc_dictionary if global_doc_dictionary else {}
        
        
    def add_tax_document(self, form_name, due_date,pdf_link,irs_key,status,why,how_to, description):
        """Add a new tax document to the database."""
        new_tax_document = TaxDocument(form_name, due_date, pdf_link,irs_key,status,why,how_to,description)
        self.global_doc_dictionary[irs_key] = new_tax_document
        self.tax_doc_lst.append(new_tax_document)
        return True
    
    def get_all_documents(self):
        """Get all tax documents."""
        return self.tax_doc_lst
    
    def get_document_by_name(self, form_name: str):
        """Get tax document by name."""
        return self.global_doc_dictionary.get(form_name)
    
    def get_documents_by_due_date(self, due_date: date):
        """Get tax documents by due date."""
        return [doc for doc in self.tax_doc_lst if doc.due_date == due_date]
    