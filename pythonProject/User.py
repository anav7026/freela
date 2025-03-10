
class User:
    def __init__(self, username, password,total):
        self.username = username
        self.password= password
        self.total=total
        self.spendable_income= float(total*.80)
        self.tax_savings=float(total*.20)

    
    
   
