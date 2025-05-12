from Client import Client
from Freelancer import Freelancer


class User:
    def __init__(self, user_id, username, password, first_name, last_name, street_address,apt,city,state,zip_code,ssn,email,role,total_income,tax_saving_rate):
        self.user_id = user_id
        self.username = username
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.street_address = street_address
        self.apt = apt
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.ssn = ssn
        self.email = email
        self.role = role
        self.total_income=float(total_income)
        self.tax_saving_rate=float(tax_saving_rate)
        self.client=None
        self.freelancer=None
        
        if role =="client":
            self.client = Client(user_id)
        if role == "freelancer":
            self.freelancer= Freelancer(user_id,total_income,tax_saving_rate)

    def get_user_id(self):
        """Get the user ID."""
        return self.user_id
    
    def get_user_role(self):
        """Get the user role."""
        return self.role
    
    def get_total_income(self):
        """Get the user's total balance."""
        return self.total_income
        
    def is_client(self):
        """Check if user is a client."""
        return self.role == "client"
        
    def is_freelancer(self):
        """Check if user is a freelancer."""
        return self.role == "freelancer"
    
    
    
    