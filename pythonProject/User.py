
import psycopg2
import os



class User:
    def __init__(self,user_id, username, password, total,saving_rate_preference,spendable_balance=None,savings_income=None):
        self.user_id=user_id
        self.username = username
        self.password = password
        self.total = total
        self.saving_rate_preference = saving_rate_preference

        self.spendable_balance = self.total * (1-self.saving_rate_preference)
        self.savings_income =  self.total * self.saving_rate_preference



        
    #Convert User object to string
    def to_str(self):
        return f"User({self.user_id}, {self.username}, {self.password}, {self.total}, {self.saving_rate_preference})"
   
    #Getters
    def get_user_id(self):
        return self.user_id
    def get_username(self):
        return self.username
    def get_password(self):
        return self.password
    def get_total(self):
        return self.total
    def get_saving_rate_preference(self):
        return self.saving_rate_preference
    def get_spendable_balance(self):
        return self.spendable_balance
    def get_savings_income(self):   
        return self.savings_income
    
    #Setters
    def set_username(self,username): #if user wants to change username [page not set up yet]
        self.username=username
    def set_password(self,password): #if user wants to change password [page not set up yet]
        self.password=password
    def set_total(self,total): #update total 
        self.total=total
    def set_saving_rate_preference(self,saving_rate_preference): #update saving rate preference
        self.saving_rate_preference=saving_rate_preference
    

   
    