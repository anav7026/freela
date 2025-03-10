from User import User
import json 
import os


class UserDatabase :
    def __init__(self,json_file='UserInfo.json',global_user_dictionary={}):
        self.users=[]
        self.global_user_dictionary=global_user_dictionary
        self.json_file=json_file
        self.load_users_to_json()

    def load_users_to_json(self):
        if os.path.exists(self.json_file):
            with open(self.json_file,'r') as file:
                user_data=json.load(file)
                
                for user in user_data:
                    username=user["username"]
                    if username not in self.global_user_dictionary:
                        new_user=User(user["username"],user["password"],user["total"])
                        self.global_user_dictionary[username]=new_user
                        self.users.append(new_user)
                    #self.global_user_dictionary[username]=User(user["username"],user["password"])
                #self.users= [User(user["username"], user["password"]) for user in user_data]
                print(f"{len(self.global_user_dictionary)} users loaded from {self.json_file}")

    def find_user(self,username):
        for user in self.users:
            if user.username == username: 
                return user 
        return None
    
    def add_user(self, username,password):
        if self.find_user(username): 
            print(f"{username} already exist")
            return False
        
        new_user=User(username,password,0)
        self.global_user_dictionary[username]=new_user
        self.users.append(new_user)
        print(f"{username} added to user database")
        
        self.save_users()
        print("added to json successful")
        
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

    def save_users(self):
        try:
        # Convert User objects to dictionaries
            user_data = [{"username": user.username, "password": user.password, "total": user.total} for user in self.global_user_dictionary.values()]
            # Write the data to the JSON file
            with open(self.json_file, 'w') as file:
                json.dump(user_data, file, indent=4)
            print(f"✅ Users saved successfully to {self.json_file}")
        except Exception as e:
            print(f"❌ Error saving users: {e}")
