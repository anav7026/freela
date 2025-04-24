from flask import Flask, redirect, request, session, url_for
import requests
import base64
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Set your PayPal sandbox credentials
CLIENT_ID = 'AS65CQOi1NgNfqFsEdrSWxOww7AOiV6EtR3A2H8BVQisHBQ7ratHjABN7mI4s3XHC_UcZwRREMXZE4I6'
CLIENT_SECRET = 'EHnAi6d-XyQDKXAB-pjL0IljAohrRbfUjSE10q7h7uDx04MZspfsxtBbL04j5_ezx6NuaGCeLwp0pPxc'
REDIRECT_URI = 'https://127.0.0.1:5001/paypal/callback'

SCOPES = "openid profile email address https://uri.paypal.com/services/paypalattributes"
AUTH_URL = "https://www.sandbox.paypal.com/signin/authorize"
TOKEN_URL = "https://api-m.sandbox.paypal.com/v1/oauth2/token"
USERINFO_URL = "https://api-m.sandbox.paypal.com/v1/identity/oauth2/userinfo?schema=paypalv1.1"

@app.route('/')
def home():
    return '<a href="/login">Login with PayPal</a>'

@app.route('/login')
def login():
    print("LOGIN URL:",
          f"{AUTH_URL}?response_type=code&client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&scope={SCOPES}")
    return redirect(f"{AUTH_URL}?response_type=code&client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&scope={SCOPES}")

@app.route('/paypal/callback')
def callback():
    code = request.args.get('code')
    if not code:
        return 'Authorization code not found', 400

    # Exchange the code for an access token
    basic_auth = base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode()
    headers = {
        'Authorization': f'Basic {basic_auth}',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI
    }
    token_res = requests.post(TOKEN_URL, headers=headers, data=data)
    token_json = token_res.json()

    access_token = token_json.get('access_token')
    if not access_token:
        return 'Failed to get access token', 400

    # Use the token to get user info
    userinfo_headers = {'Authorization': f'Bearer {access_token}'}
    userinfo_res = requests.get(USERINFO_URL, headers=userinfo_headers)
    userinfo = userinfo_res.json()

    # Show the user info in the browser
    return f"<pre>{userinfo}</pre>"

if __name__ == '__main__':
    app.run(debug=True,port=5001)
