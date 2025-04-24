import requests
import base64

client_id = 'AS65CQOi1NgNfqFsEdrSWxOww7AOiV6EtR3A2H8BVQisHBQ7ratHjABN7mI4s3XHC_UcZwRREMXZE4I6'
client_secret = 'EHnAi6d-XyQDKXAB-pjL0IljAohrRbfUjSE10q7h7uDx04MZspfsxtBbL04j5_ezx6NuaGCeLwp0pPxc'
redirect_uri = 'http://localhost:5001/callback'
code = 'auth_url = f"https://www.sandbox.paypal.com/signin/authorize?client_id={client_id}&response_type=code&scope=openid profile email address paypal.personal_information.read&redirect_uri={redirect_uri}"'
# Redirect user to auth_url # from the redirect

auth_string = f"{client_id}:{client_secret}"
encoded_auth = base64.b64encode(auth_string.encode()).decode()

headers = {
    'Authorization': f'Basic {encoded_auth}',
    'Content-Type': 'application/x-www-form-urlencoded'
}

data = {
    'grant_type': 'authorization_code',
    'code': code,
    'redirect_uri': redirect_uri
}

response = requests.post(
    'https://api-m.sandbox.paypal.com/v1/oauth2/token',
    headers=headers,
    data=data
)

token_data = response.json()
access_token = token_data['access_token']