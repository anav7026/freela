from User import User

class UserDatabase:
    def __init__(self):
        self.users = []
        self.username_to_user = {}  # For quick lookups
    
    def add_user(self, user_id, username, password, total=0, saving_rate_preference=0.2):
        """Add a new user to the database."""
        if username in self.username_to_user:
            return False
        
        new_user = User(user_id, username, password, total, saving_rate_preference)
        self.users.append(new_user)
        self.username_to_user[username] = new_user
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