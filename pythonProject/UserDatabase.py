from User import User

class UserDatabase :
    def __init__(self):
        self.users=[]

    def find_user(self,username):
        for user in self.users:
            if user.username == username:
                return user 
        return None
    
    def add_user(self, username,password):
        if self.find_user(username): 
            print(f"{username} already exist")
            return False
        
        new_user=User(username,password)
        self.users.append(new_user)
        print(f"{username} added successfully")
        return True
    
    
    def authenticate(self, username, password):
        user = self.find_user(username)
        if user and user.password == password:
            print(f"Welcome, {username}!")
            return True
        print("Invalid username or password!")
        return False

    def list_users(self):
        # Display all users (for debugging purposes)
        for user in self.users:
            print(user)
