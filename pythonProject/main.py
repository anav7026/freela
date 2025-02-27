from flask import Flask, render_template,request ,redirect, url_for, Request
from UserDatabase import UserDatabase
from User import User

app = Flask(__name__)

user_db=UserDatabase()

@app.route("/") # this will become landing page with log in and sign up button + info 
def helloworld():
    return "Hello World!" 


@app.route("/home") 
def homepage():
    return render_template('home.html')

@app.route("/welcome/<username>") 
def welcome(username):
    return render_template('home.html', username=username)

@app.route("/signup" , methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        
        username = request.form.get('username')
        password = request.form.get('password')
        print(f"Received: {username}, {password}")
        print("checking database ......")

        if user_db.add_user(username,password): 
            print("true go to homepage of user")
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
            return redirect(url_for('welcome', username=username,show_alert=show_alert))
        else:
            show_alert=True
            alert ="Failed Login : Try Again 🙂‍↕️ "
            
            return render_template('login.html', show_alert=show_alert,alert=alert)
        
        print("User Database Process Completed")
      
    return render_template('login.html')


if __name__ == "__main__":
    app.run(debug=True, port=5001)

