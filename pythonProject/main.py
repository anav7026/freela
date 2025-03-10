from flask import Flask, render_template,request ,redirect, url_for, Request
from UserDatabase import UserDatabase
from User import User
from TaxDocument import TaxDocument
from TaxDocumentDatabase import TaxDocumentDatabase
import json

app = Flask(__name__)

tax_doc_db=TaxDocumentDatabase()
user_db=UserDatabase()
current_user=''

@app.route("/") 
def landingpage():
    
    print("global dictionary: ",user_db.global_user_dictionary)
    return render_template('landing.html') 


@app.route("/home") 
def homepage():

    return render_template('home.html')

@app.route("/welcome/<username>") 
def welcome(username):
    user=user_db.global_user_dictionary.get(username)
    if user:
        spendable_income=user.spendable_income
        tax_savings=user.tax_savings

    return render_template('home.html', username=username,spendable_income=spendable_income,tax_savings=tax_savings)

@app.route("/signup" , methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        
        username = request.form.get('username')
        password = request.form.get('password')
        if username not in user_db.global_user_dictionary:

            print(f"Received: {username}, {password}")
            print("checking database ......")

            if user_db.add_user(username,password): 
                print("true go to homepage of user")
                current_user=username
                return redirect(url_for('welcome', username=username))
        
        print("User Database Process Completed")

        return f"Username: {username} is already taken try again!"
        
    return render_template('signup.html')

@app.route("/login" , methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        print(f"Received: {username}, {password}")
        print("checking database ......")

        if user_db.authenticate(username,password):
            show_alert=False
            print("true go to homepage of user")
            current_user=username
            return redirect(url_for('welcome', username=username,show_alert=show_alert))
        else:
            show_alert=True
            alert ="Failed Login : Try Again 🙂‍↕️ "
            
            return render_template('login.html', show_alert=show_alert,alert=alert)
        
        print("User Database Process Completed")
      
    return render_template('login.html')

@app.route("/welcome/<username>/card")
def card(username):
    user = user_db.global_user_dictionary.get(username)
    if user:
        total = user.total
        spendable_income=user.spendable_income
        tax_savings = user.tax_savings
        return render_template('card.html', total=total, spendable_income=spendable_income, tax_savings=tax_savings)
    return "Error: User not found", 404

@app.route("/welcome/<username>/taxDoc")
def taxdoc(username):
    doc_dictionary=tax_doc_db.global_doc_dictionary
    return render_template('taxdoc.html', doc_dictionary=doc_dictionary)
    



if __name__ == "__main__":
    app.run(debug=True, port=5001)

