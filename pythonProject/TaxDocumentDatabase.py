from TaxDocument import TaxDocument

class TaxDocumentDatabase:
    def __init__(self, global_doc_dictionary=None):
        self.tax_doc_lst = []
        self.global_doc_dictionary = global_doc_dictionary if global_doc_dictionary else {}
        
    def add_tax_document(self, form_name, due_date, description, form_pdf):
        """Add a new tax document to the database."""
        new_tax_document = TaxDocument(form_name, due_date, description, form_pdf)
        self.global_doc_dictionary[form_name] = new_tax_document
        self.tax_doc_lst.append(new_tax_document)
        return True
    
    def get_all_documents(self):
        """Get all tax documents."""
        return self.tax_doc_lst
    
    def get_document_by_name(self, form_name):
        """Get tax document by name."""
        return self.global_doc_dictionary.get(form_name)