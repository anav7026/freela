class UserTaxDocument:
    def __init__(self, id, user_id, irs_key, completion_status="Not Started"):
            self.id = id
            self.user_id = user_id
            self.irs_key = irs_key
            self.completion_status = completion_status  # "Not Started", "In Progress", "Completed"
        
    def update_status(self, new_status):
            """Update the completion status of the tax document for this user."""
            valid_statuses = ["Not Started", "In Progress", "Completed"]
            if new_status in valid_statuses:
                self.completion_status = new_status
                return True
            return False
        
    def __str__(self):
            return f"UserTaxDocument(id={self.id}, user_id={self.user_id}, irs_key={self.irs_key}, status={self.completion_status})"