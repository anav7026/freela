class Client:
    def __init__(self, user_id):
        self.user_id = user_id
        self.invoice_list= []

        

    def add_invoice(self,invoice):
        self.invoice_list.append(invoice)
        return True
    def get_invoice_list(self):
        return self.invoice_list
    
    