from User import User

class UserDatabase:
    def __init__(self):
        self.users = []
        self.freelancers=[]
        self.clients=[]
        self.username_to_user = {}  # For quick lookups 
        self.user_id_to_user={}
    
    def add_user(self, user_id, username, password,first_name,last_name,street_address,apt,city,state,zip_code,ssn,email, role,total_income,tax_saving_rate):
        """Add a new user to the database."""
        if username in self.username_to_user:
            return False
        
        new_user = User(user_id, username, password, first_name,last_name, street_address,apt,city,state,zip_code,ssn,email,role,total_income,tax_saving_rate)
        self.users.append(new_user)
        if role == "client":
            self.clients.append(new_user)
        elif role == "freelancer":
            self.freelancers.append(new_user)
        self.username_to_user[username] = new_user
        self.user_id_to_user[user_id]=new_user
        return True
    
    def find_user(self, username):
        """Find a user by username."""
        return self.username_to_user.get(username)
    
    def authenticate(self, username, password):
        """Authenticate a user."""
        user = self.find_user(username)
        if user and user.password == password:
            return True
        return False
    
    def list_users(self):
        """List all usernames."""
        return [user.username for user in self.users]
    
    def find_user_with_id(self,user_id):
        return self.user_id_to_user.get(user_id)