from UserTaxDocument import UserTaxDocument

class UserTaxDocumentDatabase:
    def __init__(self):
        self.user_tax_documents = []
        self.next_id = 1
    
    def add_user_tax_document(self, user_id, irs_key, completion_status="Not Started"):
        """Add a new user-tax document relationship."""
        user_tax_doc = UserTaxDocument(self.next_id, user_id, irs_key, completion_status)
        self.user_tax_documents.append(user_tax_doc)
        self.next_id += 1
        return user_tax_doc
    
    def get_user_tax_documents(self, user_id):
        """Get all tax documents for a specific user."""
        return [doc for doc in self.user_tax_documents if doc.user_id == user_id]
    
    def get_user_tax_document(self, user_id, irs_key):
        """Get a specific tax document for a user."""
        for doc in self.user_tax_documents:
            if doc.user_id == user_id and doc.irs_key == irs_key:
                return doc
        return None
    
    def update_document_status(self, user_id, irs_key, new_status):
        """Update the status of a tax document for a user."""
        user_tax_doc = self.get_user_tax_document(user_id, irs_key)
        if user_tax_doc:
            return user_tax_doc.update_status(new_status)
        return False
    
    def get_user_tax_document_by_id(self, id):
        """Get a user tax document by its ID."""
        for doc in self.user_tax_documents:
            if doc.id == id:
                return doc
        return None