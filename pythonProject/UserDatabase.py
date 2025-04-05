from User import User
import json 
import os
import psycopg2


class UserDatabase:
    def __init__(self, global_user_dictionary=None):
        self.users = []
        self.global_user_dictionary = global_user_dictionary if global_user_dictionary else {}
        

    
        



    def find_user(self, username):
        """Find a user in the database by username."""
        for user in self.users:
            if user.username == username:
                return user
        return None
    
    def add_user(self, user_id,username, password,total, saving_rate_preference):
        """Add a new user to the database."""
        if username in self.global_user_dictionary:
            print("User already exists.")
            return False
        else:
            new_user = User(user_id,username, password, total, saving_rate_preference)
            self.global_user_dictionary[username] = new_user
            self.users.append(new_user)
            return True
        
    
    def authenticate(self, username, password):
        """Authenticate a user by username and password."""
        user = self.find_user(username)
        if user and user.password == password:
            return True
        return False

    def list_users(self):
        """List all users in the database."""
        return [user.to_str() for user in self.users]

    def save_users(self):
        pass