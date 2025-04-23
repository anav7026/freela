class User:
    def __init__(self, user_id, username, password, total=0, saving_rate_preference=0.2):
        self.user_id = user_id
        self.username = username
        self.password = password
        self.total = float(total)
        self.saving_rate_preference = float(saving_rate_preference)
    
    def get_user_id(self):
        """Get the user ID."""
        return self.user_id
    
    def get_total(self):
        """Get the total balance."""
        return self.total
    
    def get_spendable_balance(self):
        """Calculate the spendable balance."""
        return self.total * (1 - self.saving_rate_preference)
    
    def get_savings_income(self):
        """Calculate the savings income."""
        return self.total * self.saving_rate_preference
    
    def update_balance(self, amount):
        """Update the total balance."""
        self.total += amount
        return True